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

See `CONTRIBUTING.md` or open a GitHub issue to discuss ideas.

# F7-LAS™ — Expert Q&A (Top 20)

1. **Is F7-LAS just a restatement of POMDP/PEAS in security terms?**  
No. F7-LAS uses PEAS/POMDP as a conceptual backbone, but it focuses on **where and how to place controls** (prompts, grounding, planners, tools, policy engines, sandboxes, telemetry) in real systems. It is a **control decomposition**, not a purely mathematical model.

2. **How is this different from NIST AI RMF or ISO/IEC 42001?**  
Those frameworks define **governance and risk management**. F7-LAS is a **technical architecture lens** for agentic AI – it tells you how to organize prompts, tools, policies, and sandboxes to enforce those high-level requirements.

3. **How does F7-LAS relate to MITRE ATLAS?**  
ATLAS describes **attack techniques** against AI. F7-LAS provides the **layered surfaces and controls** you can map those techniques onto. Think: ATLAS = “what might the attacker do,” F7-LAS = “which layer should catch or limit it.”

4. **Why is Layer 5 (Policy Engine) outside the LLM?**  
To avoid **prompt-injection and generative bypass** of security policy. The PDP/PEP pattern ensures that all tool calls go through a **deterministic policy engine**, independent of the model’s text output.

5. **Can I use a different policy engine (not OPA)?**  
Yes. The repo shows patterns with OPA/Rego, but also conceptual examples for Cedar, Sentinel, Kyverno, and SpiceDB. Layer 5 is explicitly **vendor-neutral** as long as you can implement PDP/PEP semantics.

6. **How does F7-LAS help with multi-agent systems?**  
Each agent gets its own L1–L5 configuration (prompt, grounding, planner settings, tools, policies). L6–L7 provide **shared environment and telemetry**, preventing uncontrolled privilege sharing between agents.

7. **Does F7-LAS require a particular orchestration framework (LangChain, Semantic Kernel, etc.)?**  
No. It’s agnostic. Whatever framework you use, F7-LAS says:  
- Don’t let the orchestrator call tools directly without L5.  
- Don’t run tools in an unbounded environment without L6.  

8. **How do you handle RAG poisoning in Layer 2?**  
Layer 2 assumes **governed, allowlisted sources** and uses schemas/allowlists under `config/`. F7-LAS doesn’t solve poisoning by itself, but it forces you to separate and govern **what the agent is allowed to read and trust**.

9. **What about tool compromise in Layer 4?**  
L4 is treated as the **action surface**. Tool compromise is mitigated by:  
- L5 – policy constraints on actions and parameters,  
- L6 – sandboxed execution and least privilege,  
- L7 – telemetry to detect misuse.

10. **Is there any formal verification in F7-LAS?**  
Not in Stage-1. However, engines like **Cedar** and **OPA** can support more formal analysis of policies. F7-LAS encourages, but does not yet implement, model checking or formal proofs.

11. **How does this model handle human-in-the-loop approvals?**  
Layer 5 policies can return decisions like “allow-with-approval.” The planner or orchestrator must then pause, collect human approval, and re-submit the action with proof, which L5 can validate.

12. **Can I plug this into existing SOC tooling (XDR, SIEM)?**  
Layer 7 is designed with that in mind: telemetry schemas can be forwarded to SIEM/XDR. Stage-1 only includes a JSON logger, but the pattern is compatible with downstream integrations.

13. **What are the key metrics for evaluating F7-LAS deployments?**  
Examples:  
- % of tool calls blocked or modified by L5.  
- Number of sandbox-escaped vs sandbox-contained incidents.  
- Coverage of tools by allowlists/policies.  
- Alignment of logged behavior with defined policies over time.

14. **Is there any evaluation harness for attack simulation?**  
Not yet fully implemented. Stage-1 focuses on scaffolding (policies, planner stub, tools). Future stages could integrate ATLAS-style evaluation scenarios.

15. **How does F7-LAS handle identity and authentication?**  
Identity is an input to Layer 5 decisions (e.g., `user_role`, `agent_id`). F7-LAS assumes standard identity and access management, and uses those attributes in PDP rules.

16. **Why doesn’t the repo ship a full production agent?**  
On purpose. The goal is to provide **patterns, not a black-box product**. Every organization has different constraints, stacks, and risk tolerances. F7-LAS is meant to be adapted.

17. **Is this compatible with Retrieval-Augmented Generation + tool use stacks?**  
Yes. L1–L2 cover prompt and retrieval, L3–L4 cover planner and tools, L5–L7 cover enforcement, environment, and telemetry. The design assumes RAG+tools as a default pattern.

18. **Can I adopt only some layers?**  
Yes – but you lose defense-in-depth. Many teams start by adding explicit Layer-5 and Layer-7 controls around an existing L3/L4 stack.

19. **Is there any licensing constraint on using the model?**  
The repo and docs are licensed under **CC BY 4.0**. The model itself (F7-LAS™) is a trademark of the author. See the main `README.md` for full license and disclaimer details.

20. **What is the long-term vision for this project?**  
To evolve from a conceptual model + examples into a **widely-used reference architecture** for securing agentic systems, with:  
- richer policies,  
- better sandbox patterns,  
- evaluation harnesses,  
- and community-driven extensions.

