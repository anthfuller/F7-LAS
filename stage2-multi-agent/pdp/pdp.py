from telemetry.audit import write_audit
from telemetry.logger import log_event


def evaluate(action: str, context: dict, run_id: str = "run-unknown") -> dict:
    """
    Central PDP decision for Stage2.

    Principles:
    - ALLOW read-only KQL execution against registered MCP tools.
    - REQUIRE_HITL for any write/modify intent (future expansion).
    - DENY unknown actions.
    """

    # Read-only KQL tools (LAW)
    if action.startswith("sentinel_read_only:") or action.startswith("sentinel_query:"):
        decision = {"decision": "ALLOW", "reason": "Registered read-only KQL action"}
    elif action.startswith("write:") or action.startswith("modify:") or action.startswith("delete:"):
        decision = {"decision": "REQUIRES_HUMAN_APPROVAL", "reason": "Write action requires HITL"}
    else:
        decision = {"decision": "DENY", "reason": "Action not permitted"}

    write_audit(
        run_id=run_id,
        stage="pdp_decision",
        data={"action": action, "decision": decision["decision"], "reason": decision["reason"], "context": context},
    )

    log_event(event_type="pdp_evaluation", payload={"action": action, **decision})
    return decision
