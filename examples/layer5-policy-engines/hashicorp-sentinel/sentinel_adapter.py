"""
HashiCorp Sentinel PDP Adapter (F7-LAS Layer 5)
Maps F7-LAS PDP input → Sentinel-style allow/deny logic.
"""

from typing import Dict, Tuple


def sentinel_check(pdp_input: Dict) -> Tuple[bool, str]:
    action = pdp_input.get("action")
    env = pdp_input.get("environment")
    time_ok = pdp_input.get("current_time_ok_for_change")

    # Allow all read-only actions
    if action.startswith(("get_", "list_", "describe_")):
        return True, "Allowed by Sentinel: read-only action."

    # Handle destructive action
    if action == "terminate_instance":
        if env == "production" and not time_ok:
            return False, (
                "Denied by Sentinel: destructive production action outside approved window."
            )
        if env != "production" and time_ok:
            return True, (
                "Allowed by Sentinel: destructive action in non-production with approved time."
            )

    # Default deny
    return False, "Denied by Sentinel: no allow rule matched."
