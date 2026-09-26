# F7-LAS™ — Fuller 7-Layer Agentic Security

[![CI](https://github.com/anthfuller/F7-LAS/actions/workflows/f7las-ci.yml/badge.svg)](https://github.com/anthfuller/F7-LAS/actions/workflows/f7las-ci.yml)
[![Current whitepaper](https://img.shields.io/badge/whitepaper-v4.1-blue.svg)](docs/whitepaper/F7-LAS-Whitepaper-v4.1-Restored-Full-Edition.pdf)
![maturity](https://img.shields.io/badge/implementation-prototype-yellow)

> **Current status:** Established reference model with a **prototype reference implementation**. The repository is not a production agent platform, control plane, SOC product, SIEM/SOAR replacement, or production-ready implementation.

Whitepaper version **4.1 — Restored Full Edition** is the current repository
whitepaper and is distinct from repository release **v4.0.0**. It restores the
complete long-form v3.0 coverage with the corrected canonical control-loop
diagrams and their execution semantics. The v3.0 and v4.0 publications remain
historical records; the v4.0 Zenodo DOI identifies only that historical edition.

F7-LAS™ is Anthony Fuller's vendor-neutral, protocol-agnostic security model for designing, reviewing, and governing agentic AI systems. It separates security responsibilities across seven layers so that generative output is not treated as authority to act.

This is independent personal work. It is not affiliated with, endorsed by, or representative of Microsoft or any other employer.

## The seven layers

| Layer | Control concern |
|---|---|
| 1 | System Prompt — soft-policy intent and role boundaries |
| 2 | Grounding / RAG — source and epistemic constraints |
| 3 | Planner / Controller — bounded planning and delegation |
| 4 | Tools & Integrations — proposed action surface and argument contracts |
| 5 | External Policy Engine — deterministic PDP/PEP guardrails |
| 6 | Sandboxed Execution — scope and blast-radius containment |
| 7 | Monitoring & Evaluation — correlated evidence and assurance |

Software supply-chain security is a cross-cutting supplemental domain, **Layer S**; it is not an eighth F7-LAS layer.

## What is in this repository now

- The current [F7-LAS Whitepaper v4.1 — Restored Full Edition](docs/whitepaper/F7-LAS-Whitepaper-v4.1-Restored-Full-Edition.pdf)
  and its [SHA-256 checksum](docs/whitepaper/F7-LAS-Whitepaper-v4.1-Restored-Full-Edition.sha256)
- The historical [v4.0 whitepaper](docs/whitepaper/F7-LAS-Whitepaper-v4.0.pdf),
  published at [10.5281/zenodo.22867553](https://doi.org/10.5281/zenodo.22867553)
- The immutable historical [F7-LAS whitepaper v3.0](docs/F7-LAS-model-whitepaper_v3.0.pdf)
- A draft [implementation guide](docs/f7-las-implementation-guide/README.md)
- A draft catalog of [46 core Layers 1–7 controls plus five supplemental Layer S controls](docs/F7-LAS-Control-Catalog-v0.1.md)
- Current [architecture diagrams](docs/architecture-diagrams.md), with explicit implementation boundaries, and engineering review material
- Canonical v1.0.0 data contracts and one synthetic, offline Python + OPA workflow
- Illustrative prompts, additional policies, validators, and runtime stubs
- Supply-chain CI, behavioral tests, evidence verification, deterministic replay,
  and a clean-user acceptance gate for the canonical path
- Machine-readable [control-to-evidence traceability](config/control-traceability.json)
  covering all 51 catalog controls

The canonical workflow provides one deliberately constrained executable Layers 1–7 path. It does not make the other examples executable or production-ready. The behavioral scenario matrix exercises the canonical enforcement path; the separate golden-dataset runner validates scenario structure and does not prove the described allow/deny behavior. Non-canonical examples remain illustrative unless they are explicitly reclassified and tested.

## Executable versus illustrative

| Repository area | Current classification |
|---|---|
| Validation scripts | Executable structural validation |
| Canonical Python + OPA path | Executable for one synthetic, offline, read-only action |
| Other OPA/PDP/PEP code | Partial prototype |
| Planner, tools, sandbox, telemetry | Illustrative prototypes |
| Other policy-engine examples | Illustrative, non-canonical patterns |
| Other end-to-end workflows | Not provided |
| Production integrations or actions | Not provided |

Nothing in this repository should be connected to production data, identities, cloud resources, security platforms, or remediation systems without independent engineering and security review.

## Validate the current repository

The canonical code supports Python 3.10 or later. To reproduce the CI dependency
environment, use Python 3.12.14 in an isolated environment and install the
hash-locked file:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --require-hashes -r requirements-ci.lock
python scripts/validate-supply-chain.py
python scripts/validate-documentation.py
python scripts/validate-citation.py
python scripts/validate-control-traceability.py
python scripts/validate-prompts.py
python scripts/validate-policies.py
python scripts/allowlist-validator.py
python scripts/validate-settings.py config/settings.yaml
python scripts/validate-contracts.py
opa check --strict config/policies/canonical-workflow.rego
python -m pytest -q
```

These commands validate the **current prototype and repository structure**. They are not evidence of production readiness or full behavioral enforcement.

## Start here

- [Documentation index](docs/README.md)
- [Current Whitepaper v4.1 — Restored Full Edition](docs/whitepaper/F7-LAS-Whitepaper-v4.1-Restored-Full-Edition.pdf)
- [Whitepaper v4.1 SHA-256 checksum](docs/whitepaper/F7-LAS-Whitepaper-v4.1-Restored-Full-Edition.sha256)
- [Historical Whitepaper v4.0](docs/whitepaper/F7-LAS-Whitepaper-v4.0.pdf) and [its historical DOI](https://doi.org/10.5281/zenodo.22867553)
- [Historical Whitepaper v4.0 checksum](docs/whitepaper/F7-LAS-Whitepaper-v4.0.sha256)
- [Historical Whitepaper v3.0 artifact record](docs/whitepaper-v3.0-artifact.md)
- [Implementation guide](docs/f7-las-implementation-guide/README.md)
- [Control catalog v0.1](docs/F7-LAS-Control-Catalog-v0.1.md)
- [Engineering review checklist](docs/Engineering-Review-Checklist.md)
- [Current QA and maturity statement](docs/F7-LAS-QA.md)
- [Canonical data contracts v1.0.0](schemas/contracts/README.md)
- [Canonical offline workflow](examples/canonical-workflow/README.md)
- [Supply-chain and CI controls](docs/supply-chain-and-ci.md)
- [Clean-user acceptance](docs/clean-user-acceptance.md)
- [Architecture diagrams](docs/architecture-diagrams.md)
- [Control-to-evidence traceability](config/control-traceability.json)
- [v4.0.0 release notes](RELEASE_NOTES.md)
- [Release and exact-tag SBOM procedure](docs/release-process.md)
- [Roadmap](ROADMAP.md)
- [Security policy](SECURITY.md)

## Version and maturity boundaries

Versions belong to individual artifacts:

| Artifact | Current version/status |
|---|---|
| Seven-layer model | Established design baseline |
| Whitepaper | v4.1 — Restored Full Edition, current repository edition; v3.0 and v4.0 preserved as historical artifacts |
| Implementation guide | Draft; bundled with 4.0.0 but not independently versioned |
| Control catalog | v0.1 draft |
| Executable reference implementation | Prototype included in repository release v4.0.0 |
| Repository release | v4.0.0, independently versioned from Whitepaper v4.1 |

Repository version numbers do not silently change the whitepaper, control catalog, or schema versions.

## Licensing, trademark, and attribution

- Documentation, diagrams, the model, and other authored content are licensed under [CC BY 4.0](LICENSE-CONTENT.md).
- Executable source code and policy/configuration examples are licensed under the [MIT License](LICENSE-CODE).
- [LICENSE.md](LICENSE.md) defines the file-level boundary for mixed directories.
- F7-LAS™ is a trademark of Anthony L. Fuller. Copyright licenses do not grant trademark rights or imply endorsement.

Preferred citation metadata for the current repository edition is in
[CITATION.cff](CITATION.cff). No DOI is assigned to Whitepaper v4.1. The
[10.5281/zenodo.22867553](https://doi.org/10.5281/zenodo.22867553) DOI
identifies only the historical Whitepaper v4.0 publication. Historical
Whitepapers v3.0 and v4.0 remain preserved unchanged in the repository.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing a change. Changes to the fundamental seven-layer model require explicit author approval and must not be inferred from implementation work.
