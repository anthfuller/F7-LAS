# Layer 4 — Tool Security Profile v2

**Status:** Draft (Stage-2)

Defines capability classes and sanitization rules for tools.

## Capability Classes

| Class | Example Actions | Risk Level |
|------|-----------------|-----------|
| Safe | list, describe | Low |
| Medium-Risk | modify, write | Medium |
| High-Impact | delete, terminate, isolate | High |

## Required Metadata (MCP-inspired, vendor-neutral)

- `name`
- `capability_class`
- `allowed_arguments`
- `schema_version`
- `simulation_mode_supported: true/false`

## Sanitization Rules

| Stage | Rule |
|------|-----|
| Input | Validate argument schema + ranges |
| Output | Strip PII and system-internal IDs |
