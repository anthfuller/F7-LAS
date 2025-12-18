"""
F7-LAS Stage 2 – Remediator Agent (Read-only + HITL)
- Produces remediation *proposals* only
- No execution, no claims of action taken
- Any real change requires HITL (outside Stage2 scope)
"""

from typing import Dict, Any
from telemetry.logger import log_event
from telemetry.audit import write_audit


class RemediatorAgent:
    def propose(self, investigation: Dict[str, Any], run_id: str = "run-unknown") -> Dict[str, Any]:
        # Keep proposals conservative and evidence-driven.
        proposals = []

        # If no evidence, propose HITL triage questions.
        total = investigation.get("summary", {}).get("total_rowcount", 0)
        if total == 0:
            proposals.append({
                "type": "HITL_REQUEST",
                "reason": "No rows returned from current tools. Confirm scope/time window or provide specific user/device/resource identifiers.",
            })
        else:
            proposals.append({
                "type": "HITL_REQUEST",
                "reason": "Evidence collected. Human reviewer should validate whether containment actions are warranted (write actions are out of scope for Stage2).",
            })

        result = {"proposals": proposals, "note": "No remediation executed (read-only Stage2)."}
        write_audit(run_id=run_id, stage="remediation_proposed", data=result)
        log_event(event_type="remediation_proposed", payload={"proposal_count": len(proposals)})

        return result
