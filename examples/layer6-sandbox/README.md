# Layer 6 — Sandbox (Execution Isolation)

Layer 6 provides a minimal isolated environment for executing allowed actions.

## Files

### `docker-compose.yml`
Creates a private, internal-only container network to simulate isolation.

### `sandbox_readme.md`
Describes how the sandbox is used to contain execution after Layer 5 approval.

## Notes

This is not a production sandbox.  
A full L6 implementation would use:
- Firecracker microVMs  
- syscall filtering  
- eBPF restrictions  
- seccomp profiles  
- privilege dropping  

Purpose: **Demonstrate isolation and blast-radius control.**
