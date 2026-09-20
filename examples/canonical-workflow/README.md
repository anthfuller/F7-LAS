# Canonical Offline Workflow

This is the single Milestone 3 executable path across F7-LAS Layers 1–7. It is
deterministic, synthetic, offline, and fail-closed. It does not call an LLM,
cloud API, production service, or network tool.

The path uses fixed prompt intent and admission checks (Layer 1), synthetic
grounding (Layer 2), a bounded deterministic plan (Layer 3), one proposed
read-only action (Layer 4), an offline OPA CLI decision (Layer 5), a registered
no-network synthetic executor (Layer 6), and correlated canonical audit records
(Layer 7).

Milestone 3 uses `not_required` for the low-risk synthetic read. Binding an
explicit approval to the complete request/action/policy/scope/expiry tuple is
Milestone 4 and is intentionally not claimed here.

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
allow decision.
