# F7-LAS — Fuller 7-Layer Agentic AI Security Framework™

*A layered, control-centric security architecture for agentic and multi-agent AI systems.*

![CI](https://github.com/anthfuller/F7-LAS/actions/workflows/f7las-ci.yml/badge.svg)
![status](https://img.shields.io/badge/status-passing-brightgreen)
![version](https://img.shields.io/badge/version-v3.1-blue)
![license](https://img.shields.io/badge/license-Proprietary-lightgrey)
![maturity](https://img.shields.io/badge/maturity-Stage%200%20%E2%80%94%20Experimental-yellow)

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
│   ├── validate-prompts.py
│   ├── validate-policies.py
│   ├── validate-settings.py
│   └── check-golden-thresholds.py
│
├── docs/
│   ├── Security-Agentic-AI-The-7-Layer-Model-v2.4.pdf
│   ├── F7-LAS-Implementation-Guide-v3.1/
│   │   ├── 00-Introduction.md
│   │   ├── 01-Control-Objectives.md
│   │   ├── 02-Layer-by-Layer-Controls.md
│   │   ├── 03-Suppplemental-Layer-S.md
│   │   ├── 04-Model-Security-Annex.md
│   │   ├── 05-Metrics-and-SLOs.md
│   │   ├── 06-Operational-Playbooks.md
│   │   ├── 07-RACI-Model.md
│   │   ├── 08-Implementation-Profiles.md
│   │   └── appendices/
│   │       ├── a-schemas.md
│   │       ├── b-templates.md
│   │       ├── c-engineering-review-checklist.md
│   │       └── d-reference-architectures.md
│   │
│   ├── Engineering-Review-Checklist.md
│   ├── Multi-Agent-F7-LAS_Architecture.png
│   └── F7-LAS-Control-Catalog_v0.1.md
│
├── config/
│   ├── prompts/
│   ├── policies/
│   └── settings.yaml
│
├── src/
│   ├── core/
│   ├── agents/
│   ├── tools/
│   └── demo-runner/
│
├── tests/
│   ├── golden-dataset/
│   └── test-agents-basic.py
│
└── examples/
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

## Contributing

Contributions welcome — scenarios, policies, prompts, controls, tools.  
Follow:
- Engineering Review Checklist  
- CI pipeline requirements  
- PSP formatting rules  

---

## License & Disclaimer

© 2025 Anthony L. Fuller. All rights reserved.  
F7-LAS™ is a trademark of Anthony L. Fuller. Trademark application pending.

This project was created independently by the author and is not affiliated with, endorsed by, or associated with Microsoft or any other employer. All opinions, design patterns, and documentation reflect the author's personal work.


