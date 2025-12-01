# examples/layer5-policy-engines/spicedb/pep_spicedb.py
import requests

SPICEDB_URL = "http://spicedb:8443/v1/permissions/check"

def spicedb_destructive_allowed(user_id: str, env_id: str) -> bool:
    body = {
        "resource": {
            "object_type": "environment",
            "object_id": env_id
        },
        "permission": "maintainer",
        "subject": {
            "object": {
                "object_type": "user",
                "object_id": user_id
            }
        }
    }
    resp = requests.post(SPICEDB_URL, json=body, timeout=3)
    resp.raise_for_status()
    return resp.json().get("permissionship") == "PERMISSIONSHIP_HAS_PERMISSION"

def enforce_l5_policy(tool_call: dict, ctx: dict) -> bool:
    """Combine SpiceDB (role/env) with time window in PEP."""
    action = tool_call.get("action")
    env = ctx.get("environment")
    user_id = ctx.get("user_id")
    time_ok = ctx.get("current_time_ok_for_change", False)

    if action != "terminate_instance":
        return True

    if env == "production" and not time_ok:
        return False

    # Check if user is allowed in that env
    if not spicedb_destructive_allowed(user_id=user_id, env_id=env):
        return False

    return True
