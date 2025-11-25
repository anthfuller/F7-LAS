# F7-LAS Control Catalog v0.1

**Purpose**  
This catalog defines a set of **concrete, testable security controls** for agentic AI systems, organized by the **F7-LAS (Fuller 7-Layer Agentic AI Security)** model.

F7-LAS does **not** claim to be a formal profile or mapping of NIST, ISO, or other standards.  
Instead, these controls are designed to **complement** existing frameworks (e.g., NIST AI RMF, ISO/IEC 42001/23894, MITRE ATLAS) and to provide **agent-specific** guardrails where those standards are currently high-level or silent.

Use this catalog to:

- Design and review agentic AI architectures
- Drive implementation and CI/CD enforcement
- Support internal risk assessments, audits, and governance

**Control ID format:** `F7-L<layer>-NN` (e.g., `F7-L4-02`)

---

## Layer 1 – System Prompt (Soft Policy)

**Intent:** Define agent roles, scope, and safety posture *in text*, under change control.  
Prompts are **soft controls** and must be treated as such, but they are still a primary surface where risk can be shaped.

### F7-L1-01 – Prompt Version Control

- **Control:**  
  All production system prompts **SHALL** be stored in a version-controlled repository or configuration store with history and access controls.
- **Implementation Notes:**  
  - Store prompts under `config/prompts/` in Git.  
  - Protect the branch used for production prompts.  
- **Evidence:**  
  - Git history showing commits to prompt files.  
  - Branch protection rules/screenshots.

---

### F7-L1-02 – Role & Scope Definition

- **Control:**  
  Each agent’s system prompt **SHALL** explicitly define the agent’s role (e.g., Coordinator, Investigator, Remediator) and operational scope.
- **Implementation Notes:**  
  - Use structured metadata at the top of each prompt (role, scope, risk level). :contentReference[oaicite:0]{index=0}  
- **Evidence:**  
  - Prompt file content with clear role/scope sections.  

---

### F7-L1-03 – Prohibited Actions

- **Control:**  
  System prompts **SHALL** explicitly state *disallowed actions* (e.g., no direct remediation, no changes to production, no policy overrides).
- **Implementation Notes:**  
  - Include “MUST NOT” clauses for destructive or privileged actions.  
- **Evidence:**  
  - Prompt text showing explicit prohibitions.

---

### F7-L1-04 – Abstain & Escalate Behavior

- **Control:**  
  System prompts **SHALL** define when the agent must **abstain** and when to **escalate to a human**, including uncertainty, scope violation, or high-risk actions.
- **Implementation Notes:**  
  - Embed escalation rules (e.g., “If requested to isolate host, escalate to human approver”).  
- **Evidence:**  
  - Prompt sections describing abstain/escalate.

---

### F7-L1-05 – Prompt Change Control

- **Control:**  
  Changes to production system prompts **SHALL** follow a documented change-control process (review and approval by an authorized role).
- **Implementation Notes:**  
  - Require PRs with at least one security/architecture approver.  
- **Evidence:**  
  - PRs showing review/approval for prompt changes.

---

### F7-L1-06 – Prompt Security Testing

- **Control:**  
  System prompts **SHALL** undergo periodic **prompt-injection and jailbreak testing**, with findings tracked and mitigations implemented.
- **Implementation Notes:**  
  - Integrate basic tests into CI and periodic manual or automated red-teaming. :contentReference[oaicite:1]{index=1}  
- **Evidence:**  
  - Test results/red-team reports.  
  - Issues or tickets tracking mitigations.

---

## Layer 2 – Grounding / RAG (Epistemic Guardrail)

**Intent:** Ensure retrieved context is **curated, access-controlled, and treated as untrusted**. RAG reduces epistemic risk, but is not a hard boundary.

### F7-L2-01 – RAG Source Inventory

- **Control:**  
  All RAG sources (indexes, knowledge bases, APIs) **SHALL** be enumerated and documented, including owners and classification.
