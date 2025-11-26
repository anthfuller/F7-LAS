#!/usr/bin/env python3
"""
F7-LAS golden threshold checker.

Reads the results JSON produced by src/demo_runner/run_golden_dataset.py
and enforces simple success-rate thresholds.
"""

import json
import sys
from pathlib import Path

DEFAULT_MIN_SUCCESS_RATE = 0.8


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "Usage: python scripts/check_golden_thresholds.py <results.json>",
            file=sys.stderr,
        )
        return 1

    results_path = Path(sys.argv[1])
    if not results_path.exists():
        print(f"[ERROR] Results file not found: {results_path}", file=sys.stderr)
        return 1

    with results_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    summary = data.get("summary", {})
    success_rate = float(summary.get("success_rate", 0.0))
    total = int(summary.get("scenarios_total", 0))

    rubric = data.get("rubric", {})
    min_success_rate = float(
        rubric.get("minimum_success_rate", DEFAULT_MIN_SUCCESS_RATE)
    )
    min_scenarios = int(rubric.get("minimum_scenarios", 1))

    if total < min_scenarios:
        print(
            f"[FAIL] Only {total} scenarios, minimum required is {min_scenarios}.",
            file=sys.stderr,
        )
        return 1

    if success_rate < min_success_rate:
        print(
            f"[FAIL] Success rate {success_rate:.2f} below threshold "
            f"{min_success_rate:.2f}.",
            file=sys.stderr,
        )
        return 1

    print(
        f"[PASS] Golden dataset OK. {total} scenarios, "
        f"success rate {success_rate:.2f} (min {min_success_rate:.2f})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
