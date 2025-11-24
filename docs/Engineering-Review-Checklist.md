# F7-LAS Engineering Review Checklist

**Purpose:**  
Use this checklist to assess whether an agentic or multi-agent AI system implementation conforms to the F7‑LAS (Fuller 7‑Layer Agentic AI Security) model.

**How to use:**  
- Complete this checklist during **architecture/design review**, **pre‑production go‑live**, and after **material changes**.  
- For each item, mark: ✅ **Yes** / ⚠️ **Partial** / ❌ **No** / N/A.  
- Capture findings and actions in your internal tracking system (e.g., GitHub issues, Azure Boards, Jira).  

---

## Project Metadata

- **System / Project Name:** ________________________________
- **Owner / Team:** ________________________________________
- **Reviewer(s):** _________________________________________
- **Date of Review:** ______________
- **Agent Runtime / Framework (e.g., LangGraph, AutoGen):** ______________________
- **Deployment Environment(s):** ____________________________

---

## Legend

- ✅ = Fully implemented / satisfactory  
- ⚠️ = Partially implemented / needs work  
- ❌ = Missing / not implemented  
- N/A = Not applicable to this system  

You may optionally assign **risk levels** (Low / Medium / High) per item.

---

## Layer 1 – System Prompt (Soft Policy)

**Goal:** Agent roles, boundaries, and safety posture are clearly defined and under change control.

| ID | Checklist Item | Status | Notes / Actions |
|----|----------------|--------|-----------------|
| L1.1 | Each agent has a clearly defined **role** and **scope** in its system prompt (e.g., Coordinator, Investigator, Remediator). |  |  |
| L1.2 | Prompts explicitly state what the agent **must not do** (e.g., no direct remediation, no policy overrides). |  |  |
| L1.3 | Prompts include **abstain / escalate** instructions when the agent is uncertain or out of scope. |  |  |
| L1.4 | System prompts are stored in a **version-controlled location** (e.g., repo, config store). |  |  |
| L1.5 | Changes to prompts follow a **formal change-control process** (review + approval). |  |  |
| L1.6 | Prompts have undergone **prompt-injection and jailbreak testing**. |  |  |

---

## Layer 2 – Grounding / RAG (Epistemic Guardrail)

**Goal:** Retrieved knowledge is curated, access-controlled, and not treated as a hard security boundary.

| ID | Checklist Item | Status | Notes / Actions |
|----|----------------|--------|-----------------|
| L2.1 | All RAG sources are **enumerated and documented** (indexes, databases, APIs). |  |  |
| L2.2 | RAG sources are **access-controlled** (auth, roles, network controls). |  |  |
| L2.3 | There is a process to **curate and retire** knowledge (removal of stale or risky content). |  |  |
| L2.4 | Controls exist to detect or prevent **RAG poisoning** (e.g., restricted authors, approval for new content). |  |  |
| L2.5 | Retrieved content is treated as **untrusted input**; no direct execution of instructions from RAG. |  |  |
| L2.6 | RAG has been tested for **prompt injection through retrieved text**. |  |  |

---

## Layer 3 – Agent Planner / Controller

**Goal:** Planning logic (single or multi-agent) is bounded, observable, and aligned with policy.

| ID | Checklist Item | Status | Notes / Actions |
|----|----------------|--------|-----------------|
| L3.1 | The main planning component(s) (e.g., Supervisor / Router) are **identified and documented**. |  |  |
| L3.2 | Maximum **step count / recursion depth / wall‑clock time** for agent loops is enforced. |  |  |
| L3.3 | The planner has explicit **stop conditions** (e.g., success, failure, timeout, escalation). |  |  |
| L3.4 | Planning logic is tested for **goal/role drift** and unsafe routing decisions. |  |  |
| L3.5 | For multi-agent systems, **delegation rules** between agents are documented. |  |  |
| L3.6 | Planner outputs are captured in logs for **post‑incident analysis**. |  |  |

---

## Layer 4 – Tools & Integrations (Action Surface)

**Goal:** All tools are cataloged, least‑privilege, and risk‑tiered; read/write separation is enforced.

| ID | Checklist Item | Status | Notes / Actions |
|----|----------------|--------|-----------------|
| L4.1 | A **tool catalog** exists listing every tool/API/connector the agent(s) can call. |  |  |
| L4.2 | Each tool is assigned a **risk tier** (e.g., Tier 1 = read‑only, Tier 2 = low‑impact writes, Tier 3 = high‑impact writes). |  |  |
| L4.3 | Read‑only tools are strictly separated from write / state‑changing tools. |  |  |
| L4.4 | Each agent is granted access only to the **minimum set of tools** needed for its role. |  |  |
| L4.5 | Credentials / identities used by tools follow **least privilege** and **rotation** best practices. |  |  |
| L4.6 | All tool calls are **logged with agent identity, parameters (redacted as needed), and outcome**. |  |  |

---

## Layer 5 – Policy Engine Outside the LLM (Hard Guardrails)

