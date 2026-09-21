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

The canonical path has automated behavioral checks, evidence verification,
deterministic replay, and a clean-user acceptance gate. The
[machine-readable traceability file](../config/control-traceability.json) covers
all 46 core Layers 1–7 controls plus five supplemental Layer S controls and
records implemented, partial, or not-implemented status, limitations, and
verifiable repository evidence locators. Its status is scoped to this bounded
repository implementation, not to a production deployment.

## Is the code production-ready?

No. Current planners, tools, sandboxing, telemetry, and policy adapters are incomplete or illustrative prototypes. Do not connect them to production data, accounts, identities, cloud resources, security platforms, or remediation systems.

## What is canonical?

The seven-layer model and current Whitepaper v4.0 are the design baseline.
Whitepaper v3.0 remains an immutable historical artifact. The canonical
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

## How should the architecture diagrams be interpreted?

The [architecture diagrams](architecture-diagrams.md) describe F7-LAS control
responsibilities and the governed execution flow. They are not deployment
diagrams or proof that a control is implemented. Layer numbers identify control
domains rather than a universally linear runtime order: a Layer 4 action is
proposed before Layer 5 authorization, while actual Layer 4 tool access is
allowed only after permit and within the applicable Layer 6 boundary. The
diagram guide maps every visual stage to the bounded canonical implementation
and states the unimplemented production boundaries.

## What do evidence verification and replay prove?

The canonical verifier independently checks the complete record chain,
cross-record bindings, the policy-bundle digest covering metadata and exact
executable Rego bytes, action digests, and final audit correlation. The OPA
adapter verifies that bundle reference before executing the policy.
Deterministic replay reruns the same admitted input through the synthetic
workflow and requires the complete canonical evidence document to match. These
checks detect inconsistent mutation, and a previously trusted evidence-set
digest exposes later replacement. Replay reproduces this bounded outcome. The
checks do not provide a digital signature, trusted timestamp, external
attestation, or replay of real-world side effects.

## Does F7-LAS expose internal model reasoning?

No. Architecture and evidence use auditable plans, decisions, source references, proposed actions, policy outcomes, approvals, results, and evaluations. Private chain-of-thought is neither required nor treated as an audit artifact.

## What is Layer S?

Layer S is a cross-cutting software supply-chain control domain. It is not an eighth layer and does not change the fundamental seven-layer model.

## Which Layer S controls are implemented in this repository?

The canonical CI installs a fully resolved, SHA-256-hashed Python lock, pins
external GitHub Actions to full commit SHAs, verifies downloaded OPA and
Gitleaks binaries against fixed SHA-256 values, scans the Git history for
recognized secret patterns, checks the locked Python graph for published known
vulnerabilities, and retains a CycloneDX JSON SBOM for 30 days. Dependabot is
configured to propose weekly Python and GitHub Actions updates for review.

These controls cover the repository's Python CI environment and the two
downloaded Linux binaries. They do not attest the GitHub-hosted runner image,
prove that dependencies are non-malicious, guarantee that no secret exists, or
create a signed release SBOM or provenance attestation. See
[Supply-chain and CI controls](supply-chain-and-ci.md) for the exact boundary.

## Has the documented canonical path been tested as a clean user?

Yes, within a deliberately narrow boundary. The
[clean-user acceptance gate](clean-user-acceptance.md) copies the repository
without Git metadata, removes inherited Python import settings, creates a new
Python 3.12.14 virtual environment, performs a hash-locked installation, and
runs the supported validation and canonical walkthrough commands with the
checksum-verified OPA 1.20.2 binary. It does not test the illustrative layer
examples or establish production readiness.

## How should practitioners use the repository today?

Use it as a design-review lens, threat-modeling aid, draft control catalog, and source of clearly labeled examples. Verify each claimed outcome independently before adapting any pattern.

## How are artifacts versioned?

- Whitepaper: v4.0, current publication; v3.0 is preserved as an immutable
  historical artifact.
- Control catalog: v0.1 draft.
- Implementation guide: draft; bundled with repository release v4.0.0 but not
  independently versioned.
- Reference code: prototype published in tagged repository release v4.0.0.
- Individual schemas: independently versioned.

Repository release v4.0.0 and Whitepaper v4.0 are independently versioned.
Whitepaper v4.0 was published separately and is not part of the immutable
v4.0.0 tag. Repository release numbers do not silently revise a whitepaper or
other artifact.

## Is this affiliated with Microsoft?

No. F7-LAS is independent personal work by Anthony L. Fuller and is not affiliated with, endorsed by, or representative of Microsoft or any other employer.

## Where are licensing and citation details?

See [LICENSE.md](../LICENSE.md), [LICENSE-CONTENT.md](../LICENSE-CONTENT.md), [LICENSE-CODE](../LICENSE-CODE), and [CITATION.cff](../CITATION.cff). Copyright licensing does not grant F7-LAS trademark rights or imply endorsement.
