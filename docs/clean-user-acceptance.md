# Clean-user acceptance

Milestone 8 defines one supported clean-user path for the bounded F7-LAS
reference implementation. It starts from repository files without Git metadata,
creates a new virtual environment, installs only the reviewed hash-locked graph,
and runs the documented validators, tests, canonical walkthrough, evidence
verification, deterministic replay, golden structural evaluation, vulnerability
audit, CFF validation, complete control traceability, and SBOM generation.

## Exact prerequisites

- A clean checkout of this repository on Linux x86_64.
- Python **3.12.14**.
- The OPA **1.20.2** Linux x86_64 static binary with SHA-256
  `69da5179ee403d10fa11bab6cfb4ffb0d23dba5f9b682fa977db772a1da5670f`.
- Network access to the configured Python package index and vulnerability
  service during dependency installation and `pip-audit`.

The repository's canonical code supports Python 3.10 or later, but the
acceptance environment is intentionally narrower and matches CI exactly.

## Run the complete gate

From the repository root, point `OPA_BIN` at the checksum-verified binary:

```bash
OPA_BIN=/absolute/path/to/opa scripts/run-clean-user-acceptance.sh
```

The script rejects a different Python patch release, OPA version, or OPA binary
digest. It removes inherited `PYTHONPATH`, copies the working tree without Git
metadata or local environments, and performs the acceptance run in a temporary
directory. Set `KEEP_CLEAN_USER_WORKDIR=1` only when the temporary evidence and
SBOM are needed for diagnosis.

Success ends with `Clean-user acceptance PASSED`. A nonzero status means the
repository has not passed this gate.

## Command inventory

| Documentation | Classification | Clean-user evidence |
|---|---|---|
| Root validation commands | Supported | Validators and complete tests run in the isolated environment |
| Canonical workflow commands | Supported | Execution, evidence verification, and replay all run |
| Contract validation commands | Supported | Contract validator and complete tests run |
| Supply-chain reproduction commands | Supported | Locked installation, invariant validation, audit, SBOM, and supply-chain tests run |
| Non-canonical layer examples | Illustrative only | No runnable walkthrough is claimed or accepted |
| Dependency-lock regeneration | Maintainer operation | Not represented as a clean-user command; any update requires separate dependency-diff review |
| Full-history Gitleaks scan | CI-only | Requires Git history and remains enforced by the normal GitHub Actions job |

This gate proves reproducibility for one synthetic, offline workflow on the
specified platform. It does not prove production readiness, external-system
behavior, OS/container isolation, artifact provenance, or trustworthiness of
the audited dependencies.
