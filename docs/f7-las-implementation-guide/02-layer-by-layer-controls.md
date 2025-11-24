# 2. Layer-by-Layer Implementation Controls

## Layer 1 — System Prompt (Soft Policy)
### Control Requirements
- Declare role, scope, prohibited actions, escalation rules.
- Enforce deterministic structure with delimiters.
- Integrate a Prompt Security Profile (PSP).

### Implementation Actions
- Use versioned prompt files in GitHub.
- Require CAB approval for prompt changes.
- Validate prompt templates with `validate_prompts.py`.

---

## Layer 2 — RAG / Grounding (Epistemic Guardrail)
### Control Requirements
- All retrieved documents must meet trust/ti­er requirements.
- Retrieval logs must be stored for auditing.

### Implementation Actions
- Validate source trust scores.
- Enforce allowed data domains with Layer 5.
- Integrate poisoning detection checks.

---

## Layer 3 — Agent Planner / Controller
### Control Requirements
- Bound reasoning loops.
- Define stop conditions.
- Require plan-audit logging.

### Implementation Actions
- Set max_steps in `settings.yaml`.
- Use ReAct/PDDL hybrid planning if applicable.
- Enforce loop-termination SLOs.

---

## Layer 4 — Tools & Integrations
### Control Requirements
- Tool whitelisting.
- Least privilege credentialing.
- Structured tool schemas.

### Implementation Actions
- Use MCP tool definition format.
- Integrate tool-schema validation into CI.
- Store tool credentials in Azure Key Vault.

---

## Layer 5 — Policy Engine Outside the LLM
### Control Requirements
- All high-risk actions require PDP/PEP approval.
- Support Permit / Deny / Obligations / Human Review.

### Implementation Actions
- Use ABAC or OPA/Rego policies.
- Use the Tripwire logging pattern.
- Enforce evaluation at every tool invocation.

---

## Layer 6 — Sandboxed Execution Environment
### Control Requirements
- Network isolation.
- Ephemeral sandboxes.
- Privilege minimization.

### Implementation Actions
- Use Azure Container Apps isolated environments.
- Use per-agent service principals.
- Implement egress restrictions.

---

## Layer 7 — Monitoring & Evaluation
### Control Requirements
- Full telemetry collection across layers.
- Drift detection.
- Incident response hooks.

### Implementation Actions
- Emit structured logs for: inputs, RAG docs, loops, tool calls, decisions.
- Use a model-derived trust score.
- Integrate with SOC/SIEM workflows.

