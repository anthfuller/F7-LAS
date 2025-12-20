from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any

TOOLS_CONTRACT = Path(__file__).parents[1] / "contracts" / "tools_contract.json"


def _load_tools() -> Dict[str, Any]:
    with TOOLS_CONTRACT.open(encoding="utf-8") as f:
        return json.load(f)


def build_query(tool_name: str, *, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    doc = _load_tools()
    tools = {t["tool"]: t for t in doc["tools"]}

    if tool_name not in tools:
        raise KeyError(f"Unknown tool: {tool_name}. Available: {list(tools.keys())}")

    spec = tools[tool_name]

    limit = params.get("limit", spec.get("default", {}).get("limit", 50))
    max_limit = spec.get("constraints", {}).get("max_limit", limit)
    limit = min(limit, max_limit)

    query = spec["template"].format(limit=limit)

    return {
        "tool": spec["tool"],
        "action": spec["action"],
        "table": spec["table"],
        "query": query,
        "limit": limit,
        "has_time_filter": "TimeGenerated" in query,
    }
