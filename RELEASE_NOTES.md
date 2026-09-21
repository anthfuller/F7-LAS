# F7-LAS 4.0.0 Release Candidate

**Status:** Prepared but not tagged or published. This document does not
authorize a GitHub release, Zenodo update, or change to the historical
whitepaper.

F7-LAS 4.0.0 is the intended repository release for the evidence-driven
overhaul. It packages the established seven-layer reference model with one
bounded, deterministic, synthetic Python + OPA reference workflow. It remains
a prototype reference implementation, not a production agent platform.

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
  repository version 4.0.0 does not silently revise their independent versions
  or the immutable whitepaper v3.0.

## Required publication gate

Publication requires all of the following after the release-candidate branch
is independently reviewed:

1. merge the exact approved tree through a protected pull request;
2. verify the push-triggered `main` workflow against the resulting merge SHA;
3. create `v4.0.0` at that exact approved `main` SHA without additional files;
4. verify the tag-triggered workflow and its complete validation job;
5. download the CycloneDX artifact produced by that tag run, verify its run,
   commit, name, and digest, and attach it unchanged to the GitHub release;
6. publish these notes only after the release assets and target SHA are
   independently verified.

The detailed procedure is in
[`docs/release-process.md`](docs/release-process.md).
