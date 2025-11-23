F7-LAS Implementation Guide v3.1 — Documentation Index

This directory contains the enterprise-grade, NIST-style Implementation Guide for the
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

All files are organized into modular Markdown components for maximum clarity and maintainability.

Documentation Structure
00_Introduction.md

High-level overview of the guide: scope, audience, usage recommendations, and relationship to the F7-LAS whitepaper.

01_Control_Objectives.md

Defines the core control objectives and control families across all F7-LAS layers.
Establishes the foundation for engineering and validation.

02_Layer_By_Layer_Controls.md

Detailed implementation requirements for Layers 1–7:
prompts → grounding → planner → tools → policy engine → sandbox → monitoring.

03_Supplemental_Layer_S.md

Supply-chain and software-integrity controls (SBOM, SCA gating, tool vetting, attestation).
A cross-cutting layer applied across all levels of the system.

04_Model_Security_Annex.md

Model-level threats and mitigations: poisoning, evasion, extraction, unauthorized fine-tuning.
Connects model security to F7-LAS layers.

05_Metrics_and_SLOs.md

Defines measurable safety & reliability targets:
loop termination, retrieval trust scores, tool failure rates, telemetry completeness, and more.

06_Operational_Playbooks.md

Practical playbooks aligned with F7-LAS layers:
tool misuse, RAG poisoning, planner runaway, policy overrides, telemetry drift, etc.

07_RACI_Model.md

Ownership across teams (AI Platform, SecArch, MLOps, CloudSec, SOC, CAB).
Defines Responsible / Accountable / Consulted / Informed matrix per layer.

08_Implementation_Profiles.md

How to build a complete F7-LAS Implementation Profile for your environment.
Includes component mapping, control mappings, telemetry schema, and multi-agent choreography patterns.

Appendices
Appendices/A_Schemas.md

Schemas for tools, planning logs, RAG events, policy decisions, and telemetry fields.

Appendices/B_Templates.md

Templates for Implementation Profiles, PSPs (Prompt Security Profiles), CAB review forms, and more.

Appendices/C_Checklist.md

Full engineering checklist (imported from Engineering_Review_Checklist.md).
Used during design reviews, readiness checks, and pre-production assessments.

Appendices/D_Reference_Architectures.md

Secure multi-agent reference patterns, including:

Coordinator–Investigator–Remediator

Secure MCP tool gateway

Azure Container Apps isolated environment patterns

RAG pipelines with trust scoring and Layer 5 enforcement

🔧 How to Use This Guide
Architects & Platform Engineers

Use 02_Layer_By_Layer_Controls.md + 03_Layer_S to build secure agent runtimes.

Security / GRC Teams

Use 01_Control_Objectives.md + 07_RACI_Model.md + C_Checklist.md
to validate deployments and assign operational ownership.

SOC & IR Teams

Use 06_Operational_Playbooks.md + 04_Model_Security_Annex.md
to build detection rules and response procedures.

Developers

Use 05_Metrics_and_SLOs.md + A_Schemas.md
to produce measurable, instrumented agentic systems.

Versioning

Current version: v3.1 (Enterprise Edition)
Aligned with:

F7-LAS Whitepaper v2.4

Weakness analyses (6.1, 6.2, 6.3, 6.3b)

Engineering Review Checklist

DevSecOps pipeline and CI tooling

Feedback & Contributions

For suggestions, issues, or contributions:

- Open a GitHub Issue
- Submit a PR
- Framework Author: **Anthony Fuller**
- GitHub: https://github.com/anthfuller
