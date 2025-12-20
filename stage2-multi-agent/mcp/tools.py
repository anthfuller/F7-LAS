# mcp/tools.py
from __future__ import annotations

from typing import Any, Dict


def build_query(*, tool: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tool -> query contract builder.

    Returns a dict with:
      - table: Sentinel table name
      - query: KQL string
      - workspace_id: Log Analytics Workspace ID (GUID)
      - default_days: int (used if query doesn't contain ago())
    """
    workspace_id = params.get("workspace_id") or params.get("law_workspace_id")
    if not workspace_id:
        # Keep the error explicit so you don't get silent empty results.
        raise ValueError("Missing workspace_id in tool params (workspace_id / law_workspace_id).")

    # Default lookback: 7 days (you can tighten later)
    default_days = int(params.get("default_days", 7))

    tool = (tool or "").strip()

    if tool == "sentinel.security_incident.take":
        take = int(params.get("take", 20))
        query = f"SecurityIncident | sort by TimeGenerated desc | take {take}"
        return {"table": "SecurityIncident", "query": query, "workspace_id": workspace_id, "default_days": default_days}

    if tool == "sentinel.security_alert.take":
        take = int(params.get("take", 20))
        query = f"SecurityAlert | sort by TimeGenerated desc | take {take}"
        return {"table": "SecurityAlert", "query": query, "workspace_id": workspace_id, "default_days": default_days}

    if tool == "sentinel.signin_logs.take":
        take = int(params.get("take", 50))
        query = f"SigninLogs | sort by TimeGenerated desc | take {take}"
        return {"table": "SigninLogs", "query": query, "workspace_id": workspace_id, "default_days": default_days}

    if tool == "sentinel.azure_activity.take":
        take = int(params.get("take", 50))
        query = f"AzureActivity | sort by TimeGenerated desc | take {take}"
        return {"table": "AzureActivity", "query": query, "workspace_id": workspace_id, "default_days": default_days}

    if tool == "sentinel.sentinel_audit.take":
        take = int(params.get("take", 50))
        query = f"SentinelAudit | sort by TimeGenerated desc | take {take}"
        return {"table": "SentinelAudit", "query": query, "workspace_id": workspace_id, "default_days": default_days}

    # Escape hatch: allow raw KQL (still read-only)
    if tool == "sentinel.kql":
        query = params.get("query")
        if not query:
            raise ValueError("sentinel.kql requires params['query']")
        # Table is unknown here; downstream will still store evidence file if investigator chooses
        return {"table": params.get("table", "custom"), "query": str(query), "workspace_id": workspace_id, "default_days": default_days}

    raise ValueError(f"Unknown tool: {tool}")
