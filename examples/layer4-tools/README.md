# Layer 4 — Tools (Action Surface)

Layer 4 contains placeholder tools representing the system’s “Actuators.”

These tools are intentionally simple.  
They illustrate how agents perform actions after passing Layer 5.

## Files

### `tool_schema.json`
Defines:
- tool name  
- available actions  
- expected arguments  

### `aws_ec2_client_stub.py`
Simulated tool functions for:
- `terminate_instance`
- `describe_instance`
- `list_instances`

## Purpose

Layer 4 is the **risk surface**.  
Every tool call must pass through Layer 5 (PDP/PEP) before reaching this layer.
