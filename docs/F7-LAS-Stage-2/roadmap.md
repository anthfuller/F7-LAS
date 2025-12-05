### 📘 F7-LAS™ Stage-2 Roadmap  
*(2025 Engineering Expansion — Prototype → Beta Transition)*

#### Overview
Stage-2 evolves F7-LAS™ from a conceptual + prototype model into an **engineering-ready security architecture for agentic AI**.

Stage-2 goals:

- Strengthen **runtime security controls**
- Expand **planning → policy → sandbox → telemetry**
- Align with **external research** while remaining vendor-neutral
- Deliver a working **L1→L7 demo agent** with full auditing

---

#### Stage-2 Priorities

| ID   | Focus                 | Outcome                                                |
|------|-----------------------|--------------------------------------------------------|
| P1   | Runtime Security Path | Policy-mediated actions with sandbox isolation         |
| P2   | Governance Expansion  | Updated control catalog, metrics, misuse cases         |
| P3   | Stage-2 Demo Agent    | Fully auditable execution of all seven layers         |

---

#### Layer-by-Layer Enhancements

| Layer | Upgrade Focus                                      |
|-------|----------------------------------------------------|
| L1    | PSP schema v2 + soft policy threat cases           |
| L2    | Provenance logging + retrieval risk scoring        |
| L3    | Safe-step sequencing + privilege escalation checks |
| L4    | Tool capability classes + input/output sanitizers  |
| L5    | Risk scoring + cross-tool dependency rules         |
| L6    | Sandbox profiles + quotas + network controls       |
| L7    | Execution trace v2 + drift/anomaly detection       |

---

#### Alignment with MCP Whitepaper (Vendor-Neutral)

| MCP Capability              | F7-LAS Mapping                        |
|----------------------------|----------------------------------------|
| Tool capability boundaries | L4 capability classes                 |
| Policy enforcement gateway | L5 PEP before every tool call         |
| Action logs & traceability | L7 structured telemetry               |
| Controlled action surfaces | L6 sandbox isolation profiles         |
| Tool vetting               | Layer-S supply-chain + allowlist      |

> A separate document (`mcp-alignment.md`) will hold the detailed mapping.

---

#### Stage-2 Deliverables

- **D1 — Control Catalog v0.3**  
  Updated controls reflecting Stage-2 runtime and governance work.

- **D2 — Stage-2 Demo Agent**  
  Minimal, end-to-end agent executing:  
  `prompt → grounding → planning → policy → sandboxed tools → telemetry`.

- **D3 — MCP Alignment Addendum**  
  Short, vendor-neutral alignment note showing how F7-LAS incorporates ideas from MCP-style architectures.

- **D4 — Architecture Diagrams v2**  
  - Execution Control Loop  
  - Tool Gateway Flow  
  - Planner Guardrail Flow  
  - Sandbox Profiles

---

#### Milestone Timeline (6 Weeks)

| Week  | Work Focus                                      |
|-------|-------------------------------------------------|
| 1–2   | L3 planner, L4 tools, L5 policy expansion       |
| 3     | Sandbox profiles (L6) + telemetry model (L7 v2) |
| 4     | Stage-2 Demo Agent implementation               |
| 5     | Stage-2 release (v3.5 or v4.0)                  |
| 6     | Slides + write-up + community announcement      |

---

#### Guiding Principles

- **Vendor-neutral**  
- **Security-first** for every agent action path  
- **Transparent & versioned** maturity stages  
- **Research-aligned**, but not dependent on any single paper  
- **Practical for engineering teams** to adopt and adapt  

---

**Status:** Stage-2 → _In Progress_  
_File maintained in:_ `docs/F7-LAS-Stage-2/roadmap.md`
