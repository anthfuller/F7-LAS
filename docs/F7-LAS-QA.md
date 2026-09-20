# F7-LAS Questions, Answers, and Current Maturity

## What is F7-LAS?

F7-LAS™ (Fuller 7-Layer Agentic Security) is Anthony Fuller's vendor-neutral, protocol-agnostic security model for agentic AI systems. It separates soft policy, grounding, planning, proposed tool use, external policy enforcement, containment, and assurance.

## Is it a runtime or product?

No. F7-LAS is an engineering and governance reference model. This repository contains a **prototype reference implementation**, illustrative material, and draft guidance. It is not a production agent platform, SOC product, SIEM/SOAR replacement, or autonomous-response control plane.

## What is the current implementation maturity?

**Prototype reference implementation.** The repository contains one coherent,
tested, synthetic and offline Layers 1–7 execution path. It demonstrates a
bounded Python + OPA flow; it does not make the broader illustrative code
executable or production-ready. The existing golden-dataset evaluator validates
scenario and rubric structure; it does not execute or prove the stated security
behavior.

The canonical path has automated behavioral checks, but repository-wide control
status is not yet machine-readable or evidence-linked.

## Is the code production-ready?

No. Current planners, tools, sandboxing, telemetry, and policy adapters are incomplete or illustrative prototypes. Do not connect them to production data, accounts, identities, cloud resources, security platforms, or remediation systems.

## What is canonical?

The seven-layer model and whitepaper v3.0 are the design baseline. The canonical
executable path is the offline, deterministic Python + OPA workflow under
[`examples/canonical-workflow/`](../examples/canonical-workflow/README.md).
Other policy-engine examples remain non-canonical illustrative patterns unless
explicitly reclassified later.

## How does approval work in the canonical path?

The canonical path creates deterministic synthetic approval evidence bound to
the exact request and action references and digests, arguments, complete scope,
complete policy reference, approving authority, and validity window. Approval
returns through OPA evaluation and independent executor enforcement; it never
bypasses policy or invokes a tool directly. This demonstrates the binding and
enforcement pattern, not an interactive human-approval service or proof that a
real person's identity was verified.

## How are Layer 4 and Layer 6 separated?

Layer 4 defines and validates proposed tool requests and the external action
surface. A proposal is data, not authority. Layer 5 authorizes or denies it at
PDP/PEP boundaries. The current Layer 6 demonstration is a synthetic in-process
executor that makes no network calls; it is not an OS/container sandbox or an
enforced network-isolation boundary.

## Does F7-LAS expose internal model reasoning?

No. Architecture and evidence use auditable plans, decisions, source references, proposed actions, policy outcomes, approvals, results, and evaluations. Private chain-of-thought is neither required nor treated as an audit artifact.

## What is Layer S?

Layer S is a cross-cutting software supply-chain control domain. It is not an eighth layer and does not change the fundamental seven-layer model.

## How should practitioners use the repository today?

Use it as a design-review lens, threat-modeling aid, draft control catalog, and source of clearly labeled examples. Verify each claimed outcome independently before adapting any pattern.

## How are artifacts versioned?

- Whitepaper: v3.0, immutable historical artifact.
- Control catalog: v0.1 draft.
- Implementation guide: draft; version assigned at reviewed release.
- Reference code: prototype; intended to follow the future repository 4.0.0 release.
- Individual schemas: independently versioned.

Repository release numbers do not silently revise the whitepaper or other artifacts.

## Is this affiliated with Microsoft?

No. F7-LAS is independent personal work by Anthony L. Fuller and is not affiliated with, endorsed by, or representative of Microsoft or any other employer.

## Where are licensing and citation details?

See [LICENSE.md](../LICENSE.md), [LICENSE-CONTENT.md](../LICENSE-CONTENT.md), [LICENSE-CODE](../LICENSE-CODE), and [CITATION.cff](../CITATION.cff). Copyright licensing does not grant F7-LAS trademark rights or imply endorsement.
