#!/usr/bin/env python3
"""
F7-LAS Tool Allowlist Validator (CI-grade)

Fixes CI by validating config/tools/allowlist.json against
docs/f7-las-implementation-guide/layer-s/allowlist-schema.json using jsonschema.

The previous implementation incorrectly assumed allowlist.json was an array.
"""

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "docs" / "f7-las-implementation-guide" / "layer-s" / "allowlist-schema.json"
ALLOWLIST_PATH = REPO_ROOT / "config" / "tools" / "allowlist.json"


def _load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    if not SCHEMA_PATH.exists():
        print(f"[FAIL] allowlist schema not found: {SCHEMA_PATH}", file=sys.stderr)
        return 1
    if not ALLOWLIST_PATH.exists():
        print(f"[FAIL] allowlist file not found: {ALLOWLIST_PATH}", file=sys.stderr)
        return 1

    try:
        schema = _load_json(SCHEMA_PATH)
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
    except Exception as e:
        print(f"[FAIL] invalid allowlist schema: {e}", file=sys.stderr)
        return 1

    try:
        allowlist = _load_json(ALLOWLIST_PATH)
    except Exception as e:
        print(f"[FAIL] invalid allowlist JSON: {e}", file=sys.stderr)
        return 1

    errors = sorted(validator.iter_errors(allowlist), key=lambda e: list(e.absolute_path))
    if errors:
        print("❌ allowlist.json validation FAILED:", file=sys.stderr)
        for err in errors:
            loc = "/".join(str(x) for x in err.absolute_path) if err.absolute_path else "<root>"
            print(f" - {loc}: {err.message}", file=sys.stderr)
        return 1

    print("✅ allowlist.json is valid according to allowlist-schema.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
