# F7-LAS 4.0.0 release process

This procedure prepares a reproducible repository release without changing the
historical whitepaper or implying production readiness. It is documentation,
not authorization to publish a tag, GitHub release, or Zenodo record.

## Preconditions

- `VERSION` and `RELEASE_NOTES.md` identify `4.0.0` as the reviewed candidate.
- `main` requires pull requests and the passing `validate` status check and
  blocks force pushes and deletion.
- The candidate branch and complete diff have independent approval.
- Pull-request CI and the push-triggered post-merge `main` run pass against the
  exact reviewed tree.
- The whitepaper and canonical diagram hashes match their documented values.

## Exact tag and SBOM binding

1. Record the approved `main` commit and tree SHAs.
2. Create the annotated tag `v4.0.0` at that exact commit. Do not rebuild or
   amend the release candidate between approval and tagging.
3. Push only the tag. The CI workflow's `v*` trigger runs the same validation
   job and generates `f7las-python-sbom-<commit-sha>`.
4. Confirm the tag-triggered run has `head_sha` equal to the approved commit and
   that every job step passed.
5. Download the CycloneDX JSON artifact from that run. Record the GitHub
   artifact digest and independently calculate the extracted JSON SHA-256.
6. Create the GitHub release from the existing `v4.0.0` tag and attach the
   unchanged `f7las-python.cdx.json` plus a checksum file identifying the tag,
   commit SHA, artifact digest, and JSON digest.
7. Verify the published release target, assets, hashes, and availability before
   announcing completion.

The tag-triggered artifact is authoritative for the release. A pull-request or
earlier `main` SBOM must not be relabeled as the release SBOM, even if its
dependency content appears identical.

## Rollback and immutability

If the tag points to the wrong commit, CI fails, or the SBOM association cannot
be proven, stop without publishing the release. Do not move or reuse a public
release tag. Correct the repository through the normal reviewed pull-request
process and use a new version only after approval.

The GitHub release does not update Zenodo. Any future Zenodo deposit is a
separate reviewed publication action.
