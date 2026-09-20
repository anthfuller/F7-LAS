# F7-LAS Layer 3 – Illustrative Simple Planner Stub
# ---------------------------------------------
# This planner is intentionally minimal. It simulates
# LLM→Planner behavior without using an actual model.

def simple_planner(user_input: str) -> dict:
    """
    Illustrative planner stub.
    Takes user input -> identifies intent -> returns a tool call structure.
    
    This is a deterministic stand-in for an LLM planner. It returns proposal
    data only. This function does not route through or enforce Layer 5; the
    calling workflow must perform policy evaluation before any invocation.
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
