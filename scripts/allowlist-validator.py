#!/usr/bin/env python3
import json
import sys
import os

SCHEMA_PATH = "docs/f7-las-implementation-guide/layer-s/allowlist-schema.json"
ALLOWLIST_PATH = "config/tools/allowlist.json"

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Unable to load {path}: {e}")
        sys.exit(1)

def validate_item(item, schema_props):
    errors = []

    for prop, rules in schema_props.items():
        # Required fields
        if rules.get("required", False):
            if prop not in item:
                errors.append(f"Missing required field: {prop}")
                continue

        if prop not in item:
            continue  # not required → skip

        # Type validation
        expected_type = rules.get("type")
        if expected_type:
            actual_type = type(item[prop]).__name__
            if actual_type != expected_type:
                errors.append(f"Field '{prop}' expected type '{expected_type}', got '{actual_type}'")

        # Enum validation
        if "enum" in rules:
            if item[prop] not in rules["enum"]:
                errors.append(f"Field '{prop}' invalid value '{item[prop]}' (allowed: {rules['enum']})")

    return errors

def main():
    print("Validating F7-LAS Tool Allowlist...")

    schema = load_json(SCHEMA_PATH)
    allowlist = load_json(ALLOWLIST_PATH)

    schema_props = schema.get("properties", {})

    if not isinstance(allowlist, list):
        print("[FAIL] allowlist.json must be a JSON array")
        sys.exit(1)

    overall_errors = []
    for idx, item in enumerate(allowlist):
        errors = validate_item(item, schema_props)
        if errors:
            overall_errors.append((idx, errors))

    if overall_errors:
        print("\n❌ Validation FAILED:")
        for idx, errs in overall_errors:
            print(f"\n  Entry #{idx}:")
            for e in errs:
                print(f"   - {e}")
        sys.exit(1)

    print("allowlist.json is valid according to allowlist-schema.json")
    sys.exit(0)

if __name__ == "__main__":
    main()
