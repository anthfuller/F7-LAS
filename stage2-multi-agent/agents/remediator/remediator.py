from pdp.pdp import evaluate
from telemetry.logger import log_event

class RemediatorAgent:
    def propose(self, investigation: dict):
        action = "proposed_remediation"

        pdp_result = evaluate(action, investigation)

        remediation_plan = [{
            "action": "Contain affected entity",
            "risk": "Medium",
            "rollback": "Revert containment"
        }]

        result = {
            "remediation_plan": remediation_plan,
            "pdp_decision": pdp_result,
            "approval_status": "Pending"
        }

        log_event(
            event_type="remediation_proposal_completed",
            payload=result
        )

        return result
