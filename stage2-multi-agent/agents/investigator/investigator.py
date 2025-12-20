"""
F7-LAS Stage 2 – Investigator Agent (Layer 3)
Evidence-first execution.
Runs an explicit plan through the centralized MCP executor.
Persists raw evidence for downstream signal extraction.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Iterable

from telemetry.audit import write_audit
from telemetry.logger import log_event
from mcp.executor import execute as mcp_execute


def _json_safe(v: Any) -> Any:
    """Convert common SDK / datetime types into JSON-safe primitives."""
    if v is None:
        return None
    if isinstance(v, datetime):
        # keep timezone if present
        return v.isoformat()
    # Some SDK types have isoformat-like behavior
    iso = getattr(v, "isoformat", None)
    if callable(iso):
        try:
            return iso()
        except Exception:
            pass
    # primitives
    if isinstance(v, (str, int, float, bool)):
        return v
    # dict-like
    if isinstance(v, dict):
        return {str(k): _json_safe(val) for k, val in v.items()}
    # list/tuple-like
    if isinstance(v, (list, tuple)):
        return [_json_safe(x) for x in v]
    return str(v)


def _row_to_list(row: Any) -> List[Any]:
    """
    Azure Monitor Query returns LogsTableRow which is iterable but not list/tuple.
    Convert anything row-like into a list of values.
    """
    if isinstance(row, list):
        return row
    if isinstance(row, tuple):
        return list(row)

    # LogsTableRow (and similar) is iterable
    try:
        return list(row)  # <-- critical fix
    except TypeError:
        return [row]


class InvestigatorAgent:
    def __init__(self):
        pass

    def investigate(self, plan: List[Dict[str, Any]], *, run_id: str) -> Dict[str, Any]:
        log_event("investigator_started", {"run_id": run_id, "steps": len(plan)})

        evidence: List[Dict[str, Any]] = []

        evidence_dir = Path("runs") / run_id / "evidence"
        evidence_dir.mkdir(parents=True, exist_ok=True)

        for step in plan:
            tool = step.get("tool")
            params = step.get("params") or {}
            if not tool:
                continue

            result = mcp_execute(tool, run_id=run_id, params=params)
            evidence.append(result)

            table = result.get("table")
            if not table:
                continue

            raw_rows = result.get("rows", [])
            safe_rows = []
            for r in raw_rows:
                values = _row_to_list(r)
                safe_rows.append([_json_safe(v) for v in values])

            payload = {
                "table": table,
                "query": result.get("query"),
                "columns": result.get("columns", []),
                "rows": safe_rows,
                "rowcount": result.get("rowcount", 0),
            }

            evidence_file = evidence_dir / f"{table.lower()}.json"
            with evidence_file.open("w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)

        write_audit(run_id=run_id, stage="investigation_complete", data={"evidence_items": len(evidence)})
        log_event("investigator_completed", {"run_id": run_id, "evidence_items": len(evidence)})

        return {"evidence": evidence}
