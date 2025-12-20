"""
MCP Executor (Layer 4 enforced by Layer 5)
Central execution gateway: PDP -> execute -> L7 audit
"""

from __future__ import annotations

import os
import re
from datetime import timedelta, datetime, date
from typing import Any, Dict, Optional, List

from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient

from mcp.tools import build_query
from pdp.pdp import evaluate
from telemetry.audit import write_audit
from telemetry.logger import log_event


_AGO_RE = re.compile(r"ago\(\s*(\d+)\s*([smhd])\s*\)", re.IGNORECASE)


def _timespan_from_query(query: str) -> Optional[timedelta]:
    """
    If query contains `ago(7d)` / `ago(24h)` etc, return a matching timedelta.
    Otherwise None (let API default).
    """
    m = _AGO_RE.search(query)
    if not m:
        return None
    n = int(m.group(1))
    unit = m.group(2).lower()
    if unit == "s":
        return timedelta(seconds=n)
    if unit == "m":
        return timedelta(minutes=n)
    if unit == "h":
        return timedelta(hours=n)
    if unit == "d":
        return timedelta(days=n)
    return None


def _to_json_primitive(v: Any) -> Any:
    if v is None:
        return None
    if isinstance(v, (str, int, float, bool)):
        return v
    if isinstance(v, (datetime, date)):
        # Sentinel often returns timezone-aware; isoformat is fine for JSON + parsing
        return v.isoformat()
    # Fallback for SDK objects
    return str(v)


def execute(
    tool_name: str,
    *,
    run_id: str,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    built = build_query(tool_name, params=params)
    action = built["action"]

    # === L5: Policy Decision ===
    decision = evaluate(
        action=action,
        context={"limit": built["limit"], "has_time_filter": built["has_time_filter"]},
        run_id=run_id,
    )

    if decision["decision"] != "ALLOW":
        write_audit(run_id=run_id, stage="mcp_denied", data={"tool": tool_name, "action": action, "reason": decision["reason"]})
        return {
            "tool": tool_name,
            "action": action,
            "decision": decision["decision"],
            "reason": decision["reason"],
            "query": built["query"],
            "table": built["table"],
            "rowcount": 0,
            "columns": [],
            "rows": [],
        }

    # === L4: Real Execution ===
    workspace_id = os.getenv("SENTINEL_WORKSPACE_ID")
    if not workspace_id:
        raise EnvironmentError("Missing environment variable: SENTINEL_WORKSPACE_ID")

    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)

    ts = _timespan_from_query(built["query"])  # IMPORTANT: match query window when present
    response = client.query_workspace(workspace_id=workspace_id, query=built["query"], timespan=ts)

    columns: List[str] = []
    rows: List[List[Any]] = []
    rowcount = 0

    if response and getattr(response, "tables", None):
        t0 = response.tables[0]

        # Columns can be objects; always normalize to names
        raw_cols = getattr(t0, "columns", None) or []
        for c in raw_cols:
            columns.append(getattr(c, "name", c if isinstance(c, str) else str(c)))

        raw_rows = getattr(t0, "rows", None) or []
        for r in raw_rows:
            # LogsTableRow is iterable; convert to list + primitive values
            as_list = list(r) if not isinstance(r, list) else r
            rows.append([_to_json_primitive(v) for v in as_list])

        rowcount = len(rows)

    # === L7: Audit ===
    write_audit(
        run_id=run_id,
        stage="mcp_executed",
        data={"tool": tool_name, "action": action, "table": built["table"], "query": built["query"], "rowcount": rowcount},
    )
    log_event("mcp_tool_executed", {"run_id": run_id, "tool": tool_name, "table": built["table"], "rowcount": rowcount})

    return {
        "tool": tool_name,
        "action": action,
        "decision": "ALLOW",
        "query": built["query"],
        "table": built["table"],
        "rowcount": rowcount,
        "columns": columns,
        "rows": rows[:50],
    }
