# Canonical Offline Workflow

This is the single canonical executable path across F7-LAS Layers 1–7. It is
deterministic, synthetic, offline, and fail-closed. It does not call an LLM,
cloud API, production service, or network tool.

The path uses fixed prompt intent and admission checks (Layer 1), synthetic
grounding (Layer 2), a bounded deterministic plan (Layer 3), one proposed
read-only action (Layer 4), an offline OPA CLI decision (Layer 5), a registered
synthetic in-process executor that makes no network calls (Layer 6), and
correlated canonical audit records (Layer 7). Layer 6 here is not an OS or
container sandbox and does not enforce a network-isolation boundary.

The synthetic approval is bound to the exact request and action references and
digests, complete scope, complete policy reference, approving authority, issue
time, and expiry. OPA validates the binding before permitting, and the
in-process executor independently revalidates it at execution time. This is
deterministic approval evidence for the reference workflow, not an interactive
human-approval service or identity proofing system.

## Requirements

- Python 3.10 or later with `requirements.txt` installed.
- OPA CLI **1.20.2** available as `opa` or supplied with `--opa-binary`.

## Run

```bash
python -m src.canonical.cli \
  --input examples/canonical-workflow/request.json \
  --output /tmp/f7las-canonical-records.json \
  --opa-binary opa
```

Expected summary:

```text
decision=permit execution=succeeded output=/tmp/f7las-canonical-records.json
```

If OPA is missing, times out, rejects the policy, or returns malformed output,
the workflow emits a denial and `not_executed` result. It never falls back to an
allow decision. The evidence file is preserved and the CLI returns exit status
`3` for a denied or otherwise unexecuted action.

## Behavioral scenarios

The executable scenario manifest at `tests/behavioral_scenarios.json` covers
permit, policy denial, malformed input and PDP output, unauthorized identity,
PDP unavailability and timeout, post-decision tampering, missing obligations,
approval expiry, and recovery after a transient PDP outage. Accepted attempts
must emit schema-valid, cross-record-valid evidence with no reported side
effects. Admission refusals must emit no workflow records.

Run the matrix with the pinned OPA CLI available:

```bash
OPA_BIN=opa pytest -q tests/test_behavioral_scenarios.py
```

These are deterministic reference-workflow scenarios, not claims of production
fault injection, infrastructure recovery, or OS/container isolation.

## Evidence integrity

Verify a canonical workflow output independently of the producer:

```bash
python -m src.canonical.evidence \
  --evidence /tmp/f7las-canonical-records.json
```

Verification rejects duplicate JSON keys; schema or cross-record violations;
broken record chains, references, action/output digests, or policy bindings;
incomplete or reordered final audit sources; and audit summaries inconsistent
with the policy decision or execution result. The reported evidence-set digest
detects later mutation when compared with a previously trusted copy. It is not
a signature, proof of origin, trusted timestamp, or external attestation; a
party that can replace both evidence and its expected digest can construct a
different self-consistent set.

## Deterministic replay

Replay the same admitted input through the canonical workflow and require the
complete RFC 8785 canonical evidence document to match:

```bash
python -m src.canonical.replay \
  --input examples/canonical-workflow/request.json \
  --evidence /tmp/f7las-canonical-records.json \
  --output /tmp/f7las-replayed-records.json \
  --opa-binary opa
```

Replay first verifies the reviewed evidence, reruns the fixed synthetic action
and offline policy evaluation, verifies the new evidence, and then compares the
complete canonical documents. A reproduced denial is a successful replay; it
does not become an allow decision. Exit status `4` indicates invalid evidence
or a replay mismatch. The output path may not overwrite the input or reviewed
evidence.

Replay covers this deterministic, side-effect-free reference workflow only. It
does not reproduce external systems, network calls, operating-system state,
human identity proofing, or real-world side effects. Reproduction requires the
reviewed input, repository policy identified by its digest, compatible Python
dependencies, and the pinned OPA behavior.
