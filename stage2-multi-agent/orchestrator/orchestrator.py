"""
F7-LAS Stage 2 – Orchestrator (Evidence pipeline)
Coordinator -> creates plan
Investigator -> executes plan (PEP/PDP enforced in MCP executor)
Remediator -> proposes HITL next steps
"""

from agents.coordinator.coordinator import CoordinatorAgent
from agents.investigator.investigator import InvestigatorAgent
from agents.remediator.remediator import RemediatorAgent
from telemetry.logger import log_event
from telemetry.audit import write_audit
import uuid


class Orchestrator:
    def __init__(self):
        self.coordinator = CoordinatorAgent()
        self.investigator = InvestigatorAgent()
        self.remediator = RemediatorAgent()

    def run(self, user_request: str) -> dict:
        run_id = f"run-{uuid.uuid4().hex[:12]}"
        write_audit(run_id=run_id, stage="run_started", data={"user_request": user_request})
        log_event(event_type="run_started", payload={"run_id": run_id})

        plan = self.coordinator.handle_request(user_request, run_id=run_id)
        investigation = self.investigator.investigate(user_request, plan, run_id=run_id)
        remediation = self.remediator.propose(investigation, run_id=run_id)

        result = {"run_id": run_id, "plan": plan, "investigation": investigation, "remediation": remediation}
        write_audit(run_id=run_id, stage="run_completed", data={"summary": investigation.get("summary", {})})
        log_event(event_type="run_completed", payload={"run_id": run_id})
        return result
