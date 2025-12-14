from telemetry.audit import write_audit
from telemetry.logger import log_event


def evaluate(action: str, context: dict, run_id: str = "run-unknown") -> dict:
    # === Decision point: PDP evaluation ===
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

    # === Audit PDP decision (Layer 7) ===
    write_audit(
        run_id=run_id,
        stage="pdp_decision",
        data={
            "action": action,
            "decision": decision["decision"],
            "reason": decision["reason"]
        }
    )

    log_event(
        event_type="pdp_evaluation",
        payload={"action": action, **decision}
    )

    return decision
