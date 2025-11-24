# Appendix C — Engineering Review Checklist

This appendix links to the canonical F7-LAS Engineering Review Checklist, used for architecture reviews, readiness checks, and pre-production validation.
It ensures every agentic system is evaluated consistently across all seven layers.

➡️ **Open the full checklist here:**  
[Engineering-Review-Checklist.md](../../Engineering-Review-Checklist.md)
## C.1 Purpose

The Engineering Review Checklist provides a structured method for verifying that an agent or multi-agent system complies with the F7-LAS layered control model.
It is used during:

Design and architecture reviews

Pre-deployment readiness checks

Post-incident corrective review

Material change assessments

## C.2 How to Use

For each control, mark: Yes / Partial / No / N/A.

Capture all remediation actions with owners and due dates.

Attach the completed checklist to internal evidence sources (GitHub Issues, Azure Boards, Jira, ADRs, risk assessments).

Review this checklist together with the Control Catalog and Layer-by-Layer Controls.

## C.3 Checklist Scope

> **🧠 Note on Multi-Agent Systems**  
> F7-LAS assumes environments where agents may delegate tasks, escalate decision contexts,  
> or issue tool calls on behalf of other agents. This multi-agent choreography introduces unique  
> security and observability challenges.  
>
> Specific controls are defined in the companion Engineering Review Checklist (items MA.1–MA.5),  
> which include: delegated trust enforcement, traceability across agent boundaries, separation of duties,  
> and cross-agent telemetry correlation.  
>
> 🔗 [See Multi-Agent Controls in the Checklist →](../../Engineering-Review-Checklist.md)


The checklist covers:

Layer 1 — System Prompt

Layer 2 — RAG / Grounding

Layer 3 — Planner / Controller

Layer 4 — Tools & Integrations

Layer 5 — Policy Engine (PDP/PEP)

Layer 6 — Sandboxed Execution Environment

Layer 7 — Monitoring & Evaluation

Multi-Agent Governance (if applicable)

This appendix does not duplicate the checklist — it provides structure around it and links to the authoritative version.

## C.4 Advanced Review Add-On (Optional)

For high-assurance deployments (security operations, financial systems, regulated workloads), reviewers may include:

## C.4.1 Drift & Regression Checks

Prompt drift analysis

RAG dataset drift review

Planner loop regression tests

Tool-permission deltas

Sandbox permission-widening detection

## C.4.2 Adversarial Testing Requirements

MITRE ATLAS coverage

Prompt injection tests

Tool-abuse simulations

RAG-poisoning attack tests

PDP bypass attempts

## C.4.3 Compliance Integration

Attach results to CAB review artifacts

Link to System Security Plan (SSP) or internal equivalents

Validate evidence for internal audit

## C.5 Versioning

This appendix always links to the canonical checklist stored at:

/Engineering-Review-Checklist.md


The Implementation Guide should not rewrite the checklist; it references the source of truth so updates can be tracked independently.

### C.6 Copyright Notice

© 2025 Anthony L. Fuller. All rights reserved.
This work is independent of Microsoft and does not represent the views of any employer.
