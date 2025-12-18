"""
MCP Tool Registry (Layer 4)
Loads *registered, read-only* tools from contracts/tools_contract.json.
No hard-coded queries. No non-contract tables.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

CONTRACT_PATH = Path(__file__).resolve().parents[1] / "contracts" / "tools_contract.json"


@dataclass(frozen=True)
class ToolSpec:
    name: str
    action: str
    table: str
    template: str
    default: Dict[str, Any]
    constraints: Dict[str, Any]


def _load_contract() -> Dict[str, ToolSpec]:
    if not CONTRACT_PATH.exists():
        raise FileNotFoundError(f"Missing tool contract: {CONTRACT_PATH}")
    raw = json.loads(CONTRACT_PATH.read_text(encoding="utf-8", errors="ignore"))
    tools: Dict[str, ToolSpec] = {}
    for t in raw.get("tools", []):
        spec = ToolSpec(
            name=t["name"],
            action=t["action"],
            table=t["table"],
            template=t["template"],
            default=t.get("default") or {},
            constraints=t.get("constraints") or {},
        )
        tools[spec.name] = spec
    return tools


_TOOL_CACHE: Optional[Dict[str, ToolSpec]] = None


def get_tool_spec(tool_name: str) -> ToolSpec:
    global _TOOL_CACHE
    if _TOOL_CACHE is None:
        _TOOL_CACHE = _load_contract()
    if tool_name not in _TOOL_CACHE:
        raise ValueError(f"Tool not registered: {tool_name}")
    return _TOOL_CACHE[tool_name]


def build_query(tool_name: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Returns:
      - query: str
      - action: str
      - table: str
      - limit: int
      - has_time_filter: bool
    """
    spec = get_tool_spec(tool_name)
    params = params or {}
    limit = int(params.get("limit", spec.default.get("limit", 20)))

    max_limit = spec.constraints.get("max_limit")
    if max_limit is not None and limit > int(max_limit):
        raise ValueError(f"limit {limit} exceeds max_limit {max_limit} for tool {tool_name}")

    query = spec.template.format(limit=limit)

    # Minimal guard: enforce presence of TimeGenerated filter in template-based tools
    has_time_filter = "TimeGenerated" in query and "ago(" in query

    return {
        "query": query.strip(),
        "action": spec.action,
        "table": spec.table,
        "limit": limit,
        "has_time_filter": has_time_filter,
    }
