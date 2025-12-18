"""
F7-LAS Stage 2 – Remediator Agent (Layer 3)
Proposal-only. No execution. No LLM. HITL required for any non-read-only action.
"""

from __future__ import annotations

from typing import Any, Dict

from telemetry.audit import write_audit
from telemetry.logger import log_event


class RemediatorAgent:
    def __init__(self):
        pass

    def propose(self, investigation: Dict[str, Any], *, run_id: str) -> Dict[str, Any]:
        """
        Produce a remediation *proposal* based on evidence. No actions are executed here.
        """
        evidence = (investigation or {}).get("evidence", [])

        proposal = {
            "executed": False,
            "requires_hitl": True,
            "recommended_actions": [],
            "notes": "Read-only deployment. Proposals require human approval and separate execution path."
        }

        # Minimal deterministic signals: if any tool returned rows, recommend analyst review
        nonzero = [e for e in evidence if isinstance(e, dict) and e.get("rowcount", 0) > 0]
        if nonzero:
            proposal["recommended_actions"].append({
                "type": "HITL_REVIEW",
                "reason": f"{len(nonzero)} evidence set(s) returned non-zero rows. Review raw results and decide next actions."
            })
        else:
            proposal["recommended_actions"].append({
                "type": "NO_FINDINGS",
                "reason": "No evidence returned from the executed plan. Consider widening time window or adding identifiers."
            })

        write_audit(run_id=run_id, stage="remediation_proposal", data=proposal)
        log_event("remediator_proposal_created", {"run_id": run_id, "nonzero_evidence": len(nonzero)})

        return proposal
