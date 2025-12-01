# examples/layer5-policy-engines/azure-custom/azure_pdp.py
import json
from pathlib import Path
from typing import Any, Dict

def load_policy(path: str) -> Dict[str, Any]:
    return json.loads(Path(path).read_text())

def evaluate_request(request: Dict[str, Any], policy: Dict[str, Any]) -> bool:
    """
    Returns True if allowed, False if denied.
    Fail-closed: if policy matches, we deny (deny_on_match).
    """
    action = request.get("action")
    env = request.get("environment")
    time_ok = request.get("current_time_ok_for_change")
    role = request.get("user_role")

    if action != policy["target_action"]:
        return True  # policy doesn't apply, allow by default (up to you)

    # Check exception first
    for exc in policy.get("allow_exceptions", []):
        if exc["field"] == "user_role" and role == exc["value"]:
            return True

    # Evaluate deny conditions
    cond_env = env == "production"
    cond_time = (time_ok is False)

    if cond_env and cond_time:
        return False  # deny

    return True

def enforce_l5_policy(tool_call: Dict[str, Any], context: Dict[str, Any], policy_path: str) -> bool:
    policy = load_policy(policy_path)
    req = {
        "action": tool_call.get("action"),
        "environment": context.get("environment"),
        "current_time_ok_for_change": context.get("current_time_ok_for_change"),
        "user_role": context.get("user_role")
    }
    allowed = evaluate_request(req, policy)
    print("L5 Azure PDP decision:", "ALLOW" if allowed else "DENY")
    return allowed

if __name__ == "__main__":
    tool_call = {"action": "terminate_instance"}
    ctx = {"environment": "production", "current_time_ok_for_change": False, "user_role": "devops_engineer"}
    enforce_l5_policy(tool_call, ctx, "policy_prod_safety.json")
