# stage2-multi-agent/mcp/tools.py
from __future__ import annotations

import json
from pathlib import Path
from dataclasses import dataclass
from typing import Any, Dict, Optional

TOOLS_CONTRACT_PATH = Path(__file__).resolve().parents[1] / "contracts" / "tools_contract.json"

@dataclass(frozen=True)
class ToolSpec:
    tool: str
    action: str
    table: str
    template: str
    default: Dict[str, Any]
    constraints: Dict[str, Any]

def _load_tools_contract() -> Dict[str, Any]:
    with TOOLS_CONTRACT_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def get_tool_spec(tool_name: str) -> ToolSpec:
    doc = _load_tools_contract()
    tools = doc.get("tools", [])
    for t in tools:
        if t.get("tool") == tool_name:
            return ToolSpec(
                tool=t["tool"],
                action=t["action"],
                table=t["table"],
                template=t["template"],
                default=t.get("default", {}) or {},
                constraints=t.get("constraints", {}) or {},
            )
    raise KeyError(f"Unknown tool: {tool_name}")

def build_query(tool_name: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Returns: query, action, table, limit, has_time_filter
    """
    spec = get_tool_spec(tool_name)
    params = params or {}

    limit = int(params.get("limit", spec.default.get("limit", 20)))
    max_limit = spec.constraints.get("max_limit")
    if max_limit is not None and limit > int(max_limit):
        raise ValueError(f"limit {limit} exceeds max_limit {max_limit} for tool {tool_name}")

    query = spec.template.format(limit=limit)
    has_time_filter = ("TimeGenerated" in query) and ("ago(" in query)

    return {
        "tool": spec.tool,
        "query": query,
        "action": spec.action,
        "table": spec.table,
        "limit": limit,
        "has_time_filter": has_time_filter,
    }
