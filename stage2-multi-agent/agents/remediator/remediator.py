"""
F7-LAS Stage 2 – Remediator Agent (Layer 6)
Proposal-only. No execution. No LLM.
Human-in-the-loop required for any action.
"""

from __future__ import annotations

from typing import Any, Dict

from telemetry.audit import write_audit
from telemetry.logger import log_event


class RemediatorAgent:
    def __init__(self):
        pass

    def propose(
        self,
        *,
        case_summary: Dict[str, Any],
        evidence: Dict[str, Any],
        run_id: str
    ) -> Dict[str, Any]:
        """
        Produce a remediation proposal based on the SOC case summary
        and supporting evidence. No actions are executed here.
        """

        proposal = {
            "executed": False,
            "requires_hitl": True,
            "case_id": run_id,
            "severity": case_summary.get("severity"),
            "recommended_action": case_summary.get("recommended_action"),
            "notes": "Read-only deployment. Human approval required before any response action.",
        }

        # Optional evidence sanity check (no interpretation)
        evidence_sets = (evidence or {}).get("evidence", [])
        nonzero = [
            e for e in evidence_sets
            if isinstance(e, dict) and e.get("rowcount", 0) > 0
        ]

        if nonzero:
            proposal["evidence_support"] = {
                "datasets_with_findings": len(nonzero),
                "guidance": "Review supporting evidence before approving remediation."
            }
        else:
            proposal["evidence_support"] = {
                "datasets_with_findings": 0,
                "guidance": "No supporting evidence returned; no remediation recommended."
            }

        write_audit(
            run_id=run_id,
            stage="remediation_proposal",
            data=proposal
        )

        log_event(
            "remediator_proposal_created",
            {
                "run_id": run_id,
                "severity": proposal.get("severity"),
                "requires_hitl": True,
            }
        )

        return proposal
