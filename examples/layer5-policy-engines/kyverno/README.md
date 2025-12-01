# Layer 5 — Kyverno PDP (Kubernetes Admission Policy)

This example shows how F7-LAS Layer 5 hard guardrails can be enforced at the cluster boundary.

## Files

### `f7las-agent-action-lockdown.yaml`
A Kyverno rule that denies production-destructive actions.

### `pep_kyverno.py`
Creates a short-lived AgentAction CRD for Kyverno to validate.

## Purpose

Demonstrates enforcement through Kubernetes admission controllers.
