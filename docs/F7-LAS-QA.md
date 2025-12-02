# F7-LAS™ — Questions & Answers

## 1. What is F7-LAS™?

F7-LAS™ (Fuller 7-Layer Agentic Security) is a conceptual security model for AI agents that don’t just chat, but take actions via tools, APIs, and workflows.

It defines seven layers – from system prompts and grounding, through planners and tools, to policy engines, sandboxes, and monitoring – to help architects reason about and reduce operational risk in agentic AI systems.

## 2. Is this a runtime or a reference model?

F7-LAS is primarily a **reference security model** with supporting examples.

The repository currently provides:

- The whitepaper and implementation guide.
- Example prompts, grounding profiles, and tool schemas.
- A Stage-1 Policy Engine (Layer 5) pattern using PDP/PEP.
- Example vendor policies (OPA/Rego, Cedar, Sentinel, Kyverno, etc.).
- A lightweight sandbox and telemetry stubs.

It is **not** a full production agent framework.

## 3. What problem does F7-LAS try to solve?

Most AI security discussions stop at:

- “We added a system prompt.”
- “We added RAG.”

That mainly addresses **content quality**, not **operational risk**.

F7-LAS focuses on **action-taking systems**:

- Agents that can modify infrastructure.
- Tools that can change configuration.
- Automation that can impact production.

The model gives a structured way to ask: *“If this agent goes wrong, how far can it go, and what stops it?”*

## 4. How does F7-LAS relate to NIST AI RMF, ISO/IEC 42001, or MITRE ATLAS?

Those frameworks define **governance, risk, and high-level controls**.

F7-LAS focuses on **technical architecture** for agentic systems and can sit underneath them as an implementation lens:

- NIST AI RMF / ISO 42001 → “What do we need?”
- F7-LAS → “How do we wire prompts, tools, policies, and sandboxes to enforce it?”
- MITRE ATLAS → “Which attack patterns do we simulate against each layer?”

## 5. Why seven layers?

The layers separate **concerns and control planes**:

1. System Prompt – soft policy / intent.
2. Grounding (RAG) – epistemic guardrail.
3. Planner / Controller – decision logic and tool orchestration.
4. Tools & Integrations – action surface (APIs, workflows).
5. Policy Engine – external, hard guardrails (PDP/PEP).
6. Sandboxed Environment – blast radius control.
7. Monitoring & Telemetry – detection and assurance.

This mirrors how traditional security models separate identity, policy, enforcement, and environment.

## 6. What is the most critical layer?

From a hard security perspective: **Layer 5 (Policy Engine)** and **Layer 6 (Sandbox)**.

- L5 ensures that **no tool call bypasses policy** (PDP/PEP).
- L6 ensures that **even if something goes wrong, impact is bounded**.

Prompts and RAG matter, but they are not sufficient to protect real systems.

## 7. What does the Stage-1 implementation include?

The Stage-1 code includes:

- Layer-1 example prompts for multiple agents (investigator, coordinator, remediator).
- Layer-2 grounding allowlist and profiles.
- Layer-3 simple planner stub.
- Layer-4 stub tool client (e.g., `aws_ec2_client_stub`).
- Layer-5 Policy Engine pattern with:
  - A vendor-neutral PEP abstraction.
  - An OPA/Rego PDP demo.
  - Example policies for OPA, Cedar, Sentinel, Kyverno, SpiceDB (conceptual).
- Layer-6 sandbox stub via `docker-compose` (isolated network).
- Layer-7 telemetry schema and JSON logger.

## 8. Is the code production-ready?

No. The repo is **Stage-1 / Prototype**:

- Policies are minimal examples.
- Sandboxing is a simple container boundary.
- Telemetry is a basic JSON logger.
- CI is oriented around structure/validation, not full runtime validation.

It is intended for **learning, design reviews, and experimentation**, not direct deployment into critical environments.

## 9. How should practitioners use F7-LAS today?

Typical uses:

- As a **checklist** during design or threat modeling for agentic systems.
- As a **review lens**: “What controls do we have at each layer?”
- As a **teaching and workshop tool** to explain agent security to engineers.
- As a **starting point** for building internal patterns, guardrails, and policies.

## 10. Is this affiliated with Microsoft?

No.

F7-LAS is an **independent project** created by the author.  
It is **not** affiliated with, endorsed by, or associated with Microsoft or any other employer.

All opinions, diagrams, and implementations are personal and do not represent any company.

## 11. How can the community contribute?

Contributions are welcome across:

- Improved example policies (OPA, Cedar, Sentinel, Kyverno, etc.).
- Additional Layer-6 sandbox patterns (e.g., microVMs, stricter containers).
- Enhanced planners, tools, and evaluation harnesses.
- Threat scenarios mapped to specific layers.
- Documentation and diagrams.

See `CONTRIBUTING.md` (when available) or open a GitHub issue to discuss ideas.