- **Implementation Notes:**  
  - Maintain a `rag_sources` registry or configuration.  
- **Evidence:**  
  - RAG inventory document/config.

---

### F7-L2-02 – Access-Controlled RAG Gateway

- **Control:**  
  Retrieval for agent prompts **SHALL** be performed via a controlled **RAG gateway**, not direct access to raw storage or vector DBs.
- **Implementation Notes:**  
  - Gateway applies auth, rate limiting, source allowlists, and logging. :contentReference[oaicite:2]{index=2}  
- **Evidence:**  
  - Architecture docs showing the gateway.  
  - Logs of retrieval calls.

---

### F7-L2-03 – Curation & Retirement Process

- **Control:**  
  There **SHALL** be a process to **curate, update, and retire** RAG content, including removal of stale or risky material.
- **Implementation Notes:**  
  - Scheduled reviews, owner approvals for new or changed content.  
- **Evidence:**  
  - Change logs for content updates.  
  - Governance records.

---

### F7-L2-04 – Poisoning Defenses

- **Control:**  
  Controls **SHALL** exist to detect and prevent **RAG poisoning**, including restricted authorship and validation for high-impact content.
- **Implementation Notes:**  
  - Source trust scoring, ingestion validation pipelines, or manual review for critical sources. :contentReference[oaicite:3]{index=3}  
- **Evidence:**  
  - Ingestion policies, validation scripts, access lists.

---

### F7-L2-05 – Treat Retrieved Content as Untrusted

- **Control:**  
  Retrieved content **SHALL** be treated as **untrusted input**; the system SHALL NOT execute instructions from retrieved content without passing through policies and tooling.
- **Implementation Notes:**  
  - No direct “eval” or command execution based on retrieved text.  
- **Evidence:**  
  - Code review showing no unsafe execution paths.

---

### F7-L2-06 – RAG Injection Testing

- **Control:**  
  The RAG pipeline **SHALL** be tested for **prompt injection via retrieved text**, with mitigations applied where necessary.
- **Implementation Notes:**  
  - Inject adversarial payloads into test indexes and evaluate agent behavior.  
- **Evidence:**  
  - Test records, evaluation outputs, tracked fixes.

---

## Layer 3 – Agent Planner / Controller

**Intent:** Bound and observe the agent’s planning/decision loops, including multi-agent delegation.

### F7-L3-01 – Planner Identification

- **Control:**  
  The main planning/control component(s) (e.g., supervisor, router, coordinator) **SHALL** be explicitly identified in architecture documentation.
- **Implementation Notes:**  
  - Document planner location (e.g., LangGraph graph node, custom orchestrator).  
- **Evidence:**  
  - Architecture diagram, component docs.

---

### F7-L3-02 – Planning Contracts

- **Control:**  
  Each agent **SHALL** have a **planning contract** specifying `max_steps`, `max_tool_calls`, `max_duration_seconds`, and allowed tool set. :contentReference[oaicite:4]{index=4}  
- **Implementation Notes:**  
  - Store contracts as config, enforce at runtime in the orchestrator.  
- **Evidence:**  
  - Planning contract config.  
  - Logs showing enforcement.

---

### F7-L3-03 – Bounded Reason–Act Loops

- **Control:**  
  The planner **SHALL** enforce upper bounds on loop count, recursion depth, and wall-clock time for each task.
- **Implementation Notes:**  
  - Implement counters and timeouts; log termination reason (success, limit reached, error).  
- **Evidence:**  
  - Runtime logs, test cases hitting limits.

---

### F7-L3-04 – Explicit Stop Conditions

- **Control:**  
  Planner logic **SHALL** implement explicit stop conditions (success, failure, timeout, escalation) and record which one was used.
- **Implementation Notes:**  
  - Define termination states in code or graph nodes.  
- **Evidence:**  
  - State machine definition, logs.