**Goal:** All high‑impact actions are mediated by an external Policy Decision Point (PDP) and Policy Enforcement Point (PEP).

| ID | Checklist Item | Status | Notes / Actions |
|----|----------------|--------|-----------------|
| L5.1 | A **PDP/PEP architecture** is implemented outside the LLM / agent runtime. |  |  |
| L5.2 | All tool calls (or all Tier 2+ tools at minimum) go through a **PEP** for authorization. |  |  |
| L5.3 | Policies are expressed as **policy-as-code** (e.g., OPA, Rego, YAML, custom rules) and are version-controlled. |  |  |
| L5.4 | PDP decisions support at least: **Allow, Deny, Allow-with-Obligations, Escalate-to-Human**. |  |  |
| L5.5 | High‑impact actions (e.g., isolation, account disable) require **additional conditions** (e.g., severity, confidence, asset class). |  |  |
| L5.6 | Where required, PDP enforces **human‑in‑the‑loop approval** (human token, workflow ID, etc.). |  |  |
| L5.7 | Policy changes follow **formal review and testing** before deployment. |  |  |
| L5.8 | PDP/PEP events are logged for **audit and forensics**. |  |  |

---

## Layer 6 – Sandboxed Execution Environment (Blast Radius Control)

**Goal:** The runtime environment strictly limits what the agent can reach and change.

| ID | Checklist Item | Status | Notes / Actions |
|----|----------------|--------|-----------------|
| L6.1 | Agent runtime executes in a **segmented environment** (e.g., dedicated tenant/account/subscription). |  |  |
| L6.2 | Network access is restricted via **VNET/VPC, firewalls, private endpoints**, etc. |  |  |
| L6.3 | Separate environments exist for **development, testing, and production** with clear promotion paths. |  |  |
| L6.4 | For security use cases, an explicit **boundary** exists between read‑only “investigation” and write‑capable “remediation” environments. |  |  |
| L6.5 | Each agent has a **separate identity / role** (e.g., Coordinator vs Investigator vs Remediator) with distinct permissions. |  |  |
| L6.6 | There is a defined **blast‑radius statement** (what the agent *could* change at worst) and it is acceptable to stakeholders. |  |  |
| L6.7 | Configuration drift in the sandbox (e.g., widened permissions) is monitored and alerted on. |  |  |

---

## Layer 7 – Monitoring & Evaluation (Detection & Assurance)

**Goal:** Agent behavior, tool usage, and policy decisions are observable, measured, and continuously improved.

| ID | Checklist Item | Status | Notes / Actions |
|----|----------------|--------|-----------------|
| L7.1 | A **telemetry schema** exists for logging prompts, planner outputs, tool calls, and PDP decisions. |  |  |
| L7.2 | Telemetry is ingested into a **central monitoring platform** (e.g., SIEM/XDR). |  |  |
| L7.3 | There are **detection rules** for anomalous agent behavior (e.g., spikes in denied actions, unusual tool usage). |  |  |
| L7.4 | The system is tested against **MITRE ATLAS‑inspired attack scenarios** (prompt injection, tool abuse, RAG poisoning). |  |  |
| L7.5 | Results from red‑team exercises are captured and used to **update prompts, policies, and sandboxing**. |  |  |
| L7.6 | KPIs / SLOs exist for agent safety and are periodically reviewed (e.g., rate of blocked high‑risk actions, MTTR for incidents). |  |  |
| L7.7 | There is a defined **incident response playbook** specific to agentic AI failures or misuse. |  |  |

---

## Multi-Agent Governance (If Applicable)

**Goal:** Multi-agent interactions are governed, observable, and aligned with separation of duties.

| ID | Checklist Item | Status | Notes / Actions |
|----|----------------|--------|-----------------|
| MA.1 | Each agent in the multi-agent system has a **documented role** (e.g., Coordinator, Investigator, Remediator). |  |  |
| MA.2 | **Delegation paths** (who can call whom) are explicitly documented and enforced (e.g., via tools or policy). |  |  |
| MA.3 | Cross-agent interactions (e.g., Coordinator → Remediator) are treated as **tool calls** subject to Layer‑5 policy. |  |  |
| MA.4 | Telemetry allows **correlation across agents** for a single task/incident. |  |  |
| MA.5 | Separation of duties is preserved (e.g., investigative agents cannot directly remediate). |  |  |

---

## Overall Assessment

- **Overall F7‑LAS Alignment Rating (1–5):** ______  
- **Key Risks Identified:**  
  1. _______________________________________________  
  2. _______________________________________________  
  3. _______________________________________________  

- **Required Remediation Actions / Owners:**  
  - Action: ___________________________  Owner: ______________  Target Date: __________  
  - Action: ___________________________  Owner: ______________  Target Date: __________  

---

> Save this checklist together with your architecture decision records (ADRs), risk assessments, and model documentation as evidence of F7‑LAS application.

© 2025 Anthony L. Fuller. All rights reserved.

This work is created independently by the author and is not affiliated with,
endorsed by, or associated with Microsoft or any other employer. All opinions,
models, and materials represent the author's personal work.

