import json
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

OPA_ALLOW_URL = "http://opa-service:8181/v1/data/agent/security/enforcement/allow"
OPA_DENY_MSG_URL = "http://opa-service:8181/v1/data/agent/security/enforcement/deny_message"


def enforce_policy(tool_call: dict, context: dict):
    """
    F7-LAS Stage-1 PEP Core.
    Calls external PDP (OPA) for allow/deny decision.
    """

    now_est = datetime.now(ZoneInfo("America/New_York"))

    pdp_input = {
        "tool_name": tool_call.get("tool_name"),
        "action": tool_call.get("action"),
        "environment": context.get("environment"),
        "user_role": context.get("user_role"),
        "current_time_ok_for_change": (now_est.hour < 9 or now_est.hour >= 17),
        "arguments": tool_call.get("arguments"),
    }

    try:
        allow_resp = requests.post(OPA_ALLOW_URL, json={"input": pdp_input}, timeout=3)
        allow_resp.raise_for_status()
        allowed = allow_resp.json().get("result", False)

        if allowed:
            return {
                "allowed": True,
                "reason": "allowed_by_policy",
                "pdp_input": pdp_input
            }

        deny_resp = requests.post(OPA_DENY_MSG_URL, json={"input": pdp_input}, timeout=3)
        deny_msg = deny_resp.json().get("result", ["policy_denied"])[0]

        return {
            "allowed": False,
            "reason": deny_msg,
            "pdp_input": pdp_input
        }

    except Exception as e:
        return {
            "allowed": False,
            "reason": f"PDP_error: {e}",
            "pdp_input": pdp_input
        }
