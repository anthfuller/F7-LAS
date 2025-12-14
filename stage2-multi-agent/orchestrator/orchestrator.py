"""
F7-LAS Stage 2 – Orchestrator
Coordinates Coordinator, Investigator, and Remediator agents.
Centralized PDP enforced.
"""

from telemetry.audit import write_audit
from agents.coordinator.coordinator import CoordinatorAgent
from agents.investigator.investigator import InvestigatorAgent
from agents.remediator.remediator import RemediatorAgent
from policy.policy_engine import PolicyEngine
from telemetry.logger import log_event


class Orchestrator:
    def __init__(self):
        self.pdp = PolicyEngine()
        self.coordinator = CoordinatorAgent()
        self.investigator = InvestigatorAgent()
        self.remediator = RemediatorAgent(policy_gateway_client=self.pdp)

    def run(self, user_request: str):
        log_event("orchestration_started", {"request": user_request})

        coordination = self.coordinator.handle_request(user_request)

        investigation = self.investigator.investigate(user_request)

        remediation_proposal = self.remediator.propose(investigation)

        result = {
            "coordination": coordination,
            "investigation": investigation,
            "remediation": remediation_proposal
        }

        log_event("orchestration_completed", result)
        return result
