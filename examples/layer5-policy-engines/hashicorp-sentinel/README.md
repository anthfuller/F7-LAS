# HashiCorp Sentinel PDP Demo (Layer 5)

This folder provides a Sentinel-based example of the F7-LAS Layer-5
Policy Decision Point (PDP).

Files:

- `f7las_l5.sentinel` — the Sentinel policy that implements the L5 rules
- `sentinel_adapter.py` — a vendor-neutral PDP adapter called by the PEP

## Usage

Sentinel evaluates the policy based on an `input.request` object like:

```json
{
  "request": {
    "action": "terminate_instance",
    "environment": "production",
    "current_time_ok_for_change": false
  }
}
