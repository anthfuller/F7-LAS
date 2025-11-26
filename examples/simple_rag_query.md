# Simple RAG Query Walkthrough (Stage 0)

This example shows how a single analyst-style question would conceptually
flow through an F7-LAS–aligned system.

> **Scenario**  
> A SOC analyst wants to know:  
> *"What should I do about a high-severity Defender for Endpoint alert on host `SRV-APP-01`?"*

---

## 1. Coordinator Receives the Request (Layer 1 + 3)

1. The **Coordinator agent** system prompt is governed by its Prompt Security Profile (PSP).
2. The incoming request is classified as:
   - Risk tier: `medium`
   - Intent: investigation / triage, not remediation

The **agent policy** (`agent-policy.json`) permits the coordinator and
investigator to handle medium-risk investigative tasks.

---

## 2. Grounding via RAG (Layer 2)

The coordinator decides to ground the answer with internal knowledge:

- Allowed collections from `rag-policy.json`:
  - `kb_security_playbooks`
  - `kb_detection_engineering`
  - `kb_f7las_docs`

Disallowed collections such as `hr_records` and `customer_pii_raw` are
never requested as part of the RAG retrieval.

The RAG engine logs a retrieval event (for Layer 7 telemetry) and returns:

- A Windows EDR triage playbook  
- A detection rule description  
- A containment checklist

---

## 3. Investigator Builds the Plan (Layer 3)

The **Investigator agent**:

1. Summarizes the key facts from the RAG step.
2. Proposes a step-by-step investigation plan, such as:
   - Check alert details and related incidents.
   - Review recent process and network activity.
   - Look for similar alerts on adjacent hosts.
3. Marks all actions as *investigative* only — no changes to production.

Because the risk tier is `medium`, the agent policy does **not** require HITL yet.

---

## 4. Tool Use Under Policy (Layer 4 + 5 + 6)

For each step that touches a tool:

- Tool access is checked against `tool-policy.json`.
- Sandbox constraints (non-production tenants, dry-run where applicable)
  are applied from `sandbox-policy.json`.

Examples:

- `sentinel_query` → **allowed**, read-only.  
- `ticket_create` → **allowed**, medium risk.  
- `network_isolate_host` → **denied** at this stage (requires HITL).

Any attempt to call a denied tool would be blocked by the Layer 5 policy
engine and surfaced back to the coordinator as a policy violation.

---

## 5. Response Back to the Human (Layer 7)

The final answer sent to the analyst includes:

- A clear *investigation plan*.
- Explicit statement that **no remediation actions were taken**.
- A note indicating which steps would require human approval or a
  higher-risk policy before execution (e.g., host isolation).

Telemetry emitted:

- Correlated trace ID across coordinator, investigator, and tools.
- RAG collections consulted.
- Policy decisions (allow / deny / log-only).

This example is intentionally high level and technology-neutral,
showing how **F7-LAS ties prompts, policies, tools, and sandbox
controls together for a single RAG-based query.**
