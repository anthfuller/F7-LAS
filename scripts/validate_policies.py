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
