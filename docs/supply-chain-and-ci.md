# Supply-chain and CI controls

Milestone 7 hardens the repository's bounded Python CI path. The controls in
this document do not make the prototype production-ready and do not constitute
a signed build or release attestation.

## Enforced controls

| Area | Enforcement |
|---|---|
| Python direct dependencies | Exact versions in `requirements.txt` and `requirements-ci.in` |
| Python transitive dependencies | Fully resolved versions and SHA-256 distribution hashes in `requirements-ci.lock`; CI installs with `--require-hashes` |
| GitHub Actions | Every external `uses:` reference is a full 40-character commit SHA with its release tag recorded in a same-line comment |
| Workflow authority | The workflow-level `GITHUB_TOKEN` permission is limited to `contents: read`; checkout does not persist credentials |
| Downloaded tools | OPA and Gitleaks versions and Linux x64 archive/binary SHA-256 digests are fixed and verified before execution |
| Known vulnerabilities | `pip-audit` checks the complete locked Python graph and fails on any published known vulnerability it reports |
| Secret patterns | Gitleaks scans the checked-out Git history with redacted output and fails on a finding |
| SBOM | The dependency audit emits a CycloneDX JSON SBOM and CI retains it as a run artifact for 30 days |
| Drift prevention | `scripts/validate-supply-chain.py` and its negative tests reject unpinned dependencies, unhashed lock entries, mutable actions, persisted checkout credentials, and unverified `curl` downloads |
| Updates | Dependabot proposes weekly Python and GitHub Actions updates; changes still require normal review and CI |

## Reproduce the CI checks

Use Python 3.12.14, matching the workflow:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --require-hashes -r requirements-ci.lock
python scripts/validate-supply-chain.py
python scripts/validate-documentation.py
pip-audit --require-hashes --disable-pip --strict \
  --progress-spinner off \
  --requirement requirements-ci.lock \
  --format cyclonedx-json \
  --output f7las-python.cdx.json
python -m pytest -q tests/test_supply_chain.py
```

Gitleaks and OPA are installed in CI from the exact versioned URLs and digests
declared in `.github/workflows/f7las-ci.yml`. Their checks can be reproduced by
running the corresponding workflow commands on Linux x64.

## Updating the Python lock

Dependency-lock regeneration is a maintainer operation, not a supported
clean-user command. Change exact top-level pins deliberately, regenerate the
lock in a separately reviewed maintenance environment, and review every
transitive version and hash change. An update is incomplete until the
known-vulnerability audit, full tests, and complete dependency diff have been
reviewed. Dependabot proposals are not auto-merged.

## Release-tag SBOM

The workflow runs for version tags matching `v*` as well as pull requests and
pushes to `main`. The release process requires `v4.0.0` to point to the exact
independently approved `main` commit. That tag-triggered run generates
`f7las-python-sbom-<commit-sha>` using the same hash-locked dependency graph and
validation job.

Only the SBOM from the successful tag-triggered run may be attached to the
4.0.0 GitHub release. The maintainer must verify the workflow event, tag target,
head SHA, artifact association, GitHub artifact digest, and extracted JSON
SHA-256 before attaching the unchanged CycloneDX file and its checksum record.
The complete non-publishing procedure is documented in
[release-process.md](release-process.md).

## Assurance boundary

- Hash checking detects a downloaded Python distribution that does not match
  the reviewed lock; it does not prove the package is trustworthy.
- `pip-audit` checks published vulnerability data for Python packages. It is
  not static analysis, malware detection, or coverage for the runner OS and
  every library a wheel may contain.
- Gitleaks detects supported patterns and heuristics. A clean scan is not proof
  that the repository contains no sensitive value.
- The CycloneDX artifact inventories the locked Python CI graph. It is not
  signed, attached to a release, or a complete inventory of the runner image.
- Full action SHAs are immutable Git references, but action source and future
  SHA updates still require human review.

The pinning model follows GitHub's guidance that a full-length action commit
SHA is the immutable action reference. The vulnerability and SBOM behavior is
the documented behavior of `pip-audit`; its own security model defines the
limits above.

## Primary references

- [GitHub Actions secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [`pip-audit` documentation and security model](https://github.com/pypa/pip-audit)
- [Gitleaks documentation](https://github.com/gitleaks/gitleaks)
