# F7-LAS Overhaul Roadmap

## Current maturity

F7-LAS is an established seven-layer reference model with a **prototype reference implementation**. The repository is not Beta and is not production-ready. The canonical Python + OPA workflow demonstrates one bounded, synthetic runtime control path; the broader repository remains illustrative and incomplete.

## Approved target

The target is an **Executable Reference Implementation**: one offline, deterministic Python + OPA workflow that demonstrates bounded behavior and correlated evidence across Layers 1–7. It will remain a reference implementation, not a production agent platform.

## Milestones

1. **Repository truth and terminology** — reconcile maturity, versioning, paths, licensing, unsupported claims, and private-reasoning terminology.
2. **Canonical data contracts** — define deterministic request, context, plan, proposed action, approval, decision, result, and audit records.
3. **Canonical Python + OPA path** — one offline, fail-closed Layers 1–7 workflow is implemented for the bounded synthetic action.
4. **Approval binding** — bind synthetic approval to the exact request/action digest, scope, policy version, and expiry.
5. **Behavioral scenarios** — test permitted, denied, malformed, unauthorized, unavailable, tampered, recovery, and other required paths.
6. **Evidence and replay** — correlate records, detect tampering, and reproduce deterministic outcomes.
7. **Supply chain and CI** — pin dependencies and actions; add integrity, vulnerability, secret, and SBOM checks.
8. **Documentation reconciliation** — execute every documented command in a clean environment.
9. **F7-LAS-specific diagrams** — replace diagrams only after execution semantics are frozen.
10. **Independent review** — review the complete branch diff and CI evidence before any merge, release, or Zenodo update.

## Release boundary

The intended repository release after all acceptance gates is **4.0.0**. The whitepaper remains **v3.0** until it is separately reviewed and revised. No milestone authorizes a merge to `main`, a release, or a Zenodo update without explicit approval.

## Completion standard

Completion requires a clean-user install and walkthrough, meaningful behavior tests, control-to-evidence traceability, accurate diagrams, consistent licensing/versioning, independent review, and explicit merge approval. Test counts alone are not a maturity measure.
