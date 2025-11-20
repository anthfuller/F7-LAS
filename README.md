# F7-LAS – Fuller 7-Layer Agentic AI Security Model

**F7-LAS** (Fuller 7-Layer Agentic AI Security Model) is a control-oriented security framework and reference implementation for **agentic and multi-agent AI systems**.

This repository contains:

- The **F7-LAS whitepaper** (v2.1F)
- A **vendor-neutral multi-agent SOC demo** (Coordinator / Investigator / Remediation agents)
- Example **policies, prompts, and test scenarios** that show how to apply the 7 layers in practice

> **Status:** Early technical preview – APIs, structure, and code may evolve.

---

## 1. What is F7-LAS?

F7-LAS models agentic AI security as a **7-layer control stack**:

1. **System Prompt (Soft Policy)**
2. **Grounding / RAG (Epistemic Guardrail)**
3. **Agent Planner / Controller**
4. **Tools & Integrations (Action Surface)**
5. **Policy Engine outside the LLM (Hard Guardrails)**
6. **Sandboxed Execution Environment (Blast Radius Control)**
7. **Monitoring & Evaluation (Detection & Assurance)**

The framework is **vendor-neutral** and can be applied with any LLM platform, SIEM, EDR, IdP, or workflow engine.

The full model, rationale, and maturity matrix are described in:

- `docs/Security_Agentic_AI_The_7-Layer_Model_v2.1.pdf`

---

## 2. How F7-LAS Fits with Other Agentic AI Frameworks

F7-LAS is designed to **complement**, not replace, other frameworks:

- **MAESTRO (CSA)** – focuses on **threat modeling and layered architecture** for agentic AI.
- **AAM (Agentic Access Management)** – focuses on **identity and access** for agents and non-human identities.
- **AIGN Agentic AI Governance Framework** – focuses on **governance, trust, and regulatory alignment**.

**F7-LAS adds a control-centric view:**

- MAESTRO / AAM / AIGN help you describe **risks, access, and governance**.
- **F7-LAS helps you decide _which technical controls_ to put around agent behavior** – from prompts and planners to tools, policy engines, sandboxes, and monitoring.

---

## 3. Repository Layout (high level)

```text
F7-LAS/
├── README.md
├── LICENSE
├── docs/
│   ├── Security_Agentic_AI_The_7-Layer_Model_v2.1F.pdf
│   └── Multi-Agent_F7-LAS_Architecture.png
│
├── config/
│   ├── prompts/
│   ├── policies/
│   └── settings.yaml
│
├── src/
│   ├── core/          # LLM client interface, state manager, safety harness, protocol types
│   ├── agents/        # Coordinator, Investigator, Remediator
│   ├── tools/         # Vendor-neutral mock SIEM / EDR / IdP connectors
│   └── demo_runner/   # Scripts to run single scenarios or the golden dataset
│
├── tests/
│   └── golden_dataset/
│
└── examples/
