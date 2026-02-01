#!/usr/bin/env python3
"""
F7-LAS golden threshold checker (anti-theater)

This checker is intentionally strict:

- It must read the *CI-produced* results JSON.
- It fails if the runner indicates placeholder / non-deterministic status.
- It fails if structural validation failed or rubric errors exist.
- It enforces rubric thresholds (minimum_scenarios, minimum_success_rate).
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

    meta = data.get("meta", {})
    runner = meta.get("runner")
    if not isinstance(runner, str) or not runner.strip():
        print(
            "[FAIL] Missing meta.runner (results do not look CI-produced).",
            file=sys.stderr,
        )
        return 1
    if "placeholder" in runner.lower():
        print(f"[FAIL] Placeholder runner detected: {runner}", file=sys.stderr)
        return 1

    summary = data.get("summary", {})
    total = int(summary.get("scenarios_total", 0))
    success_rate = float(summary.get("success_rate", 0.0))
    status = summary.get("status")

    scenarios = data.get("scenarios", [])
    if not isinstance(scenarios, list):
        print("[FAIL] scenarios must be an array in results JSON.", file=sys.stderr)
        return 1

    if total != len(scenarios):
        print(
            f"[FAIL] scenarios_total ({total}) does not match scenarios length ({len(scenarios)}).",
            file=sys.stderr,
        )
        return 1

    rubric = data.get("rubric", {}) or {}
    min_success_rate = float(
        rubric.get("minimum_success_rate", DEFAULT_MIN_SUCCESS_RATE)
    )
    min_scenarios = int(rubric.get("minimum_scenarios", 1))

    rubric_errors = data.get("rubric_errors", [])
    if rubric_errors:
        print("[FAIL] Rubric validation errors present:", file=sys.stderr)
        for e in rubric_errors:
            print(f" - {e}", file=sys.stderr)
        return 1

    if status not in ("structural_pass", "pass"):
        print(f"[FAIL] Runner status is not pass: {status!r}", file=sys.stderr)
        return 1

    if total < min_scenarios:
        print(
            f"[FAIL] Only {total} scenarios, minimum required is {min_scenarios}.",
            file=sys.stderr,
        )
        return 1

    if success_rate < min_success_rate:
        print(
            f"[FAIL] Success rate {success_rate:.2f} below threshold {min_success_rate:.2f}.",
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
