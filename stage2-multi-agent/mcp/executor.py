from typing import Any, Dict, List, Optional
import os
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient

from telemetry.logger import log_event
from telemetry.audit import write_audit
from pdp.pdp import evaluate as pdp_evaluate
from hitl.approval import request_approval
from mcp.tools import get_tool_query


def _rows_from_response(response: Any) -> List[Dict[str, Any]]:
    """
    Convert azure.monitor.query response -> list[dict].
    Handles both single and multi-table responses.
    """
    rows: List[Dict[str, Any]] = []
    if response is None:
        return rows

    # SDK returns LogsQueryResult with .tables
    tables = getattr(response, "tables", None)
    if not tables:
        return rows

    for t in tables:
        cols = [c.name for c in t.columns]
        for r in t.rows:
            rows.append({cols[i]: r[i] for i in range(len(cols))})
    return rows


def execute_read_only_tool(tool_name: str, run_id: str, context: Optional[dict] = None) -> Dict[str, Any]:
    """
    Policy-enforced execution of a registered, read-only MCP tool (KQL).
    Returns raw rows + metadata. No summarization.
    """
    context = context or {}
    action = f"sentinel_read_only:{tool_name}"

    # PDP decision
    decision = pdp_evaluate(action=action, context=context, run_id=run_id)
    if decision["decision"] == "REQUIRES_HUMAN_APPROVAL":
        approved = request_approval(action=action, context=context, run_id=run_id)
        if not approved:
            return {"tool": tool_name, "approved": False, "reason": decision["reason"], "rows": []}
    elif decision["decision"] != "ALLOW":
        return {"tool": tool_name, "approved": False, "reason": decision["reason"], "rows": []}

    query = get_tool_query(tool_name)

    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    workspace_id = os.getenv("SENTINEL_WORKSPACE_ID")
    if not workspace_id:
        raise RuntimeError("Missing SENTINEL_WORKSPACE_ID environment variable")

    response = client.query_workspace(workspace_id, query)
    rows = _rows_from_response(response)

    meta = {"tool": tool_name, "approved": True, "rowcount": len(rows), "query": query}
    write_audit(run_id=run_id, stage="mcp_tool_executed", data=meta)
    log_event(event_type="mcp_tool_executed", payload={"tool": tool_name, "rowcount": len(rows)})

    return {**meta, "rows": rows}
