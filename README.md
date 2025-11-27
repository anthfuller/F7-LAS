# F7-LAS™ — Fuller 7-Layer Agentic AI Security Framework

*A layered, control-centric security architecture for agentic and multi-agent AI systems.*

![CI](https://github.com/anthfuller/F7-LAS/actions/workflows/f7las-ci.yml/badge.svg)
![status](https://img.shields.io/badge/status-passing-brightgreen)
![version](https://img.shields.io/badge/version-v3.1-blue)
![license](https://img.shields.io/badge/license-CC%20BY%204.0-blue)
![maturity](https://img.shields.io/badge/maturity-Stage%200%20%E2%80%94%20Conceptual-yellow)

> **Maturity roadmap:**
> F7-LAS is currently at Stage 0 – Conceptual. The core runtime components (agents, tools, orchestration, and controller logic) are not yet implemented in this repository.
> The current focus is on the conceptual model, control layers, prompts, policies, schemas, and CI scaffolding. Future stages will introduce example agents, hardened CI, golden datasets, reference implementations, and operational playbooks.


### F7-LAS Maturity Stages

| Stage | Label                     | Description                                     | Use Readiness            |
|-------|---------------------------|-------------------------------------------------|--------------------------|
| 0     | Experimental              | Design, scaffolding, early controls and docs.   | Evaluation, learning, PoC |
| 1     | Alpha                     | Core logic working end-to-end with gaps.        | Internal sandbox only     |
| 2     | Beta                      | CI + tests in place, coverage improving.        | Controlled pilot / lab    |
| 3     | Stable                    | Versioned, test-covered, documented patterns.   | Production-ready          |

F7-LAS is intentionally **opinionated** and will move through these stages as the implementation guide, control catalog, golden datasets, and CI hardening mature.

## 🌐 Overview
F7-LAS (Fuller 7-Layer Agentic AI Security Framework) defines a **layered control model** for securing AI agents that can plan, reason, call tools, modify systems, and interact with enterprise environments.

It provides:
- A **7-layer control stack** (L1–L7)
- A **supplemental supply-chain layer (Layer S)**
- A **full implementation guide**, patterns, controls, and engineering checklists
- A **vendor-neutral reference architecture**
- A **CI-driven DevSecOps pipeline**

> **Status:** v3.1 — Conceptual model stable, active engineering expansion.

---

## What F7-LAS Covers
F7-LAS secures agentic systems through seven layers:

1. **System Prompt (Soft Policy)**
2. **RAG / Grounding (Epistemic Guardrail)**
3. **Agent Planner / Controller**
4. **Tools & Integrations (Action Surface)**
5. **External Policy Engine (Hard Guardrails)**
6. **Sandboxed Execution / Blast Radius Control**
7. **Monitoring, Evaluation & Drift Detection**

Plus:
- **Layer S — Supply Chain Security**
- **Model Security Annex**
- **Metrics/SLO Suite**
- **RACI Model**
- **Operational Playbooks**


---


## Repository Structure

```text
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
│   ├── check_golden_thresholds.py
│   ├── validate-policies.py
│   ├── validate-prompts.py
│   └── validate-settings.py
│
├── docs/
│   ├── Security-Agentic-AI-The-7-Layer-Model-v2.4.pdf
│   ├── F7-LAS-Implementation-Guide/
│   │   ├── 00-introduction.md
│   │   ├── 01-control-objectives.md
│   │   ├── 02-layer-by-layer-controls.md
│   │   ├── 03-suppplemental-layer-s.md
│   │   ├── 04-model-security-annex.md
│   │   ├── 05-metrics-and-slos.md
│   │   ├── 06-operational-playbooks.md
│   │   ├── 07-raci-model.md
│   │   ├── 08-implementation-profiles.md
│   │   └── appendices/
│   │       ├── a-schemas.md
│   │       ├── b-templates.md
|   |       ├── c-checklist.md
│   │       └── d-reference-architectures.md
│   │      
│   │
│   ├── Engineering-Review-Checklist.md
│   ├── F7-LAS-Control-Catalog-v0.1.md
│   ├── Multi-Agent-F7-LAS_Architecture-v1.png
|   ├── README.md
|   └── f7-las-whitepaper.pdf
│
├── config/
│   ├── prompts/
│   ├── policies/
│   └── settings.yaml
│
├── src/
│   ├── agents/
│   ├── core/
│   ├── demo_runner/
│   └── tools/
│
├── tests/
│   ├── golden_dataset/
│   │   ├── golden_eval_results.json
│   │   ├── rubric.json
│   │   └── scenariojson
│   └── test_agents_basic.py
│
└── examples/
│   ├── README.md
│   ├── basic_agent_flow.md
│   ├── demo_system_prompt.txt
│   ├── policy_enforced_tool_call.md
│   ├── simple_rag_query.md
│   ├── simple_rag_readonly.md
│   ├── walkthrough_false_positive.md
│   ├── walkthrough_false_positive.md
    └── walkthrough_ransomware_case.md
```

---

## Tooling & CI Pipeline

**GitHub Actions Workflow:** `.github/workflows/f7las-ci.yml`

Enforces:
- Prompt validation (Layer 1 PSP compliance)
- Policy validation (Layer 5)
- Settings validation (Layer 3 safety)
- Golden dataset scoring (Layer 7)
- Unit tests
- Optional linting & SBOM/SCA

---

## Quickstart

```bash
git clone https://github.com/<your-org>/F7-LAS.git
cd F7-LAS

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run tests:

```bash
pytest -q tests/test_agents_basic.py
```

Run the golden evaluator:

```bash
python scripts/check_golden_thresholds.py golden_eval_results.json
```

---

## Included Artifacts

**Engineering**
- Full modular implementation guide  
- Layer-by-layer controls  
- Metrics & SLOs  
- RACI model  
- Operational playbooks  

**Security**
- Prompt Security Profile schema  
- Policy validation  
- Sandbox rules  
- Drift detection & evaluation logic  

**Development**
- Example demo runner  
- Placeholder tests  
- CI workflow and validators  

---
## Roadmap

F7-LAS is evolving through clearly defined maturity stages to ensure transparency, stability, and long-term governance.

### Current Maturity Stage

![maturity](https://img.shields.io/badge/maturity-Stage%200%20%E2%80%94%20Experimental-yellow)

F7-LAS is currently **Stage 0 — Experimental**.  
The framework structure, control catalog, prompt standards, and initial CI validation are in place, with additional hardening and functional components planned.

### Maturity Model

| Stage | Label         | Description                                              | Intended Use                |
|-------|--------------|----------------------------------------------------------|-----------------------------|
| 0     | Experimental | Design, scaffolding, control definitions, CI bootstrapping | Evaluation & research        |
| 1     | Alpha        | Core logic implemented end-to-end with gaps               | Internal sandbox testing     |
| 2     | Beta         | CI-tested, partial coverage, validated controls           | Controlled pilot deployments |
| 3     | Stable       | Versioned, test-covered, production-ready patterns        | Enterprise / production use  |

### Planned Future Enhancements

#### CI & Security
- Full golden dataset testing
- Secret scanning
- SBOM & dependency scanning
- Policy schema validation
- Prompt security linting

#### Documentation & Controls
- Additional reference architectures
- Expanded control catalog
- Tooling examples and agent demos
- Public Owner’s Guide

#### Agent & Framework Enhancements
- Example multi-agent orchestration
- Tooling adapters (OpenAI MCP / LangChain / Azure / AWS)
- Real-world security playbooks

### Badge Palette for Future Stages

- Stage 1 — Alpha  
  `![maturity](https://img.shields.io/badge/maturity-Stage%201%20%E2%80%94%20Alpha-yellowgreen)`

- Stage 2 — Beta  
  `![maturity](https://img.shields.io/badge/maturity-Stage%202%20%E2%80%94%20Beta-orange)`

- Stage 3 — Stable  
  `![maturity](https://img.shields.io/badge/maturity-Stage%203%20%E2%80%94%20Stable-brightgreen)`

---

### Visual Roadmap Diagram (Coming Soon)

A visual maturity diagram for F7-LAS will be published in the documentation.

## Contributing

Contributions welcome — scenarios, policies, prompts, controls, tools.  
Follow:the [Engineering Review Checklist](docs/Engineering-Review-Checklist.md)
- Engineering Review Checklist  
- CI pipeline requirements  
- PSP formatting rules  

---

## License & Disclaimer

© 2025 Anthony L. Fuller. All rights reserved.
F7-LAS™ is a trademark of Anthony L. Fuller. Trademark application pending.

This project was created independently by the author and is not affiliated with, endorsed by, or associated with Microsoft or any other employer. All opinions, designs, diagrams, and documentation represent the author’s personal work and do not reflect the views of Microsoft.

Licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/


