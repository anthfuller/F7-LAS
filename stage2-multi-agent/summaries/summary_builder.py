# summaries/summary_builder.py

from __future__ import annotations

import yaml
from pathlib import Path
from typing import Dict, Any


def build_summary(*, signals: Dict[str, Any], run_id: str) -> Dict[str, Any]:
    """
    Build a SOC analyst–ready case summary from domain signals.
    Deterministic. Rule-driven. No inference beyond rules.
    """

    rules_path = Path(__file__).parent / "summary_rules.yaml"
    with rules_path.open(encoding="utf-8") as f:
        rules_cfg = yaml.safe_load(f)

    domains = {d["domain"]: d for d in signals.get("domains", [])}

    # Default summary if no rule matches
    summary = {
        "case_id": run_id,
        "severity": "Informational",
        "finding": "No significant security findings",
        "assessment": "No rule conditions were met",
        "recommended_action": "No action required",
        "confidence": "High",
        "time_window": signals.get("time_window"),
        "domains_observed": list(domains.keys()),
    }

    for rule in rules_cfg.get("case_rules", []):
        required = rule.get("require_domains", [])
        if not all(d in domains for d in required):
            continue

        conditions_met = True

        for cond_key, expr in rule.get("conditions", {}).items():
            domain, metric = cond_key.split(".", 1)
            metric_value = domains[domain]["metrics"].get(metric, 0)

            if not _eval_condition(metric_value, expr):
                conditions_met = False
                break

        if conditions_met:
            summary.update({
                "severity": rule["outputs"]["severity"],
                "finding": rule["outputs"]["finding"],
                "assessment": rule["outputs"]["assessment"],
                "recommended_action": rule["outputs"]["recommended_action"],
                "confidence": rule["outputs"]["confidence"],
            })
            break

    return summary


def _eval_condition(value: int, expr: str) -> bool:
    """
    Evaluate simple numeric expressions like:
    >=1, ==0, >5
    """
    if expr.startswith(">="):
        return value >= int(expr[2:])
    if expr.startswith("<="):
        return value <= int(expr[2:])
    if expr.startswith("=="):
        return value == int(expr[2:])
    if expr.startswith(">"):
        return value > int(expr[1:])
    if expr.startswith("<"):
        return value < int(expr[1:])
    return False
