from telemetry.audit import write_audit
from telemetry.logger import log_event

def evaluate(action: str, context: dict) -> dict:
    if action.startswith("sentinel_read_only_"):
        decision = {
            "decision": "REQUIRES_HUMAN_APPROVAL",
            "reason": "Human approval required before MCP execution"
        }
    else:
        decision = {
            "decision": "DENY",
            "reason": "Action not permitted"
        }

    log_event(
        event_type="pdp_evaluation",
        payload={"action": action, **decision}
    )

    return decision
