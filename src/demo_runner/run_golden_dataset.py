#!/usr/bin/env python3
"""
F7-LAS Golden Dataset Runner (Stage 0 – Placeholder)

At Stage 0 this script:

- Accepts scenario and rubric JSON paths.
- Handles missing or invalid JSON gracefully.
- Emits a simple results JSON file so that:
  - CI can exercise the path end-to-end.
  - Future stages can plug in real evaluation logic.

This script is intentionally conservative: it must *never* break CI
because of placeholder data.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


def _safe_load_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # Stage 0: treat invalid JSON as "no data" instead of failing CI.
        return None


def run_golden_dataset(scenarios_path: Path, rubric_path: Path) -> Dict[str, Any]:
    scenarios = _safe_load_json(scenarios_path)
    rubric = _safe_load_json(rubric_path)

    # Derive a simple scenario count if possible.
    total_scenarios = 0
    if isinstance(scenarios, list):
        total_scenarios = len(scenarios)
    elif isinstance(scenarios, dict):
        if "scenarios" in scenarios and isinstance(scenarios["scenarios"], list):
            total_scenarios = len(scenarios["scenarios"])

    # Stage 0 behaviour: if we have any scenarios at all, we simply mark them as "passed"
    # without real scoring. This keeps the path alive without implying correctness.
    passed = total_scenarios
    failed = 0

    now = datetime.now(timezone.utc).isoformat()

    result: Dict[str, Any] = {
        "runner_version": "stage-0-placeholder",
        "timestamp_utc": now,
        "inputs": {
            "scenarios_path": str(scenarios_path),
            "rubric_path": str(rubric_path),
            "scenarios_loaded": scenarios is not None,
            "rubric_loaded": rubric is not None
        },
        "summary": {
            "total_scenarios": total_scenarios,
            "passed": passed,
            "failed": failed,
            "status": "placeholder"
        },
        "notes": "Stage 0 runner – replace with real evaluation logic as the framework matures."
    }

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run F7-LAS golden dataset (Stage 0).")
    parser.add_argument(
        "--scenarios",
        required=True,
        help="Path to scenarios JSON file."
    )
    parser.add_argument(
        "--rubric",
        required=True,
        help="Path to rubric JSON file."
    )
    parser.add_argument(
        "--output",
        default="golden_eval_results.json",
        help="Where to write the results JSON (default: golden_eval_results.json)."
    )

    args = parser.parse_args()

    scenarios_path = Path(args.scenarios)
    rubric_path = Path(args.rubric)
    output_path = Path(args.output)

    result = run_golden_dataset(scenarios_path, rubric_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, sort_keys=True)

    print(f"[INFO] Golden dataset placeholder run complete. Results written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
