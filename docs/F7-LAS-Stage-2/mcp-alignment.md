# Layer-by-Layer Alignment (F7-LAS ↔ MCP)

Purpose:
Document alignment of F7-LAS runtime controls with external industry practices —
including the MCP security paper — while preserving F7-LAS independence.

F7-LAS is a vendor-neutral model.
External papers provide influence, not direction.

## Mapping Overview (Draft v0.1)

| F7-LAS Layer | Security Control Focus | Corresponding MCP Section | Alignment Status |
|-------------|----------------------|---------------------------|------------------|
| L1 System Prompt | Soft policy + intent boundaries | Prompt Hardening | Planned v0.2 |
| L2 Grounding | Epistemic guardrails | Tool metadata accuracy | Planned v0.2 |
| L3 Planner | Action planning controls | Agent intent validation | In-Progress |
| L4 Tools | Allowed action surface | Capability + interface constraints | In-Progress |
| L5 Policy Engine | Hard guardrails + decisions | Tool enforcement policies | In-Progress |
| L6 Sandbox | Execution isolation | Runtime boundary controls | Planned v0.2 |
| L7 Monitoring | Drift + action audit | Traceability + metrics | In-Progress |

