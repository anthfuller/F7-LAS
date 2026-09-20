# Illustrative OPA/Rego Pattern (Layer 5)

This directory is **illustrative, non-canonical, and unsupported as a runnable walkthrough**.
It preserves an early HTTP-based PDP/PEP pattern for design comparison only.

The local files are not a coherent supported deployment:

- `policy.rego` uses an older Rego style and is not the policy executed by the
  canonical workflow.
- `pep_opa.py` targets a service hostname and package path that require external
  orchestration and configuration.
- `docker-compose.yml` is retained as historical prototype material; it uses a
  mutable image reference and does not mount the policy from this directory.

Do not infer execution, security, or compatibility from these files and do not
connect them to production tools or data. The only supported OPA execution path
is the checksum-verified CLI workflow documented in the
[canonical workflow](../../canonical-workflow/README.md). Its executable policy
is [`config/policies/canonical-workflow.rego`](../../../config/policies/canonical-workflow.rego).

This example may be removed or rebuilt in a later, separately reviewed change.
