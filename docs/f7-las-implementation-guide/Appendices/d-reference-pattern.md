# Appendix D — Reference Patterns

This appendix provides vendor-neutral, security-centric reference patterns that implement the F7-LAS model in real systems.
Each pattern is aligned with the seven layers, the supplemental supply-chain layer, and the multi-agent governance model.

These are reference designs, not prescriptive requirements.

## D.1 Reference Patterns: Coordinator–Investigator–Remediator (CIR Model)

This is the most common multi-agent model for cybersecurity and operational automation.

### D.1.1 Overview

A three-agent model providing layered responsibility:

Coordinator — receives the task, breaks it into subtasks, enforces scoping.

Investigator — performs deep analysis and evidence gathering.

Remediator — executes approved actions behind a policy engine.

### D.1.2 Layer Mapping
F7-LAS Layer	CIR Implementation Example
Layer 1 — Prompt	Three separate PSP-governed prompts
Layer 2 — RAG	Investigator has privileged RAG access; Coordinator has filtered RAG
Layer 3 — Planner	Coordinator runs master plan; Investigator runs analysis plan
Layer 4 — Tools	Investigator: investigative tools; Remediator: action tools only
Layer 5 — Policy Engine	Remediator enforces PDP/PEP; Coordinator has read-only
Layer 6 — Sandbox	Each agent has isolated execution environment
Layer 7 — Monitoring	Unified telemetry across agents w/ shared trace IDs

### D.1.3 Security Benefits

Segregation of duties

Contained blast radius

Layer-aligned observability

Auditability through unified trace IDs

Prevents over-privileged single agents

D.2 Reference Pattern: Secure MCP Tool Gateway

A pattern for exposing enterprise tools through a mediated, risk-aware gateway instead of directly to the LLM.

### D.2.1 Components

MCP Gateway — validates tool schemas, enforces credential scopes

Policy Engine (Layer 5) — evaluates all tool requests

Tool Runtime Sandbox (Layer 6) — executes isolated tool actions

Telemetry Sink (Layer 7) — receives structured logs

### D.2.2 Flow

Planner generates an action.

MCP Gateway validates schema and assigns risk tier.

PDP evaluates request.

PEP enforces decision.

Tool runs in a sandbox.

Monitoring logs reason → action → result → drift signals.

### D.2.3 Why Use This Pattern

Strong tool isolation

Deterministic schema validation

Prevents tool-injection attacks

Supports multi-tenant model

Integrates cleanly with F7-LAS layers

## D.3 Reference Pattern: Azure Container Apps Isolated Sandbox

A cloud-native pattern consistent with your real use case.

### D.3.1 Components

Agent Runtime (Coordinator/Investigator/Remediator)

Per-agent Container Apps Environment

VNet-integrated sandbox

Ingress/egress controls

Key Vault for secrets

Policy Engine (OPA/Rego or Azure Policy)

Log Analytics / SIEM sink

### D.3.2 Layer Alignment

Layer 1–3: Running inside ACA containers

Layer 4: MCP tools exposed through gateway containers

Layer 5: OPA/Rego or Azure Policy in an adjacent service

Layer 6: ACA Isolated Environment (core of blast-radius control)

Layer 7: Logs → Azure Monitoring → SIEM

### D.3.3 Strengths

Strong network isolation

Predictable container lifecycle

Cloud-provider-native least-privilege

Secure supply-chain via container scanning

## D.4 Reference Pattern: Secure RAG Pipeline with Trust Scoring

This pattern ensures grounding is trustworthy, observable, and resistant to poisoning.

### D.4.1 Components

Embedding Service

Vector Store with trust metadata

Source validation pipeline

RAG retrieval service

Layer-5 gating for sensitive sources

Telemetry logging (Layer 7)

### D.4.2 Trust Scoring Model

Each retrieved document stores:

credibility_score

domain_score

recency_score

poisoning_flags (binary)

RAG calls log these fields and feed drift detection.

### D.4.3 Benefits

Resilient to poisoning

Supports provenance and audit

Enforces domain-restricted RAG

Strengthens Layer 2 observability

## D.5 Reference Pattern: SIEM-Integrated Agentic SOC Assistant

A practical pattern for enterprise SOC automation.

### D.5.1 Components

LLM-based Coordinator Agent

Investigator Agent with SIEM & EDR read-only tooling

Remediator Agent with tool-scoped keys

Policy Engine

SIEM / XDR data feeds

Stratified sandbox environments

### D.5.2 Layer Alignment

Layer 1: Prompt with SOC-specific PSP

Layer 2: RAG restricted to approved telemetry sources

Layer 3: Planning patterns tied to alert severity

Layer 4: Read-only investigative tools + high-risk actions gated

Layer 5: Risk-tier escalation rules

Layer 6: Per-agent environment isolation

Layer 7: Monitoring integrated with alert pipeline

### D.5.3 Outcomes

Faster triage without loss of control

Reduced false positives

SOC auditability and continuous assurance