---

### F7-L3-05 – Delegation Rules for Multi-Agent

- **Control:**  
  In multi-agent setups, **delegation rules** (who may call whom, and for what) **SHALL** be documented and enforced.
- **Implementation Notes:**  
  - Coordinator → Investigator → Remediator pattern with allowed transitions. :contentReference[oaicite:5]{index=5}  
- **Evidence:**  
  - Governance doc and code enforcing allowed delegation.

---

### F7-L3-06 – Planner Telemetry

- **Control:**  
  Planner outputs and decisions **SHALL** be logged for later analysis, including selected tools, paths, and reasons where available.
- **Implementation Notes:**  
  - Emit `plan_event` telemetry as described in the implementation guide. :contentReference[oaicite:6]{index=6}  
- **Evidence:**  
  - Telemetry samples, SIEM dashboards.

---

### F7-L3-07 – Goal/Role Drift Testing

- **Control:**  
  Planner behavior **SHALL** be tested for **goal/role drift**, including adversarial tasks that attempt to push the agent out of scope.
- **Implementation Notes:**  
  - Include drift scenarios in golden dataset tests. :contentReference[oaicite:7]{index=7}  
- **Evidence:**  
  - Test scenarios, results, tracked remediations.

---

## Layer 4 – Tools & Integrations (Action Surface)

**Intent:** Clearly define and control the agent’s actuators; enforce least privilege and risk tiering.

### F7-L4-01 – Tool Catalog

- **Control:**  
  All tools/APIs/connectors callable by agents **SHALL** be listed in a **tool catalog** with owners, risk tiers, and descriptions.
- **Implementation Notes:**  
  - Maintain as YAML/JSON or DB; expose via Tool Gateway. :contentReference[oaicite:8]{index=8}  
- **Evidence:**  
  - Tool catalog artifact.

---

### F7-L4-02 – Tool Risk Tiering

- **Control:**  
  Each tool **SHALL** be assigned a **risk tier** (e.g., Tier 1: read-only; Tier 2: limited writes; Tier 3: high-impact writes).
- **Implementation Notes:**  
  - Persist risk tier in the tool definition schema. :contentReference[oaicite:9]{index=9}  
- **Evidence:**  
  - Catalog entries with risk_tier field.

---

### F7-L4-03 – Read/Write Separation

- **Control:**  
  Read-only tools **SHALL** be separated from write-capable tools logically and, where feasible, by identity/permissions.
- **Implementation Notes:**  
  - Use different roles/credentials for read vs. write tools.  
- **Evidence:**  
  - IAM policies, tool configs.

---

### F7-L4-04 – Least-Privilege Tool Permissions

- **Control:**  
  Tool identities/credentials **SHALL** be scoped to the **minimum necessary** permissions for their documented function.
- **Implementation Notes:**  
  - Managed identities with narrowly scoped roles.  
- **Evidence:**  
  - IAM role definitions, access review reports.

---

### F7-L4-05 – Agent-to-Tool Access Control

- **Control:**  
  Each agent **SHALL** have access only to the **subset of tools** needed for its role, as defined in the planning contract or configuration.
- **Implementation Notes:**  
  - Enforce allowed_tools in runtime.  
- **Evidence:**  
  - Config, runtime checks, logs.

---

### F7-L4-06 – Tool Argument Validation

- **Control:**  
  Tool inputs **SHALL** be validated against schemas before execution to prevent misuse, injection, or malformed operations.
- **Implementation Notes:**  
  - Use Pydantic/JSON schema for validation as in the implementation guide. :contentReference[oaicite:10]{index=10}  
- **Evidence:**  
  - Validation code, failing tests for bad input.

---

### F7-L4-07 – Tool Call Telemetry

- **Control:**  
  All tool calls **SHALL** be logged, including agent identity, tool ID, high-level parameters (sanitized/redacted where needed), and result.
