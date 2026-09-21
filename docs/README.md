# F7-LAS Documentation Index

This directory contains the governed documentation for the F7-LAS seven-layer reference model.

## Authoritative artifacts

- [Whitepaper v4.0](whitepaper/F7-LAS-Whitepaper-v4.0.pdf): current publication;
  the authoritative record is the permanent
  [Zenodo DOI 10.5281/zenodo.22867553](https://doi.org/10.5281/zenodo.22867553).
- [Whitepaper v4.0 SHA-256 checksum](whitepaper/F7-LAS-Whitepaper-v4.0.sha256):
  repository integrity record for the published PDF.
- [Whitepaper v3.0](F7-LAS-model-whitepaper_v3.0.pdf) — immutable historical publication.
- [Whitepaper artifact record](whitepaper-v3.0-artifact.md) — integrity identifiers and handling rule.
- [Whitepaper v3.0 errata](corrections/whitepaper-v3.0-errata.md) — corrections proposed for a future reviewed edition; does not alter the PDF.
- [Implementation guide](f7-las-implementation-guide/README.md): draft engineering guidance bundled with repository release v4.0.0.
- [Control catalog v0.1](F7-LAS-Control-Catalog-v0.1.md) — 46 core Layers 1–7 controls plus five supplemental Layer S controls; all remain draft controls in this repository.
- [Engineering review checklist](Engineering-Review-Checklist.md) — design-review aid.
- [QA and maturity](F7-LAS-QA.md) — current repository truth and limitations.
- [Canonical data contracts v1.0.0](../schemas/contracts/README.md) — machine-validated request-through-audit definitions used by the canonical executable path.
- [Canonical offline workflow](../examples/canonical-workflow/README.md) — the bounded synthetic Python + OPA Layers 1–7 demonstration.
- [Supply-chain and CI controls](supply-chain-and-ci.md) — implemented dependency, action, download, vulnerability, secret, and SBOM checks and their limits.
- [Clean-user acceptance](clean-user-acceptance.md) — the exact supported environment, complete walkthrough, command inventory, and assurance boundary.
- [Architecture diagrams](architecture-diagrams.md) — executive and layer-specific F7-LAS control-loop views, with an explicit implementation mapping and assurance boundary.
- [Control-to-evidence traceability](../config/control-traceability.json) — machine-readable status, limitations, and evidence locators for all 51 controls.
- [Release process](release-process.md) — independent approval, exact-tag validation, and release-SBOM attachment procedure.

Whitepaper version **4.0** is distinct from repository release **v4.0.0**.
Publishing or revising either artifact does not silently revise the other.

## Architecture graphics

The [current architecture diagrams](architecture-diagrams.md) describe the
F7-LAS control model at executive and layer-specific levels. Their semantic map
states exactly which elements the bounded canonical path implements and which
remain reference-architecture requirements. A diagram is not evidence of
production readiness or control effectiveness.

## Status and use

The model is established; the repository implementation is a prototype. Documentation may specify desired controls that are not implemented. Treat only the canonical behavior covered by tests and correlated evidence as verified. The machine-readable traceability file explicitly distinguishes implemented, partial, and not-implemented controls within this repository boundary.

See the root [license map](../LICENSE.md) and [security policy](../SECURITY.md).
