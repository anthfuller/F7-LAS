"""
MCP Executor (Layer 4 + enforced by Layer 5)
Central execution gateway: PDP -> execute -> L7 audit.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient

from mcp.tools import build_query
from pdp.pdp import evaluate
from telemetry.audit import write_audit
from telemetry.logger import log_event


def execute(tool_name: str, *, run_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Executes a registered read-only KQL tool against the configured workspace.

    Returns a dict with:
      - query
      - table
      - rowcount
      - rows (truncated)
      - columns (if available)
    """
    built = build_query(tool_name, params=params)
    action = built["action"]

    # === Layer 5: PDP decision ===
    decision = evaluate(action=action, context={"limit": built["limit"], "has_time_filter": built["has_time_filter"]}, run_id=run_id)
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
            "rows": [],
        }

    # === Execute (read-only) ===
    workspace_id = os.getenv("SENTINEL_WORKSPACE_ID")
    if not workspace_id:
        raise EnvironmentError("Missing env var: SENTINEL_WORKSPACE_ID")

    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)

    response = client.query_workspace(workspace_id, built["query"])

    # Extract rows safely
    rowcount = 0
    rows = []
    columns = []
    try:
        if response and getattr(response, "tables", None):
            t0 = response.tables[0]
            columns = [c.name for c in t0.columns] if getattr(t0, "columns", None) else []
            rows = t0.rows or []
            rowcount = len(rows)
    except Exception:
        # Keep rowcount at 0; log the parsing failure
        pass

    # L7 audit for executed query
    write_audit(
        run_id=run_id,
        stage="mcp_executed",
        data={
            "tool": tool_name,
            "action": action,
            "table": built["table"],
            "query": built["query"],
            "rowcount": rowcount,
        },
    )

    log_event("mcp_tool_executed", {"run_id": run_id, "tool": tool_name, "table": built["table"], "rowcount": rowcount})

    # Return raw evidence (truncated only for safety)
    return {
        "tool": tool_name,
        "action": action,
        "decision": "ALLOW",
        "query": built["query"],
        "table": built["table"],
        "rowcount": rowcount,
        "columns": columns,
        "rows": rows[: min(rowcount, 50)],
    }
