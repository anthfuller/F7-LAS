#!/usr/bin/env python3
"""
F7-LAS Policy Validator (CI-grade)

Fixes CI by enforcing that:

- The policy directory must exist and contain at least one policy file.
- Each policy JSON must be syntactically valid.
- Each policy must validate against config/policies/policy-schema.json via jsonschema.
- policy_id values must be unique across files.

This is intentionally deterministic and should run fast in CI.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import List, Dict, Any

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
POLICY_DIR = REPO_ROOT / "config" / "policies"
SCHEMA_PATH = POLICY_DIR / "policy-schema.json"


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _format_error(path: Path, err) -> str:
    loc = "/".join(str(x) for x in err.absolute_path) if err.absolute_path else "<root>"
    return f"{path}: {loc}: {err.message}"


def validate_policy_file(path: Path, validator: Draft202012Validator) -> List[str]:
    errors: List[str] = []

    try:
        data = _load_json(path)
    except Exception as e:
        return [f"{path}: invalid JSON ({e})"]

    if not isinstance(data, dict):
        return [f"{path}: top-level JSON must be an object"]

    # jsonschema validation
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path)):
        errors.append(_format_error(path, err))

    return errors


def main() -> int:
    if not POLICY_DIR.exists():
        print(f"[FAIL] Policy directory not found: {POLICY_DIR}", file=sys.stderr)
        return 1

    if not SCHEMA_PATH.exists():
        print(f"[FAIL] Policy schema not found: {SCHEMA_PATH}", file=sys.stderr)
        return 1

    try:
        schema = _load_json(SCHEMA_PATH)
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
    except Exception as e:
        print(f"[FAIL] Invalid policy schema {SCHEMA_PATH}: {e}", file=sys.stderr)
        return 1

    policy_files = sorted(p for p in POLICY_DIR.glob("*.json") if p.name != "policy-schema.json")
    if not policy_files:
        print(f"[FAIL] No policy JSON files found in {POLICY_DIR}", file=sys.stderr)
        return 1

    all_errors: List[str] = []
    seen_policy_ids: Dict[str, Path] = {}

    for path in policy_files:
        # schema validation
        all_errors.extend(validate_policy_file(path, validator))

        # uniqueness check (best-effort even if schema fails)
        try:
            data = _load_json(path)
            pid = data.get("policy_id")
            if isinstance(pid, str) and pid.strip():
                if pid in seen_policy_ids:
                    all_errors.append(
                        f"{path}: duplicate policy_id {pid!r} (also in {seen_policy_ids[pid]})"
                    )
                else:
                    seen_policy_ids[pid] = path
        except Exception:
            pass

    if all_errors:
        print("F7-LAS policy validation FAILED:\n", file=sys.stderr)
        for err in all_errors:
            print(f" - {err}", file=sys.stderr)
        return 1

    print("F7-LAS policy validation PASSED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
