"""
MCP Executor (Layer 4 enforced by Layer 5)
Central execution gateway: PDP -> execute -> L7 audit
"""

from __future__ import annotations

import os
from datetime import timedelta
from typing import Any, Dict, Optional

from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient

from mcp.tools import build_query
from pdp.pdp import evaluate
from telemetry.audit import write_audit
from telemetry.logger import log_event


def execute(
    tool_name: str,
    *,
    run_id: str,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Execute a registered, read-only KQL tool against Microsoft Sentinel.
    """

    built = build_query(tool_name, params=params)
    action = built["action"]

    # === L5: Policy Decision ===
    decision = evaluate(
        action=action,
        context={
            "limit": built["limit"],
            "has_time_filter": built["has_time_filter"],
        },
        run_id=run_id,
    )

    if decision["decision"] != "ALLOW":
        write_audit(
            run_id=run_id,
            stage="mcp_denied",
            data={
                "tool": tool_name,
                "action": action,
                "reason": decision["reason"],
            },
        )
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

    # === L4: Real Execution ===
    workspace_id = os.getenv("SENTINEL_WORKSPACE_ID")
    if not workspace_id:
        raise EnvironmentError("Missing environment variable: SENTINEL_WORKSPACE_ID")

    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)

    response = client.query_workspace(
        workspace_id=workspace_id,
        query=built["query"],
        timespan=timedelta(hours=24),
    )

    rows = []
    columns = []
    rowcount = 0

    if response and getattr(response, "tables", None):
        table = response.tables[0]
        columns = [c.name for c in table.columns]
        rows = table.rows or []
        rowcount = len(rows)

    # === L7: Audit ===
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

    log_event(
        "mcp_tool_executed",
        {
            "run_id": run_id,
            "tool": tool_name,
            "table": built["table"],
            "rowcount": rowcount,
        },
    )

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
