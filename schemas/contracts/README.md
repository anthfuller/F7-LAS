# F7-LAS Canonical Data Contracts

Version **1.0.0** defines eight record types for the canonical deterministic,
offline Python + OPA reference workflow:

1. `request`
2. `context`
3. `plan`
4. `proposed_action`
5. `approval`
6. `policy_decision`
7. `execution_result`
8. `audit_event`

The normative single-record schema is
[`f7las-records-v1.schema.json`](f7las-records-v1.schema.json). The fixture in
[`examples/approved-dry-run.json`](examples/approved-dry-run.json) is synthetic
and does not invoke a tool.

## Validation boundary

JSON Schema Draft 2020-12 validates each record independently. It enforces
required fields, field types, enumerations, closed core objects, and conditional
rules within approval, policy-decision, and execution-result records.

The Python validator enforces relationships that JSON Schema cannot establish
between separate records: matching references, cardinality, sequence and
timestamp ordering, policy and scope equality, digest binding, and
decision-to-execution consistency.

## Cardinality

- Exactly one `request`, `context`, and `plan` per workflow.
- One or more `proposed_action` records.
- Exactly one `approval`, `policy_decision`, and `execution_result` per action.
- Zero or more `audit_event` records.

## Contract rules

- Records use schema version `1.0.0`, a shared `workflow_id`, unique
  `record_id` values, and monotonically increasing `sequence` values.
- Timestamps use whole-second RFC 3339 UTC form ending in `Z`.
- `scope_id` is the required vendor-neutral boundary. `tenant_id` is optional.
- Core records reject undeclared fields. Tool `arguments`, execution `output`,
  and audit `details` allow record-specific JSON.
- Approval and policy-decision records carry an identical `policy_ref` with
  policy ID, version, and digest.
- Credentials, tokens, secrets, and private model reasoning are prohibited.
- Contract evolution follows semantic versioning; breaking changes require a
  new major contract version.

## Deterministic digests

Canonical JSON uses [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785).
SHA-256 inputs are domain-separated:

```text
record: SHA-256("F7-LAS:record:<record_type>:1.0.0\n" || JCS(record without record_digest))
action: SHA-256("F7-LAS:action:1.0.0\n" || JCS(security-relevant action projection))
output: SHA-256("F7-LAS:output:1.0.0\n" || JCS(output))
policy-bundle: SHA-256("F7-LAS:policy-bundle:1.0.0\n" || JCS({metadata, SHA-256(exact Rego bytes)}))
evidence-set: SHA-256("F7-LAS:evidence-set:1.0.0\n" || JCS(complete evidence document))
```

Digests use `sha256:<64 lowercase hexadecimal characters>`. Object key order is
immaterial; array order is material. Duplicate keys, NaN, Infinity, implicit
defaults, and self-inclusion of a digest field are not permitted.

`previous_record_digest` creates a linear record chain. Record references bind
both `record_id` and `record_digest`; action-specific records additionally bind
the exact `action_digest`.

The canonical `policy_ref.policy_digest` is the policy-bundle digest. It binds
the versioned JSON metadata and exact bytes of the Rego module executed
by OPA. The adapter recomputes and verifies this reference before invoking OPA;
the approval, decision, evidence verifier, and replay path require the same
bundle reference.

Milestone 2 defined these contracts. The canonical workflow emits and validates
them around a real offline OPA decision and binds its deterministic synthetic
approval through PDP and PEP enforcement. The canonical evidence verifier adds
a stricter single-action profile: exactly one record of each type, a final audit
event that binds every preceding record in order, and an audit summary that
matches the decision and result. This does not claim an interactive
human-approval service, identity proofing, OS/container sandbox containment,
enforced network isolation, signed evidence, or external attestation.

The evidence-set digest detects later mutation only when it is compared with a
previously trusted copy. Because the records are not signed, a party able to
replace both the evidence and its expected digest can construct another
self-consistent set. Deterministic replay adds an independent comparison to the
reviewed input and repository policy, but it is not proof of provenance.

## Validate

```bash
python scripts/validate-contracts.py
pytest -q
```
