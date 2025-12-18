"""
Stage2 PDP (Layer 5): Data-driven policy evaluation (YAML).
Authoritative decision point for ALL tool executions.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
import fnmatch
import yaml

from telemetry.audit import write_audit
from telemetry.logger import log_event


POLICY_DIR = Path(__file__).resolve().parents[1] / "policy" / "policies"


@dataclass
class Decision:
    decision: str  # ALLOW | DENY | HITL
    reason: str
    policy_id: Optional[str] = None
    rule_id: Optional[str] = None


def _load_yaml_policies() -> List[Dict[str, Any]]:
    policies: List[Dict[str, Any]] = []
    if not POLICY_DIR.exists():
        return policies

    for p in sorted(POLICY_DIR.glob("*.y*ml")):
        with p.open("r", encoding="utf-8", errors="ignore") as f:
            doc = yaml.safe_load(f) or {}
            doc["_source_file"] = str(p)
            policies.append(doc)

    return policies


def _action_matches(action: str, patterns: List[str]) -> bool:
    for pat in patterns:
        if pat == "*" or fnmatch.fnmatch(action, pat):
            return True
    return False


def evaluate(action: str, context: Dict[str, Any], run_id: str) -> Dict[str, str]:
    """
    Evaluate a single action against YAML policies.

    context expected keys (when applicable):
      - limit: int
      - has_time_filter: bool
    """
    policies = _load_yaml_policies()

    # Default if no policy matches
    final = Decision(decision="DENY", reason="No matching policy rule")

    for pol in policies:
        policy_id = pol.get("policy_id")

        for rule in pol.get("rules", []) or []:
            rule_id = rule.get("id")
            effect = (rule.get("effect") or "").upper().strip()
            patterns = rule.get("actions") or []

            if not _action_matches(action, patterns):
                continue

            # Enforce constraints only when action matches
            constraints = rule.get("constraints") or {}

            # max_limit constraint
            if "max_limit" in constraints:
                try:
                    limit = int(context.get("limit", 0))
                except Exception:
                    limit = 0

                if limit > int(constraints["max_limit"]):
                    final = Decision(
                        decision="DENY",
                        reason=f"limit {limit} exceeds max_limit {constraints['max_limit']}",
                        policy_id=policy_id,
                        rule_id=rule_id,
                    )
                    break

            # require_time_filter constraint
            if constraints.get("require_time_filter") is True:
                if context.get("has_time_filter") is not True:
                    final = Decision(
                        decision="DENY",
                        reason="missing required time filter",
                        policy_id=policy_id,
                        rule_id=rule_id,
                    )
                    break

            # Apply rule effect
            if effect in ("ALLOW", "DENY", "HITL"):
                final = Decision(
                    decision=effect,
                    reason=rule.get("reason")
                    or rule.get("description")
                    or effect,
                    policy_id=policy_id,
                    rule_id=rule_id,
                )
            else:
                final = Decision(
                    decision="DENY",
                    reason=f"invalid effect: {effect}",
                    policy_id=policy_id,
                    rule_id=rule_id,
                )

            # IMPORTANT FIX: stop once a rule decides
            break

        # Stop after first matching rule across policies
        if final.decision in ("ALLOW", "DENY", "HITL"):
            break

    # L7 telemetry
    write_audit(
        run_id=run_id,
        stage="pdp_decision",
        data={
            "action": action,
            "decision": final.decision,
            "reason": final.reason,
            "policy_id": final.policy_id,
            "rule_id": final.rule_id,
        },
    )

    log_event(
        "pdp_decision",
        {
            "run_id": run_id,
            "action": action,
            "decision": final.decision,
        },
    )

    return {"decision": final.decision, "reason": final.reason}
