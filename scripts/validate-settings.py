#!/usr/bin/env python3
"""
F7-LAS Settings Validator

Validates the structure and required fields of the settings YAML file.
"""

import sys
import yaml
from pathlib import Path

REQUIRED_TOP_LEVEL_KEYS = [
    "version",
    "description",
    "agent_runtime",
    "planner",
    "risk",
    "logging",
    "telemetry",
    "sandbox",
    "experiments",
]

def validate_settings(settings_path: Path) -> list[str]:
    errors = []
    if not settings_path.exists():
        return [f"Settings file not found: {settings_path}"]

    try:
        with settings_path.open("r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        return [f"Error reading YAML: {e}"]

    for key in REQUIRED_TOP_LEVEL_KEYS:
        if key not in config:
            errors.append(f"Missing required top-level key: '{key}'")

    return errors

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate-settings.py <settings.yaml>", file=sys.stderr)
        return 1

    settings_path = Path(sys.argv[1])
    errors = validate_settings(settings_path)

    if errors:
        print("F7-LAS settings validation FAILED:\n", file=sys.stderr)
        for err in errors:
            print(f" - {err}", file=sys.stderr)
        return 1

    print("F7-LAS settings validation PASSED.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
