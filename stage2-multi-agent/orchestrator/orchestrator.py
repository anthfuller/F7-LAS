"""
F7-LAS Stage 2 – Orchestrator (Layer 3)
Coordinator -> Investigator -> Remediator.
All executions go through centralized PEP (mcp.executor) which calls PDP.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict

from telemetry.audit import write_audit
from telemetry.logger import log_event
from agents.coordinator.coordinator import CoordinatorAgent
from agents.investigator.investigator import InvestigatorAgent
from agents.remediator.remediator import RemediatorAgent


class Orchestrator:
    def __init__(self):
        self.coordinator = CoordinatorAgent()
        self.investigator = InvestigatorAgent()
        self.remediator = RemediatorAgent()

    def run(self, user_request: str) -> Dict[str, Any]:
        run_id = f"run-{uuid.uuid4().hex[:12]}"
        log_event("orchestration_started", {"run_id": run_id, "request": user_request})
        write_audit(run_id=run_id, stage="run_started", data={"request": user_request})

        coordination = self.coordinator.handle_request(user_request, run_id=run_id)
        plan = coordination.get("plan", [])

        investigation = self.investigator.investigate(plan, run_id=run_id)

        remediation_proposal = self.remediator.propose(investigation, run_id=run_id)

        result = {
            "run_id": run_id,
            "coordination": coordination,
            "investigation": investigation,
            "remediation": remediation_proposal,
        }

        write_audit(run_id=run_id, stage="run_completed", data={"summary": {"plan_steps": len(plan)}})
        log_event("orchestration_completed", {"run_id": run_id, "plan_steps": len(plan)})
        return result
