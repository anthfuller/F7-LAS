from telemetry.audit import write_audit
from telemetry.logger import log_event


def request_approval(action: str, context: dict, run_id: str = "run-unknown") -> bool:
    """
    Human-in-the-Loop (HITL) gate.

    Stub implementation:
    - Logs request
    - Audits pending approval
    - Denies by default

    Future replacements:
    - ServiceNow
    - Teams approval
    - Portal-based workflow
    """

    log_event(
        event_type="human_approval_requested",
        payload={"action": action}
    )

    # === Audit HITL decision boundary (Layer 7) ===
    write_audit(
        run_id=run_id,
        stage="human_approval",
        data={
            "action": action,
            "status": "PENDING"
        }
    )

    # Explicit deny-by-default
    return False
