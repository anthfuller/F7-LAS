# F7-LAS Layer 4 – Illustrative AWS EC2 Client Stub
# ------------------------------------------------
# This simulates an EC2 tool interface.
# No real cloud calls. Purely deterministic and safe.

def terminate_instance(instance_id: str) -> dict:
    """
    Simulate a destructive EC2 action.

    This stub contains no Layer 5 or Layer 6 enforcement. A calling workflow
    can invoke it directly, so it must be treated as illustrative only.
    """
    print(f"[SIMULATION] Terminating instance: {instance_id}")
    return {
        "action": "terminate_instance",
        "instance_id": instance_id,
        "status": "simulated"
    }


def describe_instance(instance_id: str) -> dict:
    """
    Simulate an informational read-only call.
    """
    return {
        "instance_id": instance_id,
        "status": "running",
        "simulated": True
    }


def list_instances() -> dict:
    """
    Simulate listing all instances.
    """
    return {
        "instances": [
            {"instance_id": "i-prod-1234", "status": "running"},
            {"instance_id": "i-dev-5678", "status": "stopped"}
        ],
        "simulated": True
    }
