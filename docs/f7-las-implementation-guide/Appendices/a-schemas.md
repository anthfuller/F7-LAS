
# 📚 Appendix A — Reference Telemetry Schemas

These schemas support F7-LAS Layers 1–7 and optional cross-layer coordination. Each is designed to be:

- Minimal (for baseline observability)
- Extensible (for advanced deployments)
- Vendor-neutral and audit-friendly

---

## A.1 Prompt Event (Layer 1 — System Prompt)

Represents a system-prompt load event or prompt version change.

```json
{
  "event_type": "prompt_load",
  "timestamp": "2025-01-01T12:00:00Z",
  "agent_id": "coordinator",
  "prompt_version": "v7.2",
  "prompt_hash": "sha256:4f2ab91...",
  "psp_id": "psp-coordinator-001",
  "change_ticket": "CAB-2025-114",
  "approver": "sec-arch"
}
```

**Supports:**

- Prompt-drift detection
- PSP version enforcement
- CAB review traceability

---

## A.2 Planner Step Event (Layer 3 — Planner / Controller)

Represents a single reasoning step within a ReAct, PDDL, or hybrid planning loop.

```json
{
  "event_type": "planner_step",
  "timestamp": "2025-01-01T12:30:01Z",
  "agent_id": "investigator",
  "plan_id": "plan-7811",
  "step_number": 4,
  "reasoning_trace": "Reviewing alert details...",
  "planned_action": "query_siem",
  "stop_condition_triggered": false,
  "max_steps": 12,
  "loop_terminated": false
}
```

**Supports:**

- SLA-based loop termination compliance
- Unsafe planning detection
- ATLAS-aligned anomaly analysis

_Add `step_duration_ms` or `trigger_event` for deeper tracing._

---

## A.3 RAG Retrieval Event (Layer 2 — Grounding)

Represents a single RAG grounding retrieval operation.

```json
{
  "event_type": "rag_retrieval",
  "timestamp": "2025-01-01T12:35:01Z",
  "trace_id": "abc123",
  "agent_id": "coordinator",
  "query": "latest password reset policy",
  "source_id": "policy_kb",
  "document_ids": ["doc-4421", "doc-9921"],
  "top_k": 5,
  "avg_trust_score": 0.93,
  "min_trust_score": 0.88,
  "poisoning_flags": {
    "suspicious_terms": false,
    "out_of_domain": false
  }
}
```

**Supports:**

- RAG poisoning detection
- Retrieval-quality metrics
- Layer-2 observability

**🧠 Optional Extensions**

| Field                | Type     | Description                                   |
|---------------------|----------|-----------------------------------------------|
| retrieval_strategy  | string   | `"dense"`, `"sparse"`, `"hybrid"`             |
| trust_score_method  | string   | How trust was computed (e.g., embedding+domain)|
| response_token_count| integer  | Token count in returned context               |

---

(Section continues with other schemas...)
