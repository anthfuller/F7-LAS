# F7-LAS Overhaul Roadmap

## Current maturity

F7-LAS is an established seven-layer reference model with a **prototype reference implementation**. The repository is not Beta and is not production-ready. The canonical Python + OPA workflow demonstrates one bounded, synthetic runtime control path; the broader repository remains illustrative and incomplete.

## Approved target

The target is an **Executable Reference Implementation**: one offline, deterministic Python + OPA workflow that demonstrates bounded behavior and correlated evidence across Layers 1–7. It will remain a reference implementation, not a production agent platform.

## Milestones

1. **Repository truth and terminology** — reconcile maturity, versioning, paths, licensing, unsupported claims, and private-reasoning terminology.
2. **Canonical data contracts** — define deterministic request, context, plan, proposed action, approval, decision, result, and audit records.
3. **Canonical Python + OPA path** — one offline, fail-closed Layers 1–7 workflow is implemented for the bounded synthetic action.
4. **Approval binding** — synthetic approval is bound to the exact request/action digests, scope, complete policy reference, authority, and expiry in the canonical path.
5. **Behavioral scenarios** — an executable canonical matrix tests permitted, denied, malformed, unauthorized, unavailable, timed-out, tampered, expired, obligation, and recovery paths.
6. **Evidence and replay** — canonical evidence can be independently verified for complete correlation and tampering, then replayed from the admitted input to reproduce the exact canonical outcome.
7. **Supply chain and CI** — implement pinned and hashed dependencies, immutable action references, verified tool downloads, known-vulnerability and Git-history secret gates, and a retained CI SBOM.
8. **Documentation reconciliation** — execute every supported user command in a clean environment; classify maintainer-only and illustrative material explicitly.
9. **F7-LAS-specific diagrams** — replace diagrams only after execution semantics are frozen.
10. **Independent review** — review the complete branch diff and CI evidence before any merge, release, or Zenodo update.

## Release boundary

The intended repository release after all acceptance gates is **4.0.0**. The whitepaper remains **v3.0** until it is separately reviewed and revised. No milestone authorizes a merge to `main`, a release, or a Zenodo update without explicit approval.

## Completion standard

Completion requires a clean-user install and walkthrough, meaningful behavior tests, control-to-evidence traceability, accurate diagrams, consistent licensing/versioning, independent review, and explicit merge approval. Test counts alone are not a maturity measure.
