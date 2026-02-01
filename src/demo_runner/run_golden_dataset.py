#!/usr/bin/env python3
"""
F7-LAS Golden Dataset Runner (CI-grade, deterministic)

This runner is intentionally *deterministic* and does **not** call an LLM.
Its job is to prevent CI theater - by validating:

- Scenario file integrity (schema + invariants)
- Rubric integrity (weights + thresholds)
- Producing a results JSON that CI can enforce

If you later plug in a real agent evaluation harness, keep this structural
validation and add an additional stage output (do not remove it).
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple


ALLOWED_RISK_TIERS = {"low", "medium", "high"}


@dataclass(frozen=True)
class ScenarioCheck:
    scenario_id: str
    passed: bool
    score: float
    errors: List[str]


def _load_json_strict(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _validate_rubric(rubric: dict) -> List[str]:
    errors: List[str] = []

    # minimums
    ms = rubric.get("minimum_scenarios")
    if not isinstance(ms, int) or ms < 1:
        errors.append("rubric.minimum_scenarios must be an int >= 1")

    mrate = rubric.get("minimum_success_rate")
    if not isinstance(mrate, (int, float)) or not (0.0 <= float(mrate) <= 1.0):
        errors.append("rubric.minimum_success_rate must be between 0 and 1")

    # criteria weights should sum to ~1.0
    criteria = rubric.get("criteria")
    if not isinstance(criteria, dict) or not criteria:
        errors.append("rubric.criteria must be a non-empty object")
    else:
        weights = []
        for k, v in criteria.items():
            if not isinstance(v, dict):
                errors.append(f"rubric.criteria.{k} must be an object")
                continue
            w = v.get("weight")
            if not isinstance(w, (int, float)):
                errors.append(f"rubric.criteria.{k}.weight must be a number")
                continue
            if float(w) < 0:
                errors.append(f"rubric.criteria.{k}.weight must be >= 0")
                continue
            weights.append(float(w))

        if weights:
            total = sum(weights)
            if not (0.99 <= total <= 1.01):
                errors.append(f"rubric.criteria weights must sum to 1.0 (got {total:.3f})")

    return errors


def _validate_scenario(idx: int, s: dict) -> ScenarioCheck:
    errors: List[str] = []

    if not isinstance(s, dict):
        return ScenarioCheck(scenario_id=f"index:{idx}", passed=False, score=0.0, errors=["scenario must be an object"])

    sid = s.get("id") or f"index:{idx}"
    if not isinstance(s.get("id"), str) or not s["id"].strip():
        errors.append("id must be a non-empty string")

    for field in ("title", "input"):
        if not isinstance(s.get(field), str) or not s[field].strip():
            errors.append(f"{field} must be a non-empty string")

    eb = s.get("expected_behavior")
    if not isinstance(eb, list) or not eb or not all(isinstance(x, str) and x.strip() for x in eb):
        errors.append("expected_behavior must be a non-empty array of strings")

    for field in ("allowed_tools", "forbidden_tools"):
        v = s.get(field)
        if not isinstance(v, list) or not all(isinstance(x, str) and x.strip() for x in v):
            errors.append(f"{field} must be an array of strings")

    rt = s.get("risk_tier")
    if not isinstance(rt, str) or rt not in ALLOWED_RISK_TIERS:
        errors.append(f"risk_tier must be one of {sorted(ALLOWED_RISK_TIERS)}")

    # Invariant: allowed_tools and forbidden_tools must not overlap.
    if isinstance(s.get("allowed_tools"), list) and isinstance(s.get("forbidden_tools"), list):
        overlap = set(s.get("allowed_tools", [])) & set(s.get("forbidden_tools", []))
        if overlap:
            errors.append(f"allowed_tools and forbidden_tools overlap: {sorted(overlap)}")

    passed = len(errors) == 0
    score = 1.0 if passed else 0.0
    return ScenarioCheck(scenario_id=str(sid), passed=passed, score=score, errors=errors)


def run_golden_dataset(scenarios_path: Path, rubric_path: Path, strict: bool) -> Dict[str, Any]:
    # Load JSON strictly when strict=True; otherwise return a failing-but-well-formed result.
    try:
        scenarios_raw = _load_json_strict(scenarios_path)
    except Exception as e:
        if strict:
            raise
        scenarios_raw = {"scenarios": [] , "_load_error": str(e)}

    try:
        rubric = _load_json_strict(rubric_path)
    except Exception as e:
        if strict:
            raise
        rubric = {"_load_error": str(e)}

    if not isinstance(scenarios_raw, dict) or "scenarios" not in scenarios_raw or not isinstance(scenarios_raw["scenarios"], list):
        msg = "scenarios.json must be an object with a 'scenarios' array"
        if strict:
            raise ValueError(msg)
        scenarios_raw = {"scenarios": [], "_error": msg}

    if not isinstance(rubric, dict):
        msg = "rubric.json must be a JSON object"
        if strict:
            raise ValueError(msg)
        rubric = {"_error": msg}

    rubric_errors = _validate_rubric(rubric)

    scenarios_list: list = scenarios_raw.get("scenarios", [])
    checks: List[ScenarioCheck] = []
    seen_ids: set[str] = set()
    duplicate_ids: List[str] = []

    for idx, s in enumerate(scenarios_list):
        chk = _validate_scenario(idx, s)
        checks.append(chk)
        if chk.scenario_id in seen_ids:
            duplicate_ids.append(chk.scenario_id)
        seen_ids.add(chk.scenario_id)

    if duplicate_ids:
        rubric_errors.append(f"duplicate scenario ids found: {sorted(set(duplicate_ids))}")

    total_scenarios = len(checks)
    passed = sum(1 for c in checks if c.passed)
    failed = total_scenarios - passed
    success_rate = (passed / total_scenarios) if total_scenarios else 0.0

    # enforce rubric minimum_scenarios vs actual count (fail-fast via result status)
    min_scen = rubric.get("minimum_scenarios", 1)
    if isinstance(min_scen, int) and total_scenarios < min_scen:
        rubric_errors.append(f"only {total_scenarios} scenarios present; rubric requires minimum_scenarios={min_scen}")

    status = "structural_pass" if (not rubric_errors and failed == 0 and total_scenarios > 0) else "structural_fail"

    now = datetime.now(timezone.utc).isoformat()
    sha = os.getenv("GITHUB_SHA")
    runner_version = "structural-v1"

    result: Dict[str, Any] = {
        "meta": {
            "runner": runner_version,
            "generated_at": now,
            "git_sha": sha,
            "strict": bool(strict),
        },
        "summary": {
            "scenarios_total": total_scenarios,
            "passed": passed,
            "failed": failed,
            "success_rate": round(float(success_rate), 3),
            "status": status,
        },
        "rubric": rubric,
        "rubric_errors": rubric_errors,
        "scenarios": [
            {
                "id": c.scenario_id,
                "passed": c.passed,
                "score": c.score,
                "errors": c.errors,
            }
            for c in checks
        ],
    }

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the F7-LAS golden dataset structural validation.")
    parser.add_argument("--scenarios", required=True, help="Path to scenarios.json")
    parser.add_argument("--rubric", required=True, help="Path to rubric.json")
    parser.add_argument(
        "--output",
        default="golden_eval_results.json",
        help="Where to write the results JSON (default: golden_eval_results.json).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail (non-zero) if inputs are missing/invalid instead of producing a best-effort result.",
    )

    args = parser.parse_args()

    scenarios_path = Path(args.scenarios)
    rubric_path = Path(args.rubric)
    output_path = Path(args.output)

    if args.strict:
        # Provide clear errors for missing files
        if not scenarios_path.exists():
            raise SystemExit(f"[ERROR] scenarios file not found: {scenarios_path}")
        if not rubric_path.exists():
            raise SystemExit(f"[ERROR] rubric file not found: {rubric_path}")

    result = run_golden_dataset(scenarios_path, rubric_path, strict=bool(args.strict))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, sort_keys=True)

    # CI should fail if structural validation fails.
    if result.get("summary", {}).get("status") != "structural_pass":
        print(f"[FAIL] Golden dataset structural validation failed. Results written to {output_path}")
        return 1

    print(f"[PASS] Golden dataset structural validation passed. Results written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
