# Layer 5 — OPA / Rego PDP

This folder contains a Rego policy implementing F7-LAS hard guardrails.

## Files

### `policy.rego`
Evaluates:
- allow conditions  
- deny conditions  
- deny_message for user feedback  

### `pep_opa.py`
Python PEP middleware that:
1. Builds PDP input  
2. Sends it to OPA (`/v1/data/...`)  
3. Enforces allow / deny  
4. Logs decisions (Layer 7)

## Purpose

OPA provides deterministic allow/deny logic external to the LLM, ensuring safe action execution.
