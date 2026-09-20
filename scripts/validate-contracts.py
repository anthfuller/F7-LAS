#!/usr/bin/env python3
"""Validate the repository's canonical contract examples."""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.canonical.validation import *  # noqa: F403
from src.canonical.validation import main


if __name__ == "__main__":
    raise SystemExit(main())