- **Implementation Notes:**  
  - Emit `tool_call` telemetry events per call. :contentReference[oaicite:11]{index=11}  
- **Evidence:**  
  - Telemetry samples, SIEM dashboards.

---

### F7-L4-08 – HITL for Tier-3 Tools

- **Control:**  
  Tier-3 (high-impact) tools **SHALL** require human-in-the-loop approval before execution.
- **Implementation Notes:**  
  - Use workflow systems, approval tokens, or explicit PDP obligations. :contentReference[oaicite:12]{index=12}  
- **Evidence:**  
  - Workflow logs, PDP decision logs with HITL.

---

## Layer 5 – Policy Engine Outside the LLM (PDP/PEP)

**Intent:** Hard-enforce policies for high-impact actions in an external, testable component.

### F7-L5-01 – External PDP/PEP Architecture

- **Control:**  
  High-impact actions **SHALL** be mediated by an **external PDP/PEP**, not solely by the LLM or prompt instructions.
- **Implementation Notes:**  
  - Use an OPA/REGO service or custom PDP with PEP wrappers on tool gateways. :contentReference[oaicite:13]{index=13}  
- **Evidence:**  
  - Architecture diagrams, PDP service code.

---

### F7-L5-02 – Policy-as-Code

- **Control:**  
  Policies **SHALL** be defined as code or structured configuration in a version-controlled repository.
- **Implementation Notes:**  
  - YAML/JSON/REGO policy files with CI validation.  
- **Evidence:**  
  - Policy repo, CI logs for policy tests.

---

### F7-L5-03 – Decision Outcomes

- **Control:**  
  The PDP **SHALL** support at least: **Allow, Deny, Allow with Obligations, Escalate to Human**.
- **Implementation Notes:**  
  - Responses with decision + obligations (e.g., additional logging, HITL requirement).  
- **Evidence:**  
  - PDP API/schema, sample decisions.

---

### F7-L5-04 – Tiered Policy Enforcement

- **Control:**  
  Tier-2 and Tier-3 tools **SHALL** always be evaluated by the PDP, with stricter conditions and obligations for Tier-3.
- **Implementation Notes:**  
  - Routing logic in PEP based on tool risk_tier.  
- **Evidence:**  
  - Code paths, test cases for Tier-3 enforcement.

---

### F7-L5-05 – Policy Change Management

- **Control:**  
  Changes to policies **SHALL** undergo review, testing, and approval before deployment to production.
- **Implementation Notes:**  
  - Enforce PR review, CI policy tests, and CAB sign-off for critical changes. :contentReference[oaicite:14]{index=14}  
- **Evidence:**  
  - PRs/approvals, CAB records.

---

### F7-L5-06 – PDP/PEP Telemetry

- **Control:**  
  All PDP decisions and PEP enforcement outcomes **SHALL** be logged for audit and incident response.
- **Implementation Notes:**  
  - Emit `policy_decision` events with decision, subject, action, resource, context. :contentReference[oaicite:15]{index=15}  
- **Evidence:**  
  - Telemetry samples, query examples.

---

## Layer 6 – Sandboxed Execution Environment

**Intent:** Constrain the blast radius of agents via network, identity, environment, and resource isolation.

### F7-L6-01 – Segmented Runtime Environment

- **Control:**  
  Agent runtimes **SHALL** execute in a segmented environment (e.g., separate tenant/subscription/account) with clear boundaries from critical production systems.
- **Implementation Notes:**  
  - Use dedicated accounts/subscriptions/VPCs. :contentReference[oaicite:16]{index=16}  
- **Evidence:**  
  - Cloud resource layout, network diagrams.

---

### F7-L6-02 – Network Egress Controls

- **Control:**  
  Network egress from the agent environment **SHALL** be restricted to approved destinations via VNET/VPC rules, firewalls, and/or private endpoints.
- **Implementation Notes:**  
  - Allowlist patterns (e.g., specific internal APIs only).  
