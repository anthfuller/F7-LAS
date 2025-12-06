# Layer 3 — Planner / Controller v2 Spec

**Status:** Draft (Stage-2)**  
**Scope:** Schema + behavior spec only (no runtime wiring yet)

The Planner converts intent → structured actions that can be checked by:
L4 (tool risk), L5 (policy), L6 (sandbox), and L7 (telemetry).

---

## Planner Output Schema (v2)

```jsonc
{
  "plan_id": "string",
  "agent_id": "string",
  "target_environment": "production|staging|dev",
  "impact_level": "low|medium|high",
  "steps": [
    {
      "step_id": "string",
      "description": "string",
      "reasoning": "string",
      "tool_name": "string",
      "action": "string",
      "arguments": {},
      "step_dependency": "string|null",
      "requires_approval": false,
      "risk_flags": []
    }
  ]
}
