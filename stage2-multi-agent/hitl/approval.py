from telemetry.logger import log_event

def request_approval(action: str, context: dict) -> bool:
    """
    HITL stub.
    Replace later with ticketing (Service Now perhaps) / portal / Teams approval.
    """
    log_event(
        event_type="human_approval_requested",
        payload={"action": action}
    )

    # Explicit deny-by-default
    return False
