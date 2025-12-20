# mcp/executor.py
from __future__ import annotations

import re
from dataclasses import asdict
from datetime import timedelta, datetime
from typing import Any, Dict, List, Optional

from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient, LogsQueryStatus

from mcp.tools import build_query
from telemetry.audit import write_audit
from telemetry.logger import log_event


_AGO_RE = re.compile(r"ago\(\s*(\d+)\s*([smhd])\s*\)", re.IGNORECASE)


def _infer_timespan_from_kql(kql: str, default: timedelta) -> timedelta:
    """
    If query contains ago(7d)/ago(24h)/ago(15m), use the largest value found.
    Otherwise return default.
    """
    if not kql:
        return default

    best: Optional[timedelta] = None
    for m in _AGO_RE.finditer(kql):
        n = int(m.group(1))
        unit = m.group(2).lower()
        if unit == "s":
            ts = timedelta(seconds=n)
        elif unit == "m":
            ts = timedelta(minutes=n)
        elif unit == "h":
            ts = timedelta(hours=n)
        else:  # d
            ts = timedelta(days=n)

        best = ts if best is None else max(best, ts)

    return best or default


def _json_safe_value(v: Any) -> Any:
    """
    Convert Azure SDK / datetime-ish values to JSON-safe primitives.
    """
    if v is None:
        return None
    if isinstance(v, (str, int, float, bool)):
        return v
    if isinstance(v, datetime):
        # Prefer ISO8601; keep Z out if tz-naive
        return v.isoformat()
    # Fallback: string
    return str(v)


def _json_safe_rows(rows: Any) -> List[List[Any]]:
    """
    Convert LogsTableRow or other row objects into list-of-lists.
    """
    out: List[List[Any]] = []
    if not rows:
        return out

    for row in rows:
        # Azure returns LogsTableRow which is iterable
        try:
            seq = list(row)
        except Exception:
            out.append([_json_safe_value(row)])
            continue

        out.append([_json_safe_value(x) for x in seq])

    return out


def _json_safe_columns(cols: Any) -> List[str]:
    """
    Convert Azure Column objects to column-name strings.
    """
    out: List[str] = []
    if not cols:
        return out

    for c in cols:
        name = getattr(c, "name", None)
        out.append(str(name) if name else str(c))
    return out


def execute(tool: str, *, run_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a read-only Log Analytics query via Azure Monitor LogsQueryClient.
    Returns JSON-safe result with: table, query, columns(list[str]), rows(list[list]), rowcount.
    """
    contract = build_query(tool=tool, params=params)

    # Contract fields
    workspace_id = contract.get("workspace_id")
    if not workspace_id:
        raise ValueError("workspace_id missing (set in params or config)")

    kql = contract["query"]
    table_name = contract.get("table", "unknown")

    # Default to 7 days unless query itself declares a bigger/smaller window via ago()
    default_ts = timedelta(days=int(contract.get("default_days", 7)))
    timespan = _infer_timespan_from_kql(kql, default_ts)

    log_event("mcp_execute_started", {"run_id": run_id, "tool": tool, "table": table_name})
    write_audit(run_id=run_id, stage="mcp_execute_started", data={"tool": tool, "table": table_name, "query": kql})

    cred = DefaultAzureCredential()
    client = LogsQueryClient(cred)

    try:
        response = client.query_workspace(workspace_id, kql, timespan=timespan)
    except Exception as e:
        err = {
            "ok": False,
            "tool": tool,
            "table": table_name,
            "query": kql,
            "error": str(e),
            "rowcount": 0,
            "columns": [],
            "rows": [],
        }
        write_audit(run_id=run_id, stage="mcp_execute_error", data=err)
        log_event("mcp_execute_error", {"run_id": run_id, "tool": tool, "table": table_name})
        return err

    # Handle partial success
    if response.status == LogsQueryStatus.PARTIAL:
        tables = response.partial_data or []
        error_info = response.partial_error
    else:
        tables = response.tables or []
        error_info = None

    if not tables:
        result = {
            "ok": True,
            "tool": tool,
            "table": table_name,
            "query": kql,
            "rowcount": 0,
            "columns": [],
            "rows": [],
            "partial_error": asdict(error_info) if error_info else None,
        }
        write_audit(run_id=run_id, stage="mcp_execute_complete", data={"tool": tool, "table": table_name, "rowcount": 0})
        log_event("mcp_execute_complete", {"run_id": run_id, "tool": tool, "table": table_name, "rowcount": 0})
        return result

    # Use first table (typical)
    t0 = tables[0]
    columns = _json_safe_columns(getattr(t0, "columns", None))
    rows = _json_safe_rows(getattr(t0, "rows", None))

    result = {
        "ok": True,
        "tool": tool,
        "table": table_name,
        "query": kql,
        "columns": columns,
        "rows": rows,
        "rowcount": len(rows),
        "partial_error": asdict(error_info) if error_info else None,
    }

    write_audit(run_id=run_id, stage="mcp_execute_complete", data={"tool": tool, "table": table_name, "rowcount": result["rowcount"]})
    log_event("mcp_execute_complete", {"run_id": run_id, "tool": tool, "table": table_name, "rowcount": result["rowcount"]})
    return result
