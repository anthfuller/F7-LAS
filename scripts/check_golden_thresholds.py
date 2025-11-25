#!/usr/bin/env python3
"""
F7-LAS Golden Dataset Threshold Checker

Purpose:
    Prevent regressions in agent safety, reasoning, tool usage, and policy
    enforcement by ensuring that golden dataset scenario scores meet or exceed
    defined thresholds.

Inputs:
    - A JSON scenarios results file produced by run_golden_dataset.py
    - A JSON rubric file defining minimum required thresholds

Outputs:
    - PASS message (exit 0)
    - FAIL message with detailed reasons (exit 1)

Usage:
    python scripts/check_golden_thresholds.py \
        --results tests/golden_dataset/results.json \
        --rubric tests/golden_dataset/rubric.json
"""

import json
import sys
from pathlib import Path
import argparse


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[ERROR] Unable to load {path}: {e}", file=sys.stderr)
        sys.exit(1)


def check_thresholds(results: dict, rubric: dict) -> list[str]:
    errors = []

    min_score = rubric.get("min_score_per_scenario", 0.0)
    min_avg = rubric.get("min_average_score", 0.0)

    scenario_scores = results.get("scenario_scores", {})
    if not scenario_scores:
        return ["No scenario scores found in results.json — cannot validate."]

    # ---- Per-scenario checks ----
    for scenario_id, score in scenario_scores.items():
        if score < min_score:
            errors.append(
                f"Scenario '{scenario_id}' score {score} < minimum {min_score}"
            )

    # ---- Average score check ----
    avg = sum(scenario_scores.values()) / len(scenario_scores)
    if avg < min_avg:
        errors.append(
            f"Average score {avg:.2f} < minimum required {min_avg:.2f}"
        )

    # ---- Layer-specific thresholds (optional) ----
    layer_thresholds = rubric.get("layer_thresholds", {})
    layer_scores = results.get("layer_scores", {})

    for layer, threshold in layer_thresholds.items():
        score = layer_scores.get(layer)
        if score is None:
            errors.append(f"Missing layer score for '{layer}' in results.json")
            continue

        if score < threshold:
            errors.append(
                f"Layer '{layer}' score {score} < required {threshold}"
            )

    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True, help="Path to results.json")
    parser.add_argument("--rubric", required=True, help="Path to rubric.json")
    args = parser.parse_args()

    results_path = Path(args.results)
    rubric_path = Path(args.rubric)

    results = load_json(results_path)
    rubric = load_json(rubric_path)

    errors = check_thresholds(results, rubric)

    if errors:
        print("\n❌ F7-LAS Golden Dataset Thresholds FAILED:\n", file=sys.stderr)
        for e in errors:
            print(f" - {e}", file=sys.stderr)
        print("\nMerge blocked — thresholds not met.", file=sys.stderr)
        sys.exit(1)

    print("✅ F7-LAS Golden Dataset Thresholds PASSED.")
    sys.exit(0)


if __name__ == "__main__":
    main()
