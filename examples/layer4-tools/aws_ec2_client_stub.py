# F7-LAS Layer 4 – AWS EC2 Client Stub (Stage-1)
# ------------------------------------------------
# This simulates an EC2 tool interface.
# No real cloud calls. Purely deterministic and safe.

def terminate_instance(instance_id: str) -> dict:
    """
    Simulate a destructive EC2 action.
    Actual execution only happens AFTER passing Layer 5 (PDP/PEP)
    and running inside Layer 6 (Sandbox).
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
