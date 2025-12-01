import requests
from datetime import datetime
import zoneinfo

OPA_ALLOW_URL = "http://opa-service:8181/v1/data/agent/security/enforcement/allow"
OPA_DENY_URL  = "http://opa-service:8181/v1/data/agent/security/enforcement/deny_message"

def enforce_l5_policy(tool_call_payload, execution_context):
    eastern = zoneinfo.ZoneInfo("America/New_York")
    now_est = datetime.now(tz=eastern)
    time_ok = now_est.hour < 9 or now_est.hour >= 17

    pdp_input = {
        "tool_name": tool_call_payload.get("tool_name"),
        "action": tool_call_payload.get("action"),
        "environment": execution_context.get("target_environment"),
        "user_role": execution_context.get("initiating_user_role"),
        "arguments": tool_call_payload.get("arguments"),
        "current_time_ok_for_change": time_ok
    }

    try:
        r = requests.post(OPA_ALLOW_URL, json={"input": pdp_input}, timeout=3)
        r.raise_for_status()

        decision = r.json().get("result", False)

        if decision:
            return True

        # get deny reason
        d = requests.post(OPA_DENY_URL, json={"input": pdp_input}, timeout=3)
        deny_msgs = d.json().get("result", ["Unknown denial"])
        deny_msg = deny_msgs[0] if isinstance(deny_msgs, list) else deny_msgs

        return deny_msg

    except Exception as e:
        return f"L5 Policy Engine unavailable (fail closed): {e}"
