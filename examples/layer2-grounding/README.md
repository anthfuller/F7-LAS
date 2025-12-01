# Layer 2 — Grounding (Epistemic Guardrails)

Layer 2 constrains the agent’s knowledge to trusted sources.

This prevents:
- fabricated citations  
- unverified instructions  
- unsafe recommendations  

## Files

### `allowlist.json`
Lists approved documentation domains and excluded sources.

### `grounding_profile.yaml`
Defines retrieval rules, domain restrictions, and strict citation mode.

## Purpose

Grounding improves factual accuracy, but **does not control actions**.  
Operational enforcement begins at **Layer 3 → Layer 5**.
