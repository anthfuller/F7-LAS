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


def _annotate_scenarios(scenarios: list[dict]) -> list[dict]:
    """
    Add placeholder result fields to each scenario.
    """
    return [
        {
            **s,
            "score": 1.0,
            "passed": True,
            "note": "Stage 0 placeholder result"
        }
        for s in scenarios if isinstance(s, dict)
    ]


def run_golden_dataset(scenarios_path: Path, rubric_path: Path) -> Dict[str, Any]:
    scenarios_raw = _safe_load_json(scenarios_path)
    rubric = _safe_load_json(rubric_path) or {}

    scenario_list = []
    if isinstance(scenarios_raw, dict) and "scenarios" in scenarios_raw:
        if isinstance(scenarios_raw["scenarios"], list):
            scenario_list = _annotate_scenarios(scenarios_raw["scenarios"])

    total_scenarios = len(scenario_list)
    passed = sum(1 for s in scenario_list if s.get("passed") is True)
    failed = total_scenarios - passed
    success_rate = passed / total_scenarios if total_scenarios else 0.0

    now = datetime.now(timezone.utc).isoformat()

    result: Dict[str, Any] = {
        "runner_version": "stage-0-placeholder",
        "timestamp_utc": now,
        "inputs": {
            "scenarios_path": str(scenarios_path),
            "rubric_path": str(rubric_path),
            "scenarios_loaded": scenarios_raw is not None,
            "rubric_loaded": bool(rubric)
        },
        "summary": {
            "scenarios_total": total_scenarios,
            "success_rate": round(success_rate, 3),
            "passed": passed,
            "failed": failed,
            "status": "placeholder"
        },
        "rubric": {
            "minimum_scenarios": rubric.get("minimum_scenarios", 1),
            "minimum_success_rate": rubric.get("minimum_success_rate", 0.8)
        },
        "scenarios": scenario_list,
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
