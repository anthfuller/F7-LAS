# F7-LAS Documentation

![F7-LAS CI](https://github.com/anthfuller/F7-LAS/actions/workflows/f7las-ci.yml/badge.svg?branch=main)

A multi-layer agentic security framework for governing, evaluating, and enforcing controls across AI agents, models, and orchestration pipelines.

# F7-LAS — Fuller 7-Layer Agentic AI Security Framework

![Version](https://img.shields.io/badge/version-v3.1-blue)
![License](https://img.shields.io/badge/license-Proprietary-lightgrey)
![CI](https://img.shields.io/github/actions/workflow/status/anthfuller/F7-LAS/f7las-ci.yml)

---

### TL;DR

**F7-LAS** (Fuller 7-Layer Agentic AI Security Framework) is a vendor-neutral, control-centric model for securing advanced agentic and multi-agent AI systems. It supports SOC, AI security architects, and governance teams working across real-world deployments.

📄 [Download the White Paper (v2.4)](docs/Security_Agentic_AI_The_7-Layer_Model_v2.4.pdf)

---

## 🌐 Overview

F7-LAS defines a layered control model for securing AI agents that can plan, reason, call tools, modify systems, and interact with enterprise environments.

It provides:
- A 7-layer control stack (L1–L7)
- A supplemental supply-chain layer (Layer S)
- A full implementation guide, patterns, controls, and engineering checklists
- A vendor-neutral reference architecture for multi-agent systems
- A DevSecOps pipeline enforcing prompt, tool, policy, and scenario integrity

**Status**: v3.1 — Conceptual model stable, with expanding implementation patterns, controls, and CI pipeline integration.

---

## What F7-LAS Covers

F7-LAS models agentic system security across seven layers:

1. **System Prompt (Soft Policy)**
2. **RAG / Grounding (Epistemic Guardrail)**
3. **Agent Planner / Controller**
4. **Tools & Integrations (Action Surface)**
5. **Policy Engine Outside the LLM (PDP/PEP Hard Guardrails)**
6. **Sandboxed Execution Environment (Blast Radius Control)**
7. **Monitoring, Evaluation & Assurance**

Additional components:
- **Layer S — Supply Chain Security (SBOM, SCA, attestation)**
- **Model Security Annex**
- Risk scoring, metrics, and SLOs
- Operational playbooks
- RACI model
- Implementation profiles

F7-LAS complements (but does not directly map to):
NIST AI RMF, ISO/IEC 42001, EU AI Act, MITRE ATT&CK, MITRE ATLAS

---

## 🗂 Repository Structure

```bash
F7-LAS/
├── README.md
├── LICENSE
├── requirements.txt
│
├── .github/
│   └── workflows/
│       └── f7las-ci.yml
│
├── scripts/
│   ├── validate-prompts.py
│   ├── validate_policies.py
│   ├── validate_settings.py
│   └── check_golden_thresholds.py
│
├── config/
│   ├── prompts/
│   │   ├── coordinator-agent-prompt-v1.txt
│   │   ├── investigator-agent-prompt-v1.txt
│   │   └── remediator-agent-prompt-v1.txt
│   │
│   ├── policies/
│   │   ├── model-policy-baseline.yaml
│   │   ├── agent-policy-baseline.yaml
│   │   └── data-policy-baseline.yaml
│   │
│   ├── settings.yaml
│   ├── psp-schema.json
│
├── docs/
│   ├── F7-LAS-Control-Catalog-v0.1.md
│   ├── Engineering-Review-Checklist.md
│   ├── Multi-Agent-F7-LAS-Architecture.png
│   │
│   ├── f7-las-implementation-guide/
│   │   ├── 00-introduction.md
│   │   ├── 01-control-objectives.md
│   │   ├── 02-layer-by-layer-controls.md
│   │   ├── 03-supplemental-layer-s.md
│   │   ├── 04-model-security-annex.md
│   │   ├── 05-metrics-and-slos.md
│   │   ├── 06-operational-playbooks.md
│   │   ├── 07-raci-model.md
│   │   ├── 08-implementation-profiles.md
│   │   └── appendices/
│   │       ├── a-schemas.md
│   │       ├── b-templates.md
│   │       ├── c-checklist.md
│   │       └── d-reference-architectures.md
│
├── src/
│   ├── core/
│   ├── agents/
│   ├── tools/
│   └── demo_runner/
│       └── run_golden_dataset.py
│
├── tests/
│   ├── golden_dataset/
│   │   ├── rubric.json
│   │   └── scenarios.json
│   │
│   └── test_agents_basic.py
│
└── examples/

```
---

## Quick Start

```bash
git clone https://github.com/anthfuller/F7-LAS.git
cd F7-LAS
python scripts/validate-prompts.py
```

See `demo-runner/` for sample agent orchestration.

---

## Usage Scenarios

- Embed F7-LAS into SOC workflows
- Secure AI-driven remediation agents
- Evaluate tool-call safety & sandboxing in production
- Align agent design to NIST AI RMF, ISO/IEC 42001, and EU AI Act

---

## How to Cite

If referencing this work in research or policy:

> Fuller, A. (2025). *Security for Agentic AI: The F7-LAS Framework for Multi-Layer Controls.* [https://github.com/anthfuller/F7-LAS](https://github.com/anthfuller/F7-LAS)

---

## Contributing

Contributions welcomed — scenarios, policies, controls, tooling, and improvements.

Please open an issue before major changes.

---

## License & Disclaimer

© 2025 Anthony L. Fuller. All rights reserved.

#### This work is created independently by the author and is not affiliated with, endorsed by, or associated with Microsoft or any other employer. Opinions and materials represent the author’s personal work.
