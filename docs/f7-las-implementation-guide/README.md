# F7-LAS Implementation Guide — Draft

This guide translates the seven-layer model into engineering guidance. It describes desired controls and patterns; it does **not** claim that the current repository implements or automatically verifies every requirement.

The guide remains draft authored content bundled with repository release v4.0.0. It is reconciled with the canonical offline Python + OPA workflow and machine-readable control traceability, but it is not independently versioned or represented as fully implemented guidance.

## Contents

- [00 — Introduction](00-introduction.md)
- [01 — Control objectives](01-control-objectives.md)
- [02 — Layer-by-layer controls](02-layer-by-layer-controls.md)
- [03 — Supplemental Layer S](03-supplemental-layer-s.md)
- [04 — Model security annex](04-model-security-annex.md)
- [05 — Metrics and SLOs](05-metrics-and-slos.md)
- [06 — Operational playbooks](06-operational-playbooks.md)
- [07 — RACI model](07-raci-model.md)
- [Optional MCP security profile](08-implementation-profiles/Optional-MCP-Security-Profile.md) — protocol-specific illustrative guidance, not part of the vendor-neutral core.

### Appendices

- [A — Schemas](Appendices/a-schemas.md)
- [B — Templates](Appendices/b-templates.md)
- [C — Checklist](Appendices/c-checklist.md)
- [D — Reference patterns](Appendices/d-reference-patterns.md)

### Layer S — software supply-chain security

- [Overview](layer-s/README.md)
- [Checklist](layer-s/checklist.md)
- [SBOM guidance](layer-s/sbom-guidance.md)
- [Vetting workflow](layer-s/vetting-workflow.md)
- [Allowlist schema](layer-s/allowlist-schema.json)

Layer S is cross-cutting and is not an eighth F7-LAS layer.

## Interpretation

Normative words such as **SHALL** express the model's desired control objective. Implementation status must be established separately through the control catalog and evidence traceability; wording alone is not evidence of enforcement.

Model author: **Anthony Fuller** · [GitHub](https://github.com/anthfuller)
