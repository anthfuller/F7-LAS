"""
F7-LAS Stage 2 – Investigator Agent (Layer 3)
Evidence-first execution: runs an explicit plan through the centralized PEP/MCP executor.
Returns raw evidence only.
"""

from __future__ import annotations

from typing import Any, Dict, List

from telemetry.audit import write_audit
from telemetry.logger import log_event
from mcp.executor import execute as mcp_execute


class InvestigatorAgent:
    def __init__(self):
        pass

    def investigate(self, plan: List[Dict[str, Any]], *, run_id: str) -> Dict[str, Any]:
        log_event("investigator_started", {"run_id": run_id, "steps": len(plan)})

        evidence: List[Dict[str, Any]] = []

        for step in plan:
            tool = step.get("tool")
            params = step.get("params") or {}
            if not tool:
                continue

            result = mcp_execute(tool, run_id=run_id, params=params)
            evidence.append(result)

        write_audit(run_id=run_id, stage="investigation_complete", data={"evidence_items": len(evidence)})
        log_event("investigator_completed", {"run_id": run_id, "evidence_items": len(evidence)})

        return {"evidence": evidence}
