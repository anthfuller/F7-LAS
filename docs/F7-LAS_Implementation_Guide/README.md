F7-LAS Implementation Guide v3.1 — Documentation Index

This directory contains the enterprise-grade Implementation Guide for the
Fuller 7-Layer Agentic AI Security (F7-LAS) Framework.

The guide translates the conceptual model from the whitepaper into deployable engineering controls, including:

Layer-by-layer implementation requirements

Supply-chain hardening (Supplemental Layer S)

Model-security annex

Metrics, telemetry, and SLOs

Operational playbooks

RACI model

Engineering checklists

Reference architectures

Implementation profiles

All files are organized into modular Markdown components for clarity and maintainability.

Documentation Structure
00_Introduction.md

High-level overview of the guide: scope, audience, intended usage, and relationship to the F7-LAS whitepaper.

01_Control_Objectives.md

Core control objectives and control families aligned to all F7-LAS layers. Establishes the baseline for engineering and validation.

02_Layer_By_Layer_Controls.md

Detailed implementation requirements for Layers 1–7:
prompts → grounding → planner → tools → policy engine → sandbox → monitoring.

03_Supplemental_Layer_S.md

Supply-chain and software-integrity controls (SBOM, SCA gating, tool vetting, attestation).
A cross-cutting layer supporting all F7-LAS layers.

04_Model_Security_Annex.md

Model-level threats and mitigations: poisoning, evasion, extraction, unauthorized fine-tuning.
Connects model security considerations to the F7-LAS layers.

05_Metrics_and_SLOs.md

Measurable safety and reliability targets:
loop termination rates, retrieval trust scores, tool failure rates, telemetry completeness, and more.

06_Operational_Playbooks.md

Layer-aligned playbooks, including:
tool-misuse handling, RAG-poisoning triage, planner-loop runaway, policy-override detection, sandbox-containment procedures, telemetry drift analysis.

07_RACI_Model.md

Ownership mapping across teams (AI Platform, SecArch, MLOps, CloudSec, SOC, CAB).
Defines a Responsible / Accountable / Consulted / Informed matrix for each layer.

08_Implementation_Profiles.md

How to build a complete F7-LAS Implementation Profile:
component map, control mapping, telemetry schema, and multi-agent choreography patterns.

Appendices
Appendices/A_Schemas.md

Schemas for tools, planning logs, RAG events, policies, and telemetry fields.

Appendices/B_Templates.md

Templates for Implementation Profiles, Prompt Security Profiles (PSPs), CAB review forms, and more.

Appendices/C_Checklist.md

Full engineering checklist (imported from Engineering_Review_Checklist.md).
Used during design reviews, readiness checks, and pre-production assessment.

Appendices/D_Reference_Architectures.md

Secure multi-agent reference patterns, including:

Coordinator–Investigator–Remediator

Secure MCP tool gateway

Isolated Azure Container Apps patterns

RAG pipelines with trust scoring and Layer-5 enforcement

How to Use This Guide
Architects & Platform Engineers

Use:

02_Layer_By_Layer_Controls.md

03_Supplemental_Layer_S.md
to build secure agent runtimes.

Security / GRC Teams

Use:

01_Control_Objectives.md

07_RACI_Model.md

Appendices/C_Checklist.md
for governance, validation, and approvals.

SOC & IR Teams

Use:

06_Operational_Playbooks.md

04_Model_Security_Annex.md
to build detection and response workflows.

Developers

Use:

05_Metrics_and_SLOs.md

Appendices/A_Schemas.md
to implement measurable, observable agent systems.

Versioning

Current version: v3.1 (Enterprise Edition)
Aligned with:

F7-LAS Whitepaper v2.4

Weakness analyses (6.1, 6.2, 6.3, 6.3b)

Engineering Review Checklist

DevSecOps pipeline and CI tooling

Feedback & Contributions

For suggestions, issues, or contributions:

Open a GitHub Issue

Submit a Pull Request

Framework Author: Anthony Fuller

GitHub: https://github.com/anthfuller
