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
