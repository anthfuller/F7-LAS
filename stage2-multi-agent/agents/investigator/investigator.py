"""
F7-LAS Stage 2 – Investigator Agent (Evidence-first)
- Executes only registered read-only tools via the MCP executor (PEP + PDP enforced)
- Returns raw rows + metadata
- No LLM reasoning, no fabricated conclusions
"""

from typing import Dict, List, Any
from telemetry.logger import log_event
from telemetry.audit import write_audit
from mcp.executor import execute_read_only_tool


class InvestigatorAgent:
    def investigate(self, user_request: str, plan: Dict[str, Any], run_id: str = "run-unknown") -> Dict[str, Any]:
        tools: List[str] = plan.get("tools", [])
        context = {"user_request": user_request, "plan_domains": plan.get("domains", [])}

        log_event(event_type="investigation_started", payload={"tools": tools})
        write_audit(run_id=run_id, stage="investigation_started", data={"tools": tools, "context": context})

        results = []
        for tool in tools:
            try:
                results.append(execute_read_only_tool(tool_name=tool, run_id=run_id, context=context))
            except Exception as e:
                results.append({"tool": tool, "approved": False, "error": str(e), "rows": []})

        summary = {
            "tools_executed": [r.get("tool") for r in results],
            "total_rowcount": sum(int(r.get("rowcount", 0)) for r in results if r.get("approved")),
        }

        write_audit(run_id=run_id, stage="investigation_completed", data={"summary": summary})
        log_event(event_type="investigation_completed", payload=summary)

        return {"plan": plan, "results": results, "summary": summary}
