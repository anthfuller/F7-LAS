# F7-LAS Overhaul Roadmap

## Current maturity

F7-LAS is an established seven-layer reference model with a **prototype reference implementation**. The repository is not Beta and is not production-ready. The canonical Python + OPA workflow demonstrates one bounded, synthetic runtime control path; the broader repository remains illustrative and incomplete.

## Delivered target

The delivered **Executable Reference Implementation** provides one offline, deterministic Python + OPA workflow that demonstrates bounded behavior and correlated evidence across Layers 1–7. It remains a reference implementation, not a production agent platform.

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

Repository release **v4.0.0** is tagged and published from immutable commit
`d6a413b878393d98cc2fb2581678f05801767134`. Whitepaper **v4.0** was reviewed
and published separately at
[10.5281/zenodo.22867553](https://doi.org/10.5281/zenodo.22867553), then added
to the repository after the `v4.0.0` tag. It is not part of that immutable
repository release. Whitepaper v3.0 remains preserved as a historical
artifact. See [RELEASE_NOTES.md](RELEASE_NOTES.md) and the
[release process](docs/release-process.md).

## Completion standard

Completion requires a clean-user install and walkthrough, meaningful behavior tests, validated control-to-evidence traceability, accurate diagrams, consistent licensing/versioning, protected-branch enforcement, independent review, and explicit merge and release approval. Test counts alone are not a maturity measure.
