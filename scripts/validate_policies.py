#!/usr/bin/env python3
"""
Placeholder policy validator for F7-LAS.

Currently just checks that config/policies/ exists.
Extend later with real validation logic.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
POLICY_DIR = REPO_ROOT / "config" / "policies"


def main() -> int:
    if not POLICY_DIR.exists():
        print(f"[WARN] Policy directory not found: {POLICY_DIR}", file=sys.stderr)
        return 0
    print(f"[INFO] Policy directory present: {POLICY_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
scripts/validate_settings.py

python
Copy code
#!/usr/bin/env python3
"""
Placeholder settings validator for F7-LAS.

Later this can enforce bounds from settings.yaml.
"""

import sys
from pathlib import Path

import yaml  # from requirements.txt

REPO_ROOT = Path(__file__).resolve().parents[1]
SETTINGS_FILE = REPO_ROOT / "config" / "settings.yaml"


def main() -> int:
    if not SETTINGS_FILE.exists():
        print(f"[WARN] settings.yaml not found at {SETTINGS_FILE}", file=sys.stderr)
        return 0

    with SETTINGS_FILE.open("r", encoding="utf-8") as f:
        try:
            yaml.safe_load(f)
        except Exception as e:
            print(f"[ERROR] Failed to parse settings.yaml: {e}", file=sys.stderr)
            return 1

    print("[INFO] settings.yaml parsed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
