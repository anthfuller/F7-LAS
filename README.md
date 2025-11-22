# F7-LAS – Fuller 7-Layer Agentic AI Security Framework

F7-LAS (Fuller 7-Layer Agentic AI Security Framework) is a control-oriented security framework and reference implementation for **agentic and multi-agent AI systems**.

This repository contains:

- The **F7-LAS whitepaper** (`docs/Security_Agentic_AI_The_7-Layer_Model_v2.3.pdf`)
- A **vendor-neutral multi-agent SOC demo** (Coordinator / Investigator / Remediator agents)
- Example **policies, prompts, tools, and test scenarios** that show how to apply the 7 layers in practice
- A **Control Catalog** for F7-LAS (L1–L7 + Layer S)
- An **Engineering Review Checklist** and **DevSecOps pipeline** for CI-enforced controls

> **Status:** v3.0 – Conceptual model stable; implementation patterns, control catalog, and CI/DevSecOps pipeline are evolving.

---

## 1. What F7-LAS Is

F7-LAS models agentic AI security as a **7-layer control stack**:

1. **System Prompt (Soft Policy)**  
   Role, scope, safety posture, escalation rules.

2. **RAG / Grounding (Epistemic Guardrail)**  
   Trusted context, provenance, and retrieval controls.

3. **Agent Planner / Controller**  
   Reason–act loops, planning contracts, bounded autonomy.

4. **Tools & Integrations (Action Surface)**  
   The agent’s actuators; what it can actually change or query.

5. **Policy Engine Outside the LLM (Hard Guardrails – PDP/PEP)**  
   Permit / Deny / Obligations / Human-in-the-loop at runtime.

6. **Sandboxed Execution Environment (Blast Radius Control)**  
   Tenants, identities, networks, environments that constrain impact.

7. **Monitoring, Evaluation & Assurance**  
   Telemetry, drift detection, red-teaming, evaluation, and continuous assurance.

The framework is **vendor-neutral** and can be applied with any LLM platform, SIEM, EDR, IdP, or workflow engine.

F7-LAS is designed to **complement**, not replace or formally map to:

- NIST AI RMF  
- ISO/IEC 42001 / 23894  
- EU AI Act principles  
- MITRE ATT&CK / MITRE ATLAS  

It provides **agent-specific controls and patterns** where those standards are high-level.

---

## 2. How F7-LAS Fits with Other Agentic AI Frameworks

F7-LAS is designed to complement, not replace, other frameworks:

- **MAESTRO (CSA)** – threat modeling and layered architecture for agentic AI.  
- **AAM (Agentic Access Management)** – identity and access for agents and non-human identities.  
- **AIGN Agentic AI Governance Framework** – governance, trust, and regulatory alignment.

F7-LAS adds a **control-centric view**:

- MAESTRO / AAM / AIGN help you describe risks, access, and governance.  
- **F7-LAS helps you decide which technical controls to put around agent behavior** – from prompts and planners to tools, policy engines, sandboxes, and monitoring.

---

## 3. Repository Layout

