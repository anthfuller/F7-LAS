#!/usr/bin/env python3
"""
F7-LAS Policy Validator (Stage 0)

Validates JSON policy files under config/policies/ for:

- Basic JSON syntax.
- Presence of core fields:
  policy_id, policy_type, description, version,
  target_layer, default_decision, rules.

This is intentionally lightweight and should be easy to extend
in later stages (e.g., to enforce full JSON Schema validation).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import List


REPO_ROOT = Path(__file__).resolve().parents[1]
POLICY_DIR = REPO_ROOT / "config" / "policies"

REQUIRED_FIELDS = [
    "policy_id",
    "policy_type",
    "description",
    "version",
    "target_layer",
    "default_decision",
    "rules",
]


def validate_policy_file(path: Path) -> List[str]:
    errors: List[str] = []

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        errors.append(f"{path}: invalid JSON ({e})")
        return errors

    if not isinstance(data, dict):
        errors.append(f"{path}: top-level JSON must be an object")
        return errors

    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"{path}: missing required field {field!r}")

    # Basic type checks for a few fields
    if "rules" in data and not isinstance(data["rules"], list):
        errors.append(f"{path}: 'rules' must be an array")

    if "policy_type" in data and not isinstance(data.get("policy_type"), str):
        errors.append(f"{path}: 'policy_type' must be a string")

    return errors


def main() -> int:
    if not POLICY_DIR.exists():
        print(f"[WARN] Policy directory not found: {POLICY_DIR}", file=sys.stderr)
        return 0

    policy_files = sorted(
        p for p in POLICY_DIR.glob("*.json") if p.name != "policy-schema.json"
    )

    if not policy_files:
        print(f"[WARN] No policy JSON files found in {POLICY_DIR}")
        return 0

    all_errors: List[str] = []
    for path in policy_files:
        all_errors.extend(validate_policy_file(path))

    if all_errors:
        print("F7-LAS policy validation FAILED:\n", file=sys.stderr)
        for err in all_errors:
            print(f" - {err}", file=sys.stderr)
        return 1

    print("F7-LAS policy validation PASSED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
