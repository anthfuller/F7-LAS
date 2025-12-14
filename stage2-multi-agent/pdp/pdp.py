"""
Centralized Policy Decision Point (PDP)
Stage 2: execution is explicitly denied.
"""

from telemetry.logger import log_event

def evaluate(action: str, context: dict) -> dict:
    decision = {
        "decision": "DENY",
        "reason": "Execution disabled in Stage 2 (proposal-only)"
    }

    log_event(
        event_type="pdp_evaluation",
        payload={
            "action": action,
            "decision": decision["decision"],
            "reason": decision["reason"]
        }
    )

    return decision
