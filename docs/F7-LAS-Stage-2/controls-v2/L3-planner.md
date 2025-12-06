# Layer 3 — Planner v2 Guardrails Specification

**Status:** Draft (Stage-2)

The Planner enforces intent-aware sequencing of actions before tools execute.

## Controls (Stage-2 Initial Set)

| Control | Description | Enforcement Point |
|--------|-------------|------------------|
| Plan-Diff Check | Compare proposed plan vs executed actions | Planner / Telemetry |
| Escalation Block | Prevent unsanctioned privilege escalation | Planner + Policy |
| Safe-Step Rules | Prohibit unsafe multi-step sequences | Planner |
| Max Plan Depth | Cap number of chained actions | Planner config |
| Risk Scoring | Evaluate plan before execution | Planner → Policy |

## Outputs
- `plan_trace_v2.json`
- `risk_vector` per action
