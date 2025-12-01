# examples/layer5-policy-engines/aws-cedar/pep_cedar.py
import json
import requests

CEDAR_PDP_URL = "http://cedar-authz-service/evaluate"

def cedar_enforce(tool_call: dict, ctx: dict) -> bool:
    request = {
        "principal": {"type": "Agent", "id": ctx.get("agent_id", "unknown-agent")},
        "action": {"type": "Action", "id": tool_call["action_name"]},
        "resource": {
            "type": "Environment",
            "id": ctx.get("environment", "unknown-env")
        },
        "context": {
            "environment": ctx.get("environment"),
            "current_time_ok_for_change": ctx.get("current_time_ok_for_change", False)
        }
    }

    resp = requests.post(CEDAR_PDP_URL, json=request, timeout=3)
    resp.raise_for_status()
    decision = resp.json().get("decision", "deny")
    return decision == "allow"

# Example
if __name__ == "__main__":
    tool_call = {"action_name": "TerminateInstance"}
    context = {"environment": "production", "current_time_ok_for_change": False}
    allowed = cedar_enforce(tool_call, context)
    print("Allowed?", allowed)
