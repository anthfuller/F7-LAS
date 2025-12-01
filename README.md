# F7-LAS™ — The Fuller 7-Layer Agentic Security Model

![CI](https://github.com/anthfuller/F7-LAS/actions/workflows/f7las-ci.yml/badge.svg)
![ci_status](https://img.shields.io/badge/CI-passing-brightgreen)
![version](https://img.shields.io/badge/version-v0.1.0-blue)
![license](https://img.shields.io/badge/license-CC%20BY%204.0-blue)
![maturity](https://img.shields.io/badge/maturity-Stage%201%20—%20Prototype-yellowgreen)


**F7-LAS™ (Fuller 7-Layer Agentic Security)** is an open security model for designing, validating, and governing agentic AI systems.  
It defines seven interdependent layers—spanning prompts, grounding, planning logic, tool security, policy enforcement, sandboxing, and monitoring—to reduce risk in emerging LLM-driven autonomous agents.

This repository provides:

- The **F7-LAS whitepaper**
- **Schemas, prompts, and policy examples**
- **Continuous Integration (CI) scaffolding**
- **Implementation guidelines**
- Early-stage **examples and patterns** for applying seven-layer security to agentic workflows

F7-LAS is **not a runtime implementation** at this stage.  
It is a **conceptual model** with active engineering expansion.

> **Maturity roadmap:**
> F7-LAS is currently at Stage 0 – Conceptual. The core runtime components (agents, tools, orchestration, and controller logic) are not yet implemented in this repository.
> The current focus is on the conceptual model, control layers, prompts, policies, schemas, and CI scaffolding. Future stages will introduce example agents, hardened CI, golden datasets, reference implementations, and operational playbooks.


### F7-LAS Maturity Stages

| Stage | Label                     | Description                                     | Use Readiness            |
|-------|---------------------------|-------------------------------------------------|--------------------------|
| 0     | Conceptual              | Design, scaffolding, early controls and docs.   | Evaluation, learning, PoC |
| 1     | Alpha                     | Core logic working end-to-end with gaps.        | Internal sandbox only     |
| 2     | Beta                      | CI + tests in place, coverage improving.        | Controlled pilot / lab    |
| 3     | Stable                    | Versioned, test-covered, documented patterns.   | Production-ready          |

F7-LAS is intentionally **opinionated** and will move through these stages as the implementation guide, control catalog, golden datasets, and CI hardening mature.

## 🌐 Overview
F7-LAS (Fuller 7-Layer Agentic AI Security Model) defines a **layered control model** for securing AI agents that can plan, reason, call tools, modify systems, and interact with enterprise environments.

It provides:
- A **7-layer control stack** (L1–L7)
- A **supplemental supply-chain layer (Layer S)**
- A **full implementation guide**, patterns, controls, and engineering checklists
- A **vendor-neutral reference model**
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
│   ├── F7-LAS-model-whitepaper.pdf
│   ├── Engineering-Review-Checklist.md
│   ├── F7-LAS-Control-Catalog-v0.1.md
│   │
│   ├── F7-LAS-Implementation-Guide/
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
│   │       └── d-reference-patterns.md
│   │
│   └── images/
│       ├── F7-LAS-Model-v1.png
│       ├── F7-LAS-Model-v1A.png
│       ├── F7-LAS_Execution_Control_Loop.png
│       └── afuller_f7-las-model.png
│
├── config/
│   ├── prompts/
│   │   ├── investigator_prompt.txt
│   │   ├── coordinator_prompt.txt
│   │   ├── remediator_prompt.txt
│   │
│   ├── policies/
│   │   ├── agent-policy.json
│   │   ├── policy-schema.json
│   │   ├── policy-safety-default.json
│   │   ├── policy-escalation-default.json
│   │   ├── policy-constraints-default.json
│   │   ├── protected-assets.yaml
│   │   ├── whitelisted-ips.yaml
│   │   ├── tool-policy.yaml
│   │   ├── rag-policy.yaml
│   │   ├── sandbox-profile.yaml
│   │   │
│   │   └── l5/
│   │       └── opa/
│   │           └── agent_security_enforcement.rego   ← **L5 PDP policy**
│   │
│   ├── psp-schema.json
│   └── settings.yaml
│
├── src/
│   ├── agents/
│   │   └── (future Stage-2 agent runners)
│   │
│   ├── core/
│   │   └── (core framework pieces)
│   │
│   ├── demo_runner/
│   │   ├── demo_l5_flow.py        ← **Optional test harness**
│   │   └── demo_agent_loop.py     ← **Stage-1 agent loop**
│   │
│   ├── tools/
│   │   └── aws_ec2_client_stub.py  ← **Layer 4 stub**
│   │
│   └── policy/
│       ├── decision.py             ← **PolicyDecision dataclass**
│       ├── pep_base.py             ← **Base PEP class**
│       └── pep_opa.py              ← **OPA PEP**
│
├── layer1-system-prompt/
│   ├── README.md
│   ├── investigator_prompt.txt
│   ├── coordinator_prompt.txt
│   └── remediator_prompt.txt
│
├── layer2-grounding/
│   ├── README.md
│   ├── allowlist.json
│   └── grounding_profile.yaml
│
├── layer3-planner/
│   ├── README.md
│   └── simple_planner.py
│
├── layer4-tools/
│   ├── README.md
│   ├── tool_schema.json
│   └── aws_ec2_client_stub.py
│
├── layer5-policy-engine/
│   ├── README.md
│   ├── pep/
│   │   ├── pep_base.py
│   │   ├── pep_opa.py
│   │   ├── pep_cedar.py
│   │   ├── pep_sentinel.py
│   │   ├── pep_spicedb.py
│   │   └── pep_kyverno.py
│   │
│   └── pdp/
│       └── opa/
│           ├── agent_security_enforcement.rego
│           ├── data.json
│           └── docker-compose.yml
│
├── layer6-sandbox/
│   ├── README.md
│   └── docker-compose.yml
│
├── layer7-monitoring/
│   ├── README.md
│   ├── telemetry_logger.py
│   └── telemetry_schema.json
│
└── examples/
    ├── README.md
    ├── basic_agent_flow.md
    ├── policy_enforced_tool_call.md
    ├── simple_rag_query.md
    ├── walkthrough_false_positive.md
    ├── walkthrough_ransomware_case.md
    └── layer5-policy-engines/
        ├── aws-cedar/
        ├── azure-custom/
        ├── sentinel/
        ├── spicedb/
        ├── kyverno/
        └── opa-rego/
            ├── docker-compose.yml
            └── README.md
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

![maturity](https://img.shields.io/badge/maturity-Stage%201%20—%20Prototype-yellowgreen)

F7-LAS is currently **Stage 1 — Prototype**.  
Layers 1–7 now include minimal, working examples including:
- System prompts (L1)  
- Grounding profile + allowlist (L2)  
- Simple planner stub (L3)  
- Stub tools + schemas (L4)  
- Multi-vendor Layer-5 PDP/PEP examples (OPA, Cedar, Sentinel, Kyverno, SpiceDB)  
- Minimal sandbox boundary (L6)  
- Telemetry schema + logger (L7)


### Maturity Model

| Stage | Label         | Description                                              | Intended Use                |
|-------|--------------|----------------------------------------------------------|-----------------------------|
| 0     | Conceptuual  | Design, scaffolding, control definitions, CI bootstrapping   | Evaluation & research        |
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
- Example implementation patterns
- Expanded control catalog
- Tooling examples and agent demos
- Public Owner’s Guide

#### Agent & Model Enhancements
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


