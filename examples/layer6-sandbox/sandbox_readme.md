# F7-LAS Layer 6 — Illustrative Sandboxed Execution Environment

Layer 6 (Sandbox) is responsible for limiting the blast radius of any action that passes the Layer 5 Policy Engine.

This directory contains an illustrative minimal sandbox prototype.

---

## Intended Layer 6 goals

- Provide a controlled execution boundary.
- Require a verified Layer 5 authorization before execution.
- Limit access to the host and external systems.
- Bound execution with containers, VMs, or micro-VMs.

These are design goals, not behavior verified by the current example. The
example does not execute real cloud APIs.

---

## Components

### `docker-compose.yml`
A draft container configuration showing:
- Non-root user  
- Read-only filesystem  
- Isolated internal network  
- CPU & memory limits  
- Workspace at `/workspace`

The current Compose file does not mount `sandbox_exec.py`, the Layer 4 stub, or
a decision file into `/workspace`. It therefore cannot execute the documented
flow as written and is retained only as an illustrative configuration draft.

### `sandbox_exec.py`
The execution wrapper:
- Loads an illustrative `l5_decision.json` file.
- Trusts its unsigned `allowed: true` value without authenticating the source.
- Dispatches a local tool stub.
- Prints JSON output.

It does not verify approval binding, integrity, policy version, expiry, tool
authorization, argument schemas, or containment.

---

## Execution Flow

L3 (Planner) → produces tool call
L4 (Tools) → defines schemas & stubs
L5 (PEP/PDP) → produces l5_decision.json
L6 (Sandbox) → executes tool inside container
L7 (Telemetry) → logs action + result

The sequence above is the intended architecture. The current standalone files
do not enforce that sequence.

---

## Execution status

There is currently no supported runnable walkthrough for this Compose example.
Functional repair and automated negative-path testing belong to the canonical
implementation milestone. Do not use the configuration as a security boundary.

---

# Summary 
---

## Notes

This is *not* a production sandbox.  
It is a minimal illustration of intended Layer 6 concepts:

- Isolation goals
- Controlled-execution sequencing
- Post-policy validation requirements
- Blast-radius reduction

A production Layer-6 implementation would require:

- Firecracker microVM isolation
- Seccomp/eBPF syscall restrictions
- Network egress filtering
- Capability dropping (Linux capabilities)
- Per-tool micro-sandboxes

This sandbox is intentionally lightweight and illustrates a possible Layer 5 → Layer 6 handoff. It is not verified containment.
