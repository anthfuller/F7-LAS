"""
F7-LAS Stage 2 – Remediator Agent
Propose-only by default; execution requires centralized PDP + human approval.
"""

from typing import Dict, List, Any
from telemetry.logger import log_event


class RemediatorAgent:
    def __init__(self, policy_gateway_client=None):
        """
        policy_gateway_client: required for authorization checks before execution
        """
        self.pdp = policy_gateway_client

    def propose(self, investigator_findings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a remediation proposal based on investigator findings.
        """
        log_event(
            event_type="remediation_proposal_started",
            payload={"findings": investigator_findings}
        )

        plan = self._build_plan(investigator_findings)

        result = {
            "remediation_plan": plan,
            "approval_status": "Pending",
            "execution_log": []
        }

        log_event(
            event_type="remediation_proposal_completed",
            payload=result
        )

        return result

    def execute(self, approved_plan: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute remediation ONLY after PDP + human approval.
        """
        if not self.pdp:
            raise RuntimeError("PDP client not configured")

        authorization = self.pdp.authorize(approved_plan)

        if not authorization.get("approved"):
            log_event(
                event_type="remediation_execution_denied",
                payload={"reason": authorization.get("reason")}
            )
            return {
                "approval_status": "Denied",
                "execution_log": []
            }

        execution_log = []

        for action in approved_plan:
            # Placeholder for gateway-mediated execution
            execution_log.append({
                "action": action,
                "status": "Executed via centralized gateway"
            })

        result = {
            "approval_status": "Approved",
            "execution_log": execution_log
        }

        log_event(
            event_type="remediation_execution_completed",
            payload=result
        )

        return result

    def _build_plan(self, findings: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Build a conservative, reversible remediation plan.
        """
        plan = [
            {
                "action": "Contain affected entity",
                "risk": "Medium",
                "rollback": "Revert containment"
            }
        ]

        return plan
