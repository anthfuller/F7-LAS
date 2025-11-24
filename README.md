# F7-LAS – Fuller 7-Layer Agentic AI Security Framework

**F7-LAS** (Fuller 7-Layer Agentic AI Security) is a practical, layered security model and reference implementation for **agentic AI systems** – especially LLM-based agents that can call tools, change state, and operate in SOC / cloud environments.

It focuses on **how to govern and secure agents**, not how to make them “smart.”

> **Status:** v3.0 – Conceptual model stable; implementation patterns, code examples, control catalog, and CI/DevSecOps pipeline are evolving.

---

## 1. What F7-LAS Is

F7-LAS defines **seven interdependent layers** that together secure an agent from prompt to production:

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

A **multi-agent governance pattern** (Coordinator → Investigator → Remediator) overlays these layers, with per-agent prompts, tools, and policies and shared sandboxing and telemetry.

F7-LAS is designed to **complement** (not replace or formally map to):

- NIST AI RMF  
- ISO/IEC 42001 / 23894  
- EU AI Act principles  
- MITRE ATT&CK / MITRE ATLAS  

It provides **agent-specific controls and patterns** where those standards are high-level.

---

## 2. Repository Layout

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
3. Core Documents
F7-LAS Whitepaper (Model):
docs/Security_Agentic_AI_The_7-Layer_Model_v2.3.pdf
Introduces the 7-layer model, POMDP-style reasoning, threat–control concepts, multi-agent pattern, and appendices (maturity model, KPIs, threat map, IR usage, etc.).

F7-LAS Implementation Guide v3.0:
docs/F7-LAS_Implementation_Guide_v3.0.pdf
Complete build blueprint:

Layer-by-layer components & controls

Policy, tool, sandbox, telemetry schemas

Vendor-neutral, Azure AI Foundry, and LangGraph profiles

Incident-response playbooks (IR-F7 series)

Quantitative risk scoring and SLOs per layer

Supplemental Layer S for software supply chain & framework security

F7-LAS Control Catalog v0.1:
docs/F7-LAS_Control_Catalog_v0.1.md
A structured, layer-organized control set (L1–L7 + Layer S) with control IDs, intents, implementation notes, and evidence examples. Designed to complement NIST/ISO/ATLAS, not formally map to them.

Strength, Weakness & Improvement Report:
docs/F7-LAS_Strength-Weakness-Improvement-Report.pdf
Honest assessment of F7-LAS strengths, gaps, and improvement opportunities, including comparison concepts vs. agent frameworks (e.g., LangGraph).

DevSecOps Pipeline for F7-LAS:
docs/F7-LAS_DevSecOps_Pipeline.pdf
GitHub Actions-based pipeline that enforces F7-LAS controls on:

prompts, policies, settings

planner/agents, tools

tests & golden scenarios

SBOM/SCA and supply-chain checks

F7-LAS Engineering Review Checklist:
docs/Engineering_Review_Checklist.md
Structured checklist for architecture/security reviews to assess alignment with all 7 layers (plus multi-agent governance).

4. Quickstart (Local)
4.1. Install dependencies
bash
Copy code
git clone https://github.com/<your-org>/F7-LAS.git
cd F7-LAS

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
4.2. Run basic tests
bash
Copy code
pytest -q tests/test_agents_basic.py
4.3. Run the golden dataset evaluation (Layer 7)
bash
Copy code
python -m src.demo_runner.run_golden_dataset \
  --scenarios tests/golden_dataset/scenarios.json \
  --rubric tests/golden_dataset/rubric.json \
  --output-file golden_eval_results.json

python scripts/check_golden_thresholds.py golden_eval_results.json
This simulates end-to-end agent behavior across scenarios and ensures changes haven’t regressed safety or correctness.

4.4. Run a single demo scenario
bash
Copy code
python -m src.demo_runner.run_single_scenario --scenario-id "A"
5. F7-LAS + DevSecOps (CI/CD Alignment)
The .github/workflows/f7las-ci.yml pipeline enforces F7-LAS at the code/config level:

Static analysis:
Lint/type-check core, agents, tools (Layers 3–4).

Unit tests:
tests/test_agents_basic.py – core behaviors and orchestration sanity.

Golden dataset evaluations:
run_golden_dataset.py + check_golden_thresholds.py – Layer 7 evaluation and drift detection.

Prompt & policy validation:
scripts/validate_prompts.py – Layer 1
scripts/validate_policies.py – Layer 5
scripts/validate_settings.py – Layer 3 (bounds: max steps, timeouts, tool limits)

Supply-chain / SBOM / SCA:
Layer S – ensures dependencies and tools are scanned and gated in CI.

Branch protection:
main is protected so changes to prompts, policies, tools, safety harness, etc. must pass CI and receive review before merge.

This makes F7-LAS not just a model, but an enforceable engineering standard for agentic AI systems.

6. Use Cases
F7-LAS is intended for teams building:

Security-focused copilots and agents
SOC assistants, threat hunting agents, IR copilots.

Agentic AI on top of SIEM/XDR/SOAR
Agents that investigate alerts, enrich entities, open/update tickets, propose or trigger remediation.

Multi-agent security workflows
Coordinator–Investigator–Remediator patterns with human-on-the-loop oversight.

Vendor-agnostic agent governance
Works alongside frameworks like LangGraph, Azure AI Foundry, Bedrock, etc. by mapping F7-LAS layers to runtime components.

7. Roadmap (High-Level)
Planned / ongoing:

Additional reference implementations (beyond mock tools)

Expanded LangGraph + Azure AI Foundry profiles

Additional golden scenarios and adversarial tests

Example policy packs for common SOC patterns

Hardened Layer S supply-chain templates (SBOM, SCA integrations)

More examples/ walkthroughs and diagrams for practitioners

Refinement of the Control Catalog (v0.1 → v1.0) based on feedback

See the repo’s Issues and Projects for details and progress.

8. Contributing
Contributions are welcome, including:

New golden scenarios / rubrics

Additional cloud/runtime integration profiles

Improvements to prompts, policies, or schemas

Enhancements to the control catalog and engineering checklist

Bug fixes or enhancements in src/ and scripts/

Please open an issue first to discuss substantial changes.

9. License
This project is licensed under the terms specified in LICENSE.

© 2025 IT Security Partners LLC. All rights reserved where applicable.
