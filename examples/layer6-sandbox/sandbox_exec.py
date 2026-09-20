"""
F7-LAS Layer 6 – Illustrative Minimal Execution Wrapper

This prototype trusts an unsigned JSON ``allowed`` Boolean and then dispatches
a local stub. It does not authenticate the decision, bind it to an action,
validate a policy version or expiry, or prove sandbox containment. Do not treat
it as evidence that Layer 5 approved an action.
"""

import json
import sys

from pathlib import Path

# Import the stub tool
from layer4_tools.aws_ec2_client_stub import (
    terminate_instance,
    describe_instance,
    list_instances
)


def run_action(action: str, args: dict):
    if action == "terminate_instance":
        return terminate_instance(**args)
    if action == "describe_instance":
        return describe_instance(**args)
    if action == "list_instances":
        return list_instances()
    return {"error": "Unknown action"}


def main():
    """
    Expects an illustrative /workspace/l5_decision.json input. The file is not
    authenticated or cryptographically bound to the requested action.
    """
    decision_file = Path("/workspace/l5_decision.json")

    if not decision_file.exists():
        print("[L6] No decision file found. Execution denied.")
        sys.exit(1)

    payload = json.loads(decision_file.read_text())

    if not payload.get("allowed", False):
        print(f"[L6] Execution blocked: {payload.get('reason')}")
        sys.exit(1)

    tool = payload["tool"]
    action = tool["action"]
    args = tool.get("arguments", {})

    print("[L6] Executing tool inside sandbox...")
    result = run_action(action, args)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
