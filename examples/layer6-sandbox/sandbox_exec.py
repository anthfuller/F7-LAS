"""
F7-LAS Layer 6 – Minimal Sandbox Execution Wrapper (Stage-1)

This safely executes tool functions ONLY if Layer 5 approved the action.
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
    Expects a file called /workspace/l5_decision.json written by the PEP.
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
