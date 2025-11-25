# Appendix B — Templates

This appendix provides ready-to-use templates that support the deployment, governance, and review of systems built using the F7-LAS framework.

Organizations should clone these templates into their internal repositories and customize them based on their risk appetite, tooling, and regulatory environment.

B.1 Implementation Profile Template

A full Implementation Profile defines how your environment implements each F7-LAS layer, including controls, telemetry expectations, and multi-agent patterns.

## F7-LAS Implementation Profile — <System Name>

### 1. Metadata
- System name:
- Owner team:
- Review date:
- Reviewer(s):
- Environment(s): (dev/test/prod)
- Agent runtime/framework:
- Multi-agent? (yes/no)

### 2. Architecture Summary
- High-level description:
- Deployment pattern:
- Supported use cases:
- Expected security posture:

## 3. Layer-by-Layer Component Map
### Layer 1 — Prompting
- Prompt file path:
- PSP ID:
- Reviewers/approvers:

### Layer 2 — Grounding
- RAG sources:
- Trust-score policy:
- Allowed domains:

### Layer 3 — Planner
- Planning pattern:
- max_steps:
- Loop termination conditions:

### Layer 4 — Tools
- Tool list:
- Credential scopes:
- Risk tiers:

### Layer 5 — Policy Engine
- PDP/PEP components:
- ABAC/Rego rule sets:
- Human-in-the-loop rules:

### Layer 6 — Sandbox
- Isolation model:
- Tenant/subscription:
- Egress restrictions:

### Layer 7 — Monitoring
- Telemetry destinations:
- Key metrics/SLOs:
- Drift signals monitored:

## 4. Telemetry Schema Map
- Prompt events:
- RAG events:
- Planner traces:
- Tool calls/results:
- Policy decisions:
- Sandbox logs:
- Monitoring signals:

## 5. Multi-Agent Governance (If Applicable)
- Roles (Coordinator/Investigator/Remediator):
- Handoff rules:
- Choreography model:

## 6. Risks & Mitigations
- High-risk tools:
- Known failure modes:
- Mitigations in place:

## 7. Appendices / Evidence
- CAB tickets:
- Red-team logs:
- Policy review notes:

## B.2 Prompt Security Profile (PSP) Template

A PSP defines the security boundaries, escalation rules, and governance around a system prompt.

## Prompt Security Profile (PSP) — <Agent Name>

### 1. Metadata
- PSP ID:
- Agent role:
- Owner team:
- Reviewer/approver:
- Risk tier (low/medium/high/critical):

### 2. Purpose & Scope
- Intended tasks:
- Out-of-scope actions:

### 3. Safety Rules
- Forbidden actions:
- Required escalation behaviors:
- HITL triggers:

### 4. Grounding Requirements
- Allowed RAG sources:
- Sensitive/restricted domains:
- Input validation rules:

### 5. Prompt Structure
- Structure enforced? (Y/N)
- Delimiters used?
- Versioning approach:

### 6. Change Management
- Reviewers:
- Change approval process (CAB or equivalent):
- Storage path (repo/file):

### 7. Testing & Validation
- Red-team tests performed:
- Known failure cases:
- Mitigations in place:


## B.3 Policy Engine Template (ABAC/OPA/Rego)

Defines a policy in the Layer-5 PDP/PEP model.

package f7las.policies

default allow = false

### Example rule — deny destructive actions on sensitive assets
deny[msg] {
    input.action == "delete_user_data"
    input.resource.classification == "PII"
    msg := "Destructive action on PII is not permitted."
}

### Example rule — require human approval for high-risk actions
human_approval_required[msg] {
    input.risk_score > 0.75
    msg := "Human approval is required for high-risk actions."
}

### Example rule — allow safe actions
allow {
    not deny[_]
    input.action in ["read_logs", "query_alerts"]
}

## B.4 Tool Definition Template (MCP-Compatible)

Ensures tools exposed to the planner are properly described and validated.

{
  "tool_name": "reset_password",
  "description": "Reset a user password in the identity platform.",
  "schema": {
    "type": "object",
    "properties": {
      "user_id": { "type": "string" },
      "reason": { "type": "string" }
    },
    "required": ["user_id"]
  },
  "credential_scope": "sp-helpdesk-reset",
  "risk_tier": "medium",
  "version": "1.0.0",
  "tool_id": "tool-reset-001",
  "tool_version_hash": "sha256:ab12cd34ef5678...",
  "approved_by": "sec-arch",
  "CAB_ticket": "CAB-2025-101",
  "timeout_ms": 3000,
  "dry_run_supported": true
}

## B.5 Sandbox Profile Template

Defines the isolation and blast-radius controls for Layer 6.

## Sandbox Profile — <System or Agent Name>

### 1. Environment Scope
- Tenant/subscription:
- Isolation boundary:
- Allowed networks:
- VNet/subnet restrictions:

### 2. Identity & Privilege Model
- Service principal:
- Assigned roles:
- Least-privilege analysis:

### 3. Runtime Security
- Container isolation type:
- Egress restrictions:
- Allowed registries:
- Ephemeral instance rule:

### 4. Controls & Enforcement
- Required policy engine decisions:
- Required log events:
- Required audit evidence:

### 5. Testing
- Egress tests:
- Privilege escalation checks:
- Drift tests:

## B.6 Multi-Agent Choreography Template

For Coordinator → Investigator → Remediator style systems.

## Multi-Agent Choreography — <System Name>

### 1. Agent Roles
- Coordinator:
- Investigator:
- Remediator:

### 2. Handoff Logic
- When Coordinator hands to Investigator:
- When Investigator escalates:
- When Remediator intervenes:

### 3. Shared Context Structure
- Required fields:
- Trace IDs:
- Evidence bundles:

### 4. Approval & Governance
- Escalation rules:
- HITL checkpoints:
- Policy engine verification:

### 5. Logging & Monitoring
- Required telemetry per handoff:
- Choreography drift detection:
