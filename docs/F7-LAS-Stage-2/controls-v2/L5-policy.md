# Layer 5 — Policy Enforcement v2

**Status:** Draft (Stage-2)

Hard guardrails mediating every tool call.

## Decision Model (v2)

```text
Request
  → Classify risk (from L4)
  → Check environment policy
  → Check timing constraints
  → Produce decision: allow / deny / escalate
