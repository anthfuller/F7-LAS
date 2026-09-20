# Contributing to F7-LAS

F7-LAS is Anthony Fuller's seven-layer agentic AI security model. The repository currently contains a **prototype reference implementation** and is undergoing a controlled, evidence-driven overhaul.

## Contribution boundaries

- Preserve the fundamental seven-layer model unless a conceptual change is identified and explicitly approved by the author.
- Keep the project vendor-neutral and protocol-agnostic.
- Do not add production-readiness, enforcement, or assurance claims without executable evidence.
- Use synthetic data, identities, policies, approvals, and actions.
- Do not add code that executes external cloud, identity, security, or remediation actions.
- Prefer one coherent canonical path over multiple incomplete integrations.
- Do not expose, request, or model private chain-of-thought. Use auditable plans, decisions, evidence, requests, actions, and outcomes.

## Pull requests

Keep changes focused. A pull request must state:

- the purpose and affected F7-LAS layer(s),
- security and compatibility implications,
- files and claims changed,
- validation performed and reproducible commands,
- limitations and unverified behavior,
- whether control-catalog or traceability evidence changes.

Runnable examples require automated tests. Non-runnable patterns must be labeled **illustrative**. Documentation links and commands must work case-sensitively in a clean environment.

## Review requirements

Changes to policy semantics, approval binding, execution order, control status, diagrams, maturity, versioning, or licensing require explicit maintainer review. The historical whitepaper v3.0 PDF must not be modified.

All contributors must follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) and [SECURITY.md](SECURITY.md).

## Licensing contributions

By contributing, you agree that:

- authored documentation, diagrams, model content, and prose are licensed under [CC BY 4.0](LICENSE-CONTENT.md);
- executable source code and policy/configuration examples are licensed under [MIT](LICENSE-CODE);
- the detailed file boundary in [LICENSE.md](LICENSE.md) applies;
- no trademark rights or endorsement are granted.
