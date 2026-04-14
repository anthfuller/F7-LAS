# F7-LAS™ — The Fuller 7-Layer Agentic Security Model

![CI](https://github.com/anthfuller/F7-LAS/actions/workflows/f7las-ci.yml/badge.svg)
![ci_status](https://img.shields.io/badge/CI-passing-brightgreen)
![version](https://img.shields.io/badge/version-v3.1.1-blue)
![license](https://img.shields.io/badge/license-CC%20BY%204.0%20%2B%20MIT-blue)
![maturity](https://img.shields.io/badge/maturity-Stage%202%20—%20Beta-blue)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.17887940-blue.svg)](https://doi.org/10.5281/zenodo.18292122)


> **Disclaimer:** This is an independent personal project and is not affiliated with or endorsed by Microsoft. All work reflects the author's personal views only.



F7-LAS™ (Fuller 7-Layer Agentic Security) is an open security model for designing, validating, and governing agentic AI systems.
It defines seven interdependent layers—spanning prompts, grounding, planning logic, tool security, policy enforcement, sandboxing, and monitoring—to reduce risk in emerging LLM-driven autonomous agents.

### Intended Audience

F7-LAS is intended for security architects, SOC engineers, and platform owners designing or reviewing agentic AI systems with real operational authority. It emphasizes governance, enforcement, containment, and observability rather than agent intelligence or learning algorithms.


This repository currently provides:

- The F7-LAS whitepaper and implementation guide
- Schemas, prompts, and policy examples
- A Stage-2 beta reference implementation of key runtime pieces:
  - Layer 1: example system prompts for Investigator / Coordinator / Remediator agents
  - Layer 2: grounding / allowlist profiles
  - Layer 3: a simple planner stub
  - Layer 4: example tool schemas and stub implementations
  - Layer 5: policy engine examples (PDP/PEP) including an OPA/Rego demo and vendor-neutral PEP patterns
  - Layer 6: a minimal sandbox container stub
  - Layer 7: a lightweight telemetry schema and logger
- CI scaffolding and validation scripts for policies, prompts, and settings
- Early examples and patterns for applying seven-layer security to agentic workflows

**Maturity roadmap.**  
F7-LAS is currently at **Stage 2 – Beta**.  
The repository includes behavioral CI, negative test coverage, and golden dataset enforcement validating allow and deny paths. Coverage and reference implementations continue to expand toward stable, production-ready patterns.



### F7-LAS Maturity Stages

| Stage | Label      | Description                                     | Use Readiness             |
|-------|-----------|-------------------------------------------------|---------------------------|
| 0     | Conceptual| Design, scaffolding, early controls and docs.   | Evaluation, learning, PoC |
| 1     | Prototype | Core logic working end-to-end with gaps.        | Internal sandbox only     |
| 2     | Beta      | CI + tests in place, coverage improving.        | Controlled pilot / lab    |
| 3     | Stable    | Versioned, test-covered, documented patterns.   | Production-ready          |

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

## FAQ (Quick Answers)

**Is F7-LAS a framework or a model?**  
F7-LAS is primarily a **security model** for agentic AI, with example code and patterns. It is not a full production agent framework.

**What is “Stage-2 / Beta” mean for this repo?**  
Stage 2 (Beta) means the repository includes:
- Behavioral CI enforcing real execution paths
- Negative test coverage (deny and malformed cases)
- Golden dataset enforcement
- Working Layer-5 policy patterns (PDP/PEP)
- Reference sandbox and telemetry stubs

The project is suitable for controlled lab use and pilot experimentation, but is not yet production-ready.

**Can I use this in production?**  
Not as-is. The examples are meant as reference patterns and starting points. Any real deployment should go through your own engineering, security review, and hardening.

**Does this represent Microsoft’s views?**  
No. This is an independent project by the author and is **not affiliated with, endorsed by, or associated with Microsoft** or any other employer.

**Where do I start?**  
Suggested entry points:
- Read the whitepaper in `docs/`.
- Skim `examples/` for Layer-by-Layer demos.
- Look at `examples/layer5-policy-engines/` for the PDP/PEP patterns.



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
|   |
│   ├── F7-LAS-Implementation-Guide/
│   │   ├── 00-introduction.md
│   │   ├── 01-control-objectives.md
│   │   ├── 02-layer-by-layer-controls.md
│   │   ├── 03-supplemental-layer-s.md
│   │   ├── 04-model-security-annex.md
│   │   ├── 05-metrics-and-slos.md
│   │   ├── 06-operational-playbooks.md
│   │   ├── 07-raci-model.md
│   │   ├── 08-implementation-profiles/
|   |   |   └── Optional-MCP-Security-Profile.md
|   |   |
│   │   └── layer-s/
│   │       ├── README.md
│   │       ├── checklist.md
│   │       ├── sbom-guidance.md
│   │       ├── vetting-workflow.md
│   │       └── allowlist-schema.json
│   │
│   ├── Engineering-Review-Checklist.md
│   ├── F7-LAS-Control-Catalog-v0.1.md
│   ├── F7-LAS-Model-v1.png
│   ├── F7-LAS-QA.md
│   ├── F7-LAS-model-whitepaper_v2.4.pdf
│   ├── README.md
│   └── images/
│       ├── F7-LAS-Model-v1A.png
│       ├── F7-LAS-Model-v1B.png 
│       ├── F7-LAS_Execution_Control_Loop.png
│       └── afuller_f7-las-model.png
│
├── config/
│   ├── prompts/
│   ├── policies/
│   ├── psp-schema.json
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
│   │   └── scenario.json
│   └── test_agents_basic.py
│
└── examples/
    ├── README.md
    ├── basic_agent_flow.md
    ├── demo_system_prompt.txt
    ├── policy_enforced_tool_call.md
    ├── simple_rag_query.md
    ├── simple_rag_readonly.md
    ├── walkthrough_false_positive.md
    ├── walkthrough_ransomware_case.md
    ├── layer1-system-prompt/
    ├── layer2-grounding/
    ├── layer3-planner/
    ├── layer4-tools/
    ├── layer5-policy-engines/
    ├── layer6-sandbox/
    └── layer7-monitoring/
```

---

## Tooling & CI Pipeline

**GitHub Actions Workflow:** `.github/workflows/f7las-ci.yml`

Enforces:
- Prompt validation (Layer 1 PSP compliance)
- Policy validation (Layer 5)
- Settings validation (Layer 3 safety)
- Golden dataset scoring (Layer 7, Stage-1 placeholder)
- Unit tests
- Optional linting & SBOM/SCA (future expansion)

---

## Quickstart

```bash
git clone https://github.com/anthfuller/F7-LAS.git
cd F7-LAS

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run tests:

```bash
pytest -q tests/test_agents_basic.py
```

Run the golden evaluator (Stage-2 beta enforcement):

```bash
python scripts/check_golden_thresholds.py tests/golden_dataset/golden_eval_results.json
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
- Prompt Security Profile (PSP) schema  
- Policy validation (L5) 
- Sandbox rules (L6 prototype)  
- Drift detection & evaluation logic  

**Development**
- Example demo runner  
- Placeholder tests  
- CI workflow and validators  

---

## Roadmap

F7-LAS is evolving through clearly defined maturity stages to ensure transparency, stability, and long-term governance.

### Current Maturity Stage

![maturity](https://img.shields.io/badge/maturity-Stage%202%20—%20Beta-blue)

F7-LAS is currently **Stage 2 — Beta**. 
Layers 1–7 include working reference implementations and examples (beta), validated by behavioral CI and golden dataset enforcement, including:
- System prompts (L1)  
- Grounding profile + allowlist (L2)  
- Simple planner stub (L3)  
- Stub tools + schemas (L4)  
- Multi-vendor Layer-5 PDP/PEP examples (OPA, Cedar, Sentinel, Kyverno, SpiceDB)  
- Minimal sandbox boundary (L6)  
- Telemetry schema + logger (L7)


### Maturity Model

| Stage | Label      | Description                                              | Intended Use                |
|-------|-----------|----------------------------------------------------------|-----------------------------|
| 0     | Conceptual| Design, scaffolding, control definitions, CI bootstrapping | Evaluation & research       |
| 1     | Prototype | Core logic implemented end-to-end with gaps               | Internal sandbox testing    |
| 2     | Beta      | CI-tested, partial coverage, validated controls           | Controlled pilot deployments|
| 3     | Stable    | Versioned, test-covered, production-ready patterns        | Enterprise / production use |

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
- Tooling adapters (OpenAI MCP / LangChain / Azure / AWS / GCP)
- Real-world security playbooks

### Badge Palette for Future Stages

- Stage 1 — Prototype  
  `![maturity](https://img.shields.io/badge/maturity-Stage%201%20—%20Prototype-yellowgreen)`

- Stage 2 — Beta  
  `![maturity](https://img.shields.io/badge/maturity-Stage%202%20%E2%80%94%20Beta-orange)`

- Stage 3 — Stable  
  `![maturity](https://img.shields.io/badge/maturity-Stage%203%20%E2%80%94%20Stable-brightgreen)`

---

### Visual Roadmap Diagram (Coming Soon)

A visual maturity diagram for F7-LAS will be published in the documentation.

## Contributing

Contributions welcome — scenarios, policies, prompts, controls, tools.  
Follow the [Engineering Review Checklist](docs/Engineering-Review-Checklist.md) for:
- Engineering review steps  
- CI pipeline requirements  
- PSP formatting rules
  
By submitting a contribution, you agree that your contribution is licensed
under the same terms as this project (CC BY 4.0 for content, MIT for code)
and that Anthony L. Fuller retains authorship and trademark rights over the
F7-LAS™ framework as a whole.

---

## How to Cite F7-LAS

If you reference or build upon this work in research, engineering documentation, or academic publications, please cite the Zenodo-archived version below.

### **APA**
Fuller, A. (2025). *Securing Agentic AI: The AFuller F7-LAS™ (7-Layer) Model*. Zenodo. https://doi.org/10.5281/zenodo.18292122

### **MLA**
Fuller, Anthony. *Securing Agentic AI: The AFuller F7-LAS™ (7-Layer) Model*. 2025, Zenodo, https://doi.org/10.5281/zenodo.18292122.

### **Chicago**
Fuller, Anthony. “Securing Agentic AI: The AFuller F7-LAS™ (7-Layer) Model.” Zenodo, 2025. https://doi.org/10.5281/zenodo.18292122.

### **BibTeX**
```bibtex
@misc{fuller_f7las_2025,
  title        = {Securing Agentic AI: The AFuller F7-LAS™ (7-Layer) Model},
  author       = {Fuller, Anthony},
  year         = {2025},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.18292122},
  url          = {https://doi.org/10.5281/zenodo.18292122}
}
```

---

## License & Disclaimer

© 2025 Anthony L. Fuller. Content licensed under CC BY 4.0; source code licensed under MIT License. All trademark rights reserved.
F7-LAS™ is a trademark of Anthony L. Fuller. Trademark application pending.

This project was created independently by the author and is not affiliated with, endorsed by, or associated with Microsoft or any other employer.  
All opinions, designs, diagrams, and documentation represent the author’s personal work and do not reflect the views of Microsoft.

## Licensing

- All documentation, diagrams, models, and written content are licensed under **CC BY 4.0**.  
- All source code in the `/src/`, `/examples/`, `/scripts/`, and `/config/` directories is licensed under the **MIT License**.
