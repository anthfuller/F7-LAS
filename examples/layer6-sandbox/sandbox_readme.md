# F7-LAS Layer 6 — Sandboxed Execution Environment (Stage-1)

Layer 6 (Sandbox) is responsible for limiting the blast radius of any action that passes the Layer 5 Policy Engine.

This directory contains the minimal sandbox implementation for the F7-LAS Stage-1 prototype.

---

## Goals of Layer 6

- **Provide a controlled execution boundary**
- **Ensure tool actions only run after a Layer-5 ALLOW decision**
- **Prevent accidental access to the host system**
- **Simulate real-world isolation (containers, VMs, micro-VMs)**

This stage does *not* execute real cloud APIs—only stub tools.

---

## Components

### `docker-compose.yml`
A locked-down Python sandbox with:
- Non-root user  
- Read-only filesystem  
- Isolated internal network  
- CPU & memory limits  
- Workspace at `/workspace`

### `sandbox_exec.py`
The execution wrapper:
- Loads `l5_decision.json` (written by the PEP)
- Verifies the decision (`allowed: true`)
- Runs tool stubs safely
- Produces structured JSON output for Layer 7 logging

---

## Execution Flow

L3 (Planner) → produces tool call
L4 (Tools) → defines schemas & stubs
L5 (PEP/PDP) → produces l5_decision.json
L6 (Sandbox) → executes tool inside container
L7 (Telemetry) → logs action + result

Sandbox only runs **after** Layer 5 approves.

---

## Running the Sandbox

```bash
docker compose up

echo '{ "allowed": true, "tool": {"action": "describe_instance", "arguments": {"instance_id": "i-prod-1234"}} }' \
  > ./layer6-sandbox/l5_decision.json

# Restart the container

docker compose restart

# View Results

docker logs f7las_sandbox

---

# Summary 
---

## Notes

This is *not* a production sandbox.  
It is a minimal demonstration of F7-LAS Layer 6 mechanics:

- Isolation
- Controlled execution
- Post-policy validation
- Minimal blast radius

A full Layer-6 implementation (Stage-3) would include:

- Firecracker microVM isolation
- Seccomp/eBPF syscall restrictions
- Network egress filtering
- Capability dropping (Linux capabilities)
- Per-tool micro-sandboxes

This Stage-1 sandbox is intentionally lightweight to demonstrate the control flow between Layer 5 → Layer 6.

