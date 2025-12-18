"""
F7-LAS Stage 2 – MCP Tool Registry (LAW-backed, read-only)
Contract-driven. No schema guessing. No unregistered tables.
"""

import json
import os
from typing import Dict, Any, List

_CONTRACT_PATH = os.path.join(os.path.dirname(__file__), "..", "contracts", "tools_contract.json")

def _load_contract() -> Dict[str, Any]:
    with open(_CONTRACT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

TOOLS: Dict[str, Any] = _load_contract()

def _format_value(v: Any) -> str:
    if isinstance(v, str):
        return f'"{v}"'
    if isinstance(v, bool):
        return "true" if v else "false"
    if v is None:
        return "null"
    return str(v)

def _build_where(where: List[Dict[str, Any]]) -> str:
    if not where:
        return ""
    parts=[]
    for w in where:
        col=w["col"]
        op=w["op"]
        val=w.get("value")
        if op == "in" and isinstance(val, list):
            vals=", ".join(_format_value(x) for x in val)
            parts.append(f"{col} in ({vals})")
        else:
            parts.append(f"{col} {op} {_format_value(val)}")
    return " | where " + " and ".join(parts)

def get_tool_query(tool_name: str) -> str:
    if tool_name not in TOOLS:
        raise ValueError(f"Tool not registered: {tool_name}")

    spec = TOOLS[tool_name]
    table = spec["table"]
    lookback = spec.get("lookback", "24h")
    project = spec.get("project", [])
    where = spec.get("where", [])

    project_clause = ""
    if project:
        project_clause = " | project " + ", ".join(project)

    # NOTE: Intentionally keep queries simple and contract-locked.
    query = f"""{table}
| where TimeGenerated > ago({lookback}){_build_where(where)}{project_clause}
| take 50
"""
    return query