- **Evidence:**  
  - Firewall rules, security group configs.

---

### F7-L6-03 – Environment Separation (Read vs Remediate)

- **Control:**  
  Where security actions are involved, **read-only investigation** and **write-capable remediation** environments **SHALL** be separated.
- **Implementation Notes:**  
  - Different sandboxes or identity profiles for investigative vs. remediation tasks. :contentReference[oaicite:17]{index=17}  
- **Evidence:**  
  - Separate environment/config descriptions.

---

### F7-L6-04 – Identity Per Agent / Sandbox

- **Control:**  
  Each agent (and ideally each sandbox) **SHALL** have a distinct identity or role with clearly defined permissions.
- **Implementation Notes:**  
  - Map Coordinator/Investigator/Remediator to different IAM roles.  
- **Evidence:**  
  - IAM role configs, access reviews.

---

### F7-L6-05 – Sandbox Profile Definitions

- **Control:**  
  Sandbox profiles **SHALL** be defined (e.g., CPU/memory limits, timeouts, filesystem access, network allowlists) and applied consistently.
- **Implementation Notes:**  
  - Use structured `sandbox_profile` schema as in the implementation guide. :contentReference[oaicite:18]{index=18}  
- **Evidence:**  
  - Sandbox config files, runtime enforcement logs.

---

### F7-L6-06 – Ephemeral Sandboxes

- **Control:**  
  Sandboxes **SHALL** be ephemeral per task or session, and destroyed after completion.
- **Implementation Notes:**  
  - Automate tear-down on task completion; monitor for orphaned environments.  
- **Evidence:**  
  - Logs showing sandbox creation/destruction.

---

### F7-L6-07 – Blast Radius Statement

- **Control:**  
  A documented **blast radius statement** **SHALL** exist describing worst-case impact if the agent misbehaves within its sandbox.
- **Implementation Notes:**  
  - Use in risk acceptance and architecture decisions.  
- **Evidence:**  
  - Risk documentation, sign-off records.

---

## Layer 7 – Monitoring, Evaluation & Assurance

**Intent:** Provide visibility into agent behavior and continuous assurance via telemetry, evaluations, and red-teaming.   

### F7-L7-01 – Unified Telemetry Schema

- **Control:**  
  A **unified telemetry schema** **SHALL** exist covering events such as `prompt_event`, `rag_retrieval`, `plan_event`, `tool_call`, `policy_decision`, `sandbox_lifecycle`, `evaluation_event`.
- **Implementation Notes:**  
  - Implement as a shared schema across components.  
- **Evidence:**  
  - Schema definition, sample logs.

---

### F7-L7-02 – Central Telemetry Ingestion

- **Control:**  
  Agent telemetry **SHALL** be ingested into a central monitoring platform (e.g., SIEM/XDR) for correlation and alerting.
- **Implementation Notes:**  
  - Use log pipelines, normalizers, and dashboards.  
- **Evidence:**  
  - SIEM connectors, dashboards.

---

### F7-L7-03 – Detection Rules for Agent Misuse

- **Control:**  
  Detection rules **SHALL** exist for anomalous agent behavior (e.g., spikes in denied actions, unusual tool usage, policy violations).
- **Implementation Notes:**  
  - Use ATLAS-inspired and use-case-specific detections.  
- **Evidence:**  
  - Detection rule definitions, alert histories.

---

### F7-L7-04 – Golden Dataset Evaluation

- **Control:**  
  The system **SHALL** be evaluated against a **golden dataset** of scenarios and rubrics, with thresholds enforced in CI/CD.
- **Implementation Notes:**  
  - Use `run_golden_dataset` + `check_golden_thresholds` as in the DevSecOps pipeline. :contentReference[oaicite:20]{index=20}  
- **Evidence:**  
  - CI logs, evaluation reports.

---

### F7-L7-05 – Red-Team & Adversarial Testing

