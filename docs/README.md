# F7-LAS Documentation Index

This directory contains the governed documentation for the F7-LAS seven-layer reference model.

## Authoritative artifacts

- [Whitepaper v3.0](F7-LAS-model-whitepaper_v3.0.pdf) — immutable historical publication.
- [Whitepaper artifact record](whitepaper-v3.0-artifact.md) — integrity identifiers and handling rule.
- [Whitepaper v3.0 errata](corrections/whitepaper-v3.0-errata.md) — corrections proposed for a future reviewed edition; does not alter the PDF.
- [Implementation guide](f7-las-implementation-guide/README.md) — draft engineering guidance.
- [Control catalog v0.1](F7-LAS-Control-Catalog-v0.1.md) — 46 draft controls across Layers 1–7.
- [Engineering review checklist](Engineering-Review-Checklist.md) — design-review aid.
- [QA and maturity](F7-LAS-QA.md) — current repository truth and limitations.
- [Canonical data contracts v1.0.0](../schemas/contracts/README.md) — machine-validated request-through-audit definitions used by the canonical executable path.
- [Canonical offline workflow](../examples/canonical-workflow/README.md) — the bounded synthetic Python + OPA Layers 1–7 demonstration.
- [Supply-chain and CI controls](supply-chain-and-ci.md) — implemented dependency, action, download, vulnerability, secret, and SBOM checks and their limits.
- [Clean-user acceptance](clean-user-acceptance.md) — the exact supported environment, complete walkthrough, command inventory, and assurance boundary.

## Architecture graphics

Existing diagrams remain under `docs/` and `docs/images/` while their references and semantics are inventoried. They are historical/current draft visuals, not evidence of implemented behavior. Purpose-built replacement diagrams will be created only after the canonical execution semantics are approved.

## Status and use

The model is established; the repository implementation is a prototype. Documentation may specify desired controls that are not implemented. Treat only the canonical behavior covered by tests and correlated evidence as verified; control-to-evidence traceability remains a separate release gate.

See the root [license map](../LICENSE.md) and [security policy](../SECURITY.md).
