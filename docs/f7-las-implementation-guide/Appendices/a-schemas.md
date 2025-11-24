
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

**Supports**:
- Prompt-drift detection
- PSP version enforcement
- CAB review traceability

_No optional fields recommended for this baseline event._

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

**Supports**:
- SLA-based loop termination compliance
- Unsafe planning detection
- ATLAS-aligned anomaly analysis

_Optional additions_: `step_duration_ms`, `trigger_event`

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

**Supports**:
- RAG poisoning detection
- Retrieval-quality metrics
- Layer-2 observability

** Optional Extensions**:
| Field                 | Type     | Description                                  |
|----------------------|----------|----------------------------------------------|
| retrieval_strategy   | string   | "dense", "sparse", "hybrid"                  |
| trust_score_method   | string   | Method of trust calculation                  |
| response_token_count | integer  | Returned token count                         |

---

## A.4 Tool Call Request (Layer 4 — Tool Surface)

Represents a request to invoke an external tool.

```json
{
  "event_type": "tool_call_request",
  "timestamp": "2025-01-01T12:40:15Z",
  "trace_id": "req-9912",
  "agent_id": "remediator",
  "tool_name": "isolate_endpoint",
  "tool_args": {
    "device_id": "host-11",
    "reason": "ransomware_suspected"
  },
  "tool_schema_version": "v2.0",
  "credential_scope": "sp-remediator-limited",
  "risk_score": 0.82
}
```

**Supports**:
- Tool-misuse detection
- Over-privilege prevention
- Credential-scope audits

** Optional Extensions**:
| Field              | Type     | Description                                     |
|-------------------|----------|-------------------------------------------------|
| invocation_channel| string   | "api_gateway", "plugin_runtime"                |
| tool_timeout_ms   | integer  | Max execution time                              |
| justification     | string   | Why the tool was called                         |
| dry_run           | boolean  | Simulated call without execution                |

---

## A.5 Policy Decision (Layer 5 — Hard Guardrails)

Represents the decision returned by a PDP.

```json
{
  "event_type": "policy_decision",
  "timestamp": "2025-01-01T12:40:16Z",
  "trace_id": "req-9912",
  "subject": {
    "agent_id": "remediator",
    "delegated_user": "sec_analyst_03",
    "agent_trust_score": 0.91
  },
  "action": "isolate_endpoint",
  "resource": "host-11",
  "context": {
    "risk_level": "high",
    "time_of_day": "after_hours"
  },
  "decision": "permit_with_obligation",
  "obligations": ["mask_sensitive_fields"],
  "policy_id": "abac-rule-22"
}
```

**Supports**:
- Layer-5 enforcement
- Policy-bypass detection
- HITL override triggers

** Optional Extensions**:
| Field                  | Type     | Purpose                                  |
|-----------------------|----------|------------------------------------------|
| decision_explanation  | string   | Explanation or policy reference          |
| policy_version        | string   | Version of applied policy                |
| evaluation_duration_ms| integer  | Time spent on policy check               |
| decision_confidence   | float    | ML-driven confidence score               |

---

## A.6 Tool Execution Result (Layer 4 / Layer 6)

Represents the result of a tool execution within a sandbox.

```json
{
  "event_type": "tool_execution_result",
  "timestamp": "2025-01-01T12:40:18Z",
  "trace_id": "req-9912",
  "tool_name": "isolate_endpoint",
  "status": "success",
  "execution_time_ms": 420,
  "sandbox_id": "aca-sbx-033",
  "egress_limited": true,
  "output": {
    "message": "Endpoint isolation initiated.",
    "ticket_id": "IR-22991"
  }
}
```

**Supports**:
- Sandbox-boundary validation
- Tool reliability scoring
- Layer-6 blast-radius analysis

** Optional Extensions**:
| Field                 | Type     | Description                                     |
|----------------------|----------|-------------------------------------------------|
| output_hash          | string   | Hash of output for tamper resistance            |
| failure_reason       | string   | Reason string for failed executions             |
| sandbox_runtime      | string   | E.g., "firecracker", "gvisor", "wasmtime"       |
| resource_modifications | array | List of modified targets                        |
| execution_logs_url   | string   | Pointer to detailed execution trace or logs     |

---

## A.7 Monitoring & Evaluation Event (Layer 7 — Oversight)

Represents a periodic health, trust, or drift evaluation signal.

```json
{
  "event_type": "agent_monitor_event",
  "timestamp": "2025-01-01T12:45:00Z",
  "agent_id": "coordinator",
  "metrics": {
    "planner_loop_termination_rate": 1.0,
    "tool_failure_rate": 0.02,
    "rag_trust_score_avg": 0.91,
    "telemetry_completeness": 0.97
  },
  "drift_signals": {
    "prompt_drift": false,
    "rag_dataset_drift": false,
    "tool_permission_drift": true
  },
  "alerts_raised": ["sandbox_permission_expansion"],
  "reporting_interval_sec": 60,
  "agent_trust_score": 0.94,
  "drift_score": 0.23,
  "alert_severity": ["medium"],
  "compliance_flags": {
    "psp_compliant": true,
    "policy_signed": true
  },
  "evaluation_snapshot_id": "eval-2025-11-23T12:45Z"
}
```

**Supports**:
- Drift detection
- SLO measurement
- ATLAS-aligned threat visibility

---

## A.8 Multi-Agent Choreography Event (Cross-Agent)

Represents a coordination or task handoff event between agents.

```json
{
  "event_type": "multi_agent_coordination",
  "timestamp": "2025-01-01T12:50:12Z",
  "source_agent": "coordinator",
  "target_agent": "investigator",
  "handoff_reason": "requires_deep_alert_analysis",
  "task_context": {
    "alert_id": "A-55210",
    "severity": "high"
  },
  "handoff_type": "escalation",
  "handoff_trace_id": "handoff-9912",
  "trust_transfer_score": 0.87,
  "requires_ack": true,
  "ack_timestamp": "2025-01-01T12:50:15Z"
}
```

**Supports**:
- Multi-agent audit trails
- Escalation modeling
- Provenance of distributed decisions

** Optional Extensions**:
| Field                 | Type     | Description                                     |
|----------------------|----------|-------------------------------------------------|
| handoff_type         | string   | E.g., "escalation", "delegation", "handover"    |
| handoff_trace_id     | string   | Allows full trace correlation across agents     |
| trust_transfer_score | float    | Confidence score in target agent                |
| requires_ack         | boolean  | Whether target agent must confirm handoff       |
| ack_timestamp        | string   | When the handoff was acknowledged               |


## License & Disclaimer

© 2025 Anthony L. Fuller. All rights reserved.

#### This work is created independently by the author and is not affiliated with, endorsed by, or associated with Microsoft or any other employer. Opinions and materials represent the author’s personal work.