- **Control:**  
  Periodic red-team exercises **SHALL** be run against the agent, including prompt injection, RAG poisoning, tool misuse, and sandbox escape attempts.
- **Implementation Notes:**  
  - Track findings and tie them back to updates in prompts, policies, sandboxing. :contentReference[oaicite:21]{index=21}  
- **Evidence:**  
  - Red-team reports, change logs.

---

### F7-L7-06 – SLOs for Agent Safety

- **Control:**  
  Explicit **SLOs** (service level objectives) **SHALL** be defined for safety metrics (e.g., drift detection MTTD, rate of blocked high-risk actions).
- **Implementation Notes:**  
  - Use per-layer SLOs as in the implementation guide. :contentReference[oaicite:22]{index=22}  
- **Evidence:**  
  - SLO docs, metric dashboards, periodic review notes.

---

## Supplemental Layer S – Software Supply Chain & Framework Security

**Intent:** Address risks in the **agent frameworks, libraries, and dependencies** themselves, not just the agent behavior.

### F7-LS-01 – SBOM Generation

- **Control:**  
  An SBOM (Software Bill of Materials) **SHALL** be generated for agent runtime dependencies and kept up to date.
- **Implementation Notes:**  
  - Integrate SBOM generation into CI (e.g., in `f7las-ci.yml`). :contentReference[oaicite:23]{index=23}  
- **Evidence:**  
  - SBOM artifacts.

---

### F7-LS-02 – Dependency Vulnerability Scanning

- **Control:**  
  Dependencies **SHALL** be scanned for known vulnerabilities; builds **SHALL** be blocked for critical issues affecting agent runtime or tools.
- **Implementation Notes:**  
  - SCA tooling in CI; thresholds for failing the build. :contentReference[oaicite:24]{index=24}  
- **Evidence:**  
  - SCA reports, CI logs showing failed builds on critical findings.

---

### F7-LS-03 – Framework Version Pinning

- **Control:**  
  Agent frameworks and critical libraries **SHALL** be version-pinned, with changes controlled and tested.
- **Implementation Notes:**  
  - Use explicit versions in `requirements.txt` / lockfiles.  
- **Evidence:**  
  - Dependency manifests, PRs for version changes.

---

### F7-LS-04 – Plugin & Tool Framework Governance

- **Control:**  
  Third-party plugins/tools **SHALL** go through a review process prior to being enabled for agents, with risk assessment and owner assignment.
- **Implementation Notes:**  
  - Similar governance to introducing a new Tier-2/3 tool.  
- **Evidence:**  
  - Plugin review records, approvals.

---

### F7-LS-05 – Framework Telemetry & Attestation

- **Control:**  
  Telemetry **SHALL** capture framework/runtime version identifiers, and where feasible, build attestation IDs (e.g., sbom_id).
- **Implementation Notes:**  
  - Include `framework_version` and `sbom_id` fields in telemetry events. :contentReference[oaicite:25]{index=25}  
- **Evidence:**  
  - Telemetry samples, attestation records.

---

## Using This Catalog

- Treat this catalog as a **living document** for F7-LAS-compliant systems.
- Not every control will apply in every deployment; mark N/A where justified.
- For each applicable control:
  - Decide if it is **Implemented**, **Planned**, or **Accepted Risk**.
  - Capture **evidence** and **owners**.
- Combine this catalog with:
  - The **F7-LAS Whitepaper** (model)  
  - The **Implementation Guide v3.0**  
  - The **Engineering Review Checklist**  
  - The **DevSecOps Pipeline** (CI enforcement)

Together, they define a full lifecycle for designing, implementing, and assuring secure agentic AI systems.

© 2025 Anthony L. Fuller. All rights reserved.

#### This work is created independently by the author and is not affiliated with, endorsed by, or associated with Microsoft or any other employer. All opinions,
#### models, and materials represent the author's personal work.


