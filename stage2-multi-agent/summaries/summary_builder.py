from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


@dataclass
class SummaryResult:
    case_id: str
    severity: str
    finding: str
    assessment: str
    recommended_action: str
    confidence: str
    time_window: Optional[str] = None
    user: Optional[str] = None
    rule_id: Optional[str] = None


_OP_RE = re.compile(r"^\s*(==|!=|>=|<=|>|<)\s*(-?\d+(\.\d+)?)\s*$")


def _safe_number(v: Any) -> Optional[float]:
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        try:
            return float(v.strip())
        except Exception:
            return None
    return None


def _eval_condition(actual: Any, expr: str) -> bool:
    """
    Evaluate a simple numeric condition like '>=1', '==0', '<5'.
    Returns False if actual is not numeric or expr invalid.
    """
    m = _OP_RE.match(expr or "")
    if not m:
        return False

    op = m.group(1)
    target = float(m.group(2))
    a = _safe_number(actual)
    if a is None:
        return False

    if op == "==":
        return a == target
    if op == "!=":
        return a != target
    if op == ">=":
        return a >= target
    if op == "<=":
        return a <= target
    if op == ">":
        return a > target
    if op == "<":
        return a < target
    return False


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _index_domain_metrics(domain_signals: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    domain_signals expected:
      {
        "domains": [
          {"domain": "identity", "metrics": {...}},
          ...
        ],
        "time_window": {"start": "...", "end": "..."}  (optional)
      }
    """
    out: Dict[str, Dict[str, Any]] = {}
    for d in domain_signals.get("domains", []) or []:
        name = d.get("domain")
        if not name:
            continue
        out[name] = d.get("metrics", {}) or {}
    return out


def _format_time_window(domain_signals: Dict[str, Any]) -> Optional[str]:
    tw = domain_signals.get("time_window") or {}
    start = tw.get("start")
    end = tw.get("end")
    if start and end:
        return f"{start} – {end}"
    return None


def build_case_summary(
    *,
    run_id: str,
    domain_signals_path: Path,
    summary_rules_path: Path,
    output_path: Optional[Path] = None,
    user: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Deterministically build a SOC case summary from domain metrics.

    - No LLM usage
    - No table-specific logic
    - Rule order in YAML is priority order (first match wins)

    Returns the summary dict, and writes it if output_path is provided.
    """
    domain_signals = json.loads(domain_signals_path.read_text(encoding="utf-8"))
    rules_doc = _load_yaml(summary_rules_path)

    domain_metrics = _index_domain_metrics(domain_signals)
    time_window = _format_time_window(domain_signals)

    # Default summary if nothing matches
    summary = SummaryResult(
        case_id=run_id,
        severity="Informational",
        finding="No matching case rule",
        assessment="No case interpretation rule matched the extracted domain signals.",
        recommended_action="Review evidence or expand summary rules.",
        confidence="Low",
        time_window=time_window,
        user=user,
        rule_id=None,
    )

    for rule in (rules_doc.get("case_rules") or []):
        rule_id = rule.get("id") or "unnamed_rule"
        required = rule.get("require_domains") or rule.get("domains_required") or []
        conditions = rule.get("conditions") or {}
        outputs = rule.get("outputs") or {}

        # Must have required domains present in extracted metrics
        if any(dom not in domain_metrics for dom in required):
            continue

        # Evaluate conditions: keys like "identity.failed_signins"
        ok = True
        for key, expr in conditions.items():
            if "." not in key:
                ok = False
                break
            dom, metric = key.split(".", 1)
            actual = (domain_metrics.get(dom) or {}).get(metric)
            if not _eval_condition(actual, str(expr)):
                ok = False
                break

        if not ok:
            continue

        # First match wins
        summary = SummaryResult(
            case_id=run_id,
            severity=str(outputs.get("severity", "Informational")),
            finding=str(outputs.get("finding", f"Matched rule {rule_id}")),
            assessment=str(outputs.get("assessment", "")),
            recommended_action=str(outputs.get("recommended_action", "")),
            confidence=str(outputs.get("confidence", "Medium")),
            time_window=time_window,
            user=user,
            rule_id=rule_id,
        )
        break

    out = {
        "case_id": summary.case_id,
        "severity": summary.severity,
        "finding": summary.finding,
        "user": summary.user,
        "time_window": summary.time_window,
        "assessment": summary.assessment,
        "recommended_action": summary.recommended_action,
        "confidence": summary.confidence,
        "matched_rule_id": summary.rule_id,
    }

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    return out
