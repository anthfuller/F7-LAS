# Layer 5 — Azure Custom PDP

Azure does not provide a direct runtime PDP, so this example uses a custom JSON policy + Python evaluator.

## Files

### `policy_prod_safety.json`
Defines structured policy conditions.

### `azure_pdp.py`
Evaluates the JSON policy and returns allow/deny.

## Purpose

Demonstrates how enterprises can build a lightweight PDP using Azure Functions / API services.
