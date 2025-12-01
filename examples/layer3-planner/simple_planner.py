# F7-LAS Layer 3 – Simple Planner (Stage 1 Stub)
# ---------------------------------------------
# This planner is intentionally minimal. It simulates
# LLM→Planner behavior without using an actual model.

def simple_planner(user_input: str) -> dict:
    """
    Stage-1 Planner Stub.
    Takes user input -> identifies intent -> returns a tool call structure.
    
    This is a safe, deterministic stand-in for an LLM planner.
    It will ALWAYS route through Layer 5 (PDP/PEP) before L4 executes.
    """

    text = user_input.lower()

    # Unsafe intent → maps to destructive tool call
    if "shutdown" in text or "terminate" in text or "delete" in text:
        return {
            "tool_name": "aws_ec2_client",
            "action": "terminate_instance",
            "arguments": {
                "instance_id": "i-prod-1234"
            }
        }

    # Default → safe read-only action
    return {
        "tool_name": "aws_ec2_client",
        "action": "describe_instance",
        "arguments": {
            "instance_id": "i-prod-1234"
        }
    }
