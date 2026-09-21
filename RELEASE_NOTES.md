# F7-LAS v4.0.0 Repository Release

**Status:** Published as the
[v4.0.0 GitHub repository release](https://github.com/anthfuller/F7-LAS/releases/tag/v4.0.0).
The annotated tag targets commit
`d6a413b878393d98cc2fb2581678f05801767134`.

F7-LAS v4.0.0 is the published repository release for the evidence-driven
overhaul. It packages the established seven-layer reference model with one
bounded, deterministic, synthetic Python + OPA reference workflow. It remains
a prototype reference implementation, not a production agent platform.

Whitepaper v4.0 was published separately at
[10.5281/zenodo.22867553](https://doi.org/10.5281/zenodo.22867553) and added to
the repository after the `v4.0.0` release. It is not part of the immutable
`v4.0.0` tag. The tag retains Whitepaper v3.0 as a historical artifact.

## Release contents

- Canonical v1.0.0 contracts for request-through-audit records.
- One offline, fail-closed Python + OPA Layers 1–7 path.
- Approval binding to request, action, scope, authority, time window, and the
  exact executable policy bundle.
- Behavioral scenarios, evidence integrity verification, and deterministic
  replay.
- Hash-locked dependencies, immutable Action references, verified OPA and
  Gitleaks downloads, vulnerability scanning, full-history secret scanning,
  and a retained CycloneDX SBOM.
- Clean-user acceptance using Python 3.12.14 and OPA 1.20.2.
- Machine-readable traceability for all 46 core Layers 1–7 controls and five
  supplemental Layer S controls.
- Corrected executive and layer-specific control-loop diagrams.

## Explicit limitations

- The supported executor is synthetic and in-process. It is not an OS or
  container sandbox and does not enforce network isolation.
- No production identity, cloud, SIEM, SOAR, XDR, remediation, or human
  approval integration is provided.
- The golden-dataset runner validates scenario and rubric structure; the
  behavioral matrix separately exercises canonical enforcement paths.
- Evidence is digest-bound but not digitally signed, externally timestamped,
  or backed by a provenance service.
- The control catalog and implementation guide remain draft authored content;
  repository release v4.0.0 does not silently revise their independent
  versions or either whitepaper publication.

## Publication verification

The repository release completed the reviewed publication process:

1. the exact approved tree was merged through a protected pull request;
2. the push-triggered `main` workflow passed against the merge commit;
3. the annotated `v4.0.0` tag was created at the exact approved commit;
4. the tag-triggered workflow passed all validation steps;
5. the exact-tag CycloneDX SBOM and checksum manifest were verified and
   attached unchanged to the GitHub release;
6. the GitHub release was published from the existing immutable tag.

The detailed procedure is in
[`docs/release-process.md`](docs/release-process.md).