```text
F7-LAS/
├── README.md
├── LICENSE
├── requirements.txt          # Python deps for examples, tests, CI
│
├── .github/
│   └── workflows/
│       └── f7las-ci.yml      # CI: lint, tests, golden eval, config checks, SCA hook
│
├── scripts/                  # Helper scripts used by CI and local checks
│   ├── validate_prompts.py       # L1: schema/guardrails for config/prompts/*.txt
│   ├── validate_policies.py      # L5: schema/consistency for config/policies/*.yaml
│   ├── validate_settings.py      # L3: safety bounds for config/settings.yaml
│   └── check_golden_thresholds.py# L7: enforce min scores on golden_dataset results
│
├── docs/
│   ├── Security_Agentic_AI_The_7-Layer_Model_v2.3.pdf      # Core whitepaper (F7-LAS model)
│   ├── F7-LAS_Implementation_Guide_v3.0.pdf                # Full engineering blueprint
│   ├── F7-LAS_Control_Catalog_v0.1.md                      # Layered control set for agentic systems
│   ├── F7-LAS_Strength-Weakness-Improvement-Report.pdf     # Design review & roadmap
│   ├── F7-LAS_DevSecOps_Pipeline.pdf                       # GitHub-based DevSecOps pipeline
│   ├── Engineering_Review_Checklist.md                     # F7-LAS engineering review checklist
│   ├── Multi-Agent_F7-LAS_Architecture.png
│   └── ...                                                 # Diagrams, worksheets, appendices
│
├── config/
│   ├── prompts/
│   │   ├── coordinator_system_prompt.txt
│   │   ├── investigator_system_prompt.txt
│   │   └── remediation_system_prompt.txt
│   ├── policies/
│   │   ├── protected_assets.yaml
│   │   ├── whitelisted_ips.yaml
│   │   └── do_not_isolate.yaml
│   └── settings.yaml             # model names, max steps, timeouts, etc.
│
├── src/
│   ├── core/
│   │   ├── llm_client.py
│   │   ├── state_manager.py
│   │   ├── safety_harness.py
│   │   └── protocol_types.py
│   ├── agents/
│   │   ├── coordinator_agent.py
│   │   ├── investigator_agent.py
│   │   └── remediation_agent.py
│   ├── tools/
│   │   ├── mock_siem.py
│   │   ├── mock_edr.py
│   │   └── mock_idp.py
│   └── demo_runner/
│       ├── run_single_scenario.py
│       └── run_golden_dataset.py
│
├── tests/
│   ├── golden_dataset/
│   │   ├── scenarios.json
│   │   └── rubric.json
│   └── test_agents_basic.py
│
└── examples/
    ├── walkthrough_false_positive.md
    ├── walkthrough_ransomware_case.md
    └── README.md
4. Core Documents
F7-LAS Whitepaper (Model):
docs/Security_Agentic_AI_The_7-Layer_Model_v2.3.pdf

F7-LAS Implementation Guide v3.0:
docs/F7-LAS_Implementation_Guide_v3.0.pdf

F7-LAS Control Catalog v0.1:
docs/F7-LAS_Control_Catalog_v0.1.md

Strength, Weakness & Improvement Report:
docs/F7-LAS_Strength-Weakness-Improvement-Report.pdf

DevSecOps Pipeline for F7-LAS:
docs/F7-LAS_DevSecOps_Pipeline.pdf

F7-LAS Engineering Review Checklist:
docs/Engineering_Review_Checklist.md

5. Quickstart (Local)
bash
Copy code
git clone https://github.com/<your-org>/F7-LAS.git
cd F7-LAS

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
pytest -q tests/test_agents_basic.py

python -m src.demo_runner.run_golden_dataset \
  --scenarios tests/golden_dataset/scenarios.json \
  --rubric tests/golden_dataset/rubric.json \
  --output-file golden_eval_results.json

python scripts/check_golden_thresholds.py golden_eval_results.json
Run a single demo scenario:

bash
Copy code
python -m src.demo_runner.run_single_scenario --scenario-id "A"
6. F7-LAS + DevSecOps (CI/CD Alignment)
The .github/workflows/f7las-ci.yml pipeline enforces F7-LAS controls over:

Code (core, agents, tools)

Prompts, policies, and settings

Golden scenario evaluations

SBOM/SCA checks for dependencies

No merges to main if any job fails.

7. Use Cases
Security copilots / SOC assistants

Agentic automation on top of SIEM/XDR/SOAR

Multi-agent security workflows (Coordinator / Investigator / Remediator)

Vendor-agnostic agent governance

8. Roadmap (High-Level)
More reference implementations

More golden scenarios and adversarial tests

Policy packs for common SOC patterns

Refinement of the Control Catalog (v0.1 → v1.0)

9. Contributing
Contributions welcome: scenarios, profiles, policies, controls, or code.
Please open an issue first for significant changes.

10. License
This project is licensed under the terms in LICENSE.

© 2025 Anthony L. Fuller. All rights reserved.
