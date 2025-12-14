def evaluate(action: str, context: dict) -> dict:
    if action.startswith("sentinel_read_only_"):
        return {
            "decision": "ALLOW",
            "reason": "Approved read-only Sentinel query"
        }

    return {
        "decision": "DENY",
        "reason": "Action not permitted"
    }
