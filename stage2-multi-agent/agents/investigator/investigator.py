"""
F7-LAS Stage 2 – Investigator Agent
Read-only evidence analysis.
Consumes replayed Sentinel evidence (JSON).
No live API calls. No remediation.
"""

import json
import os
from typing import Dict, Any, List
from telemetry.logger import log_event


class InvestigatorAgent:
    def __init__(self, evidence_path: str = "evidence"):
        self.evidence_path = evidence_path

    def investigate(self, context: str) -> Dict[str, Any]:
        log_event(
            event_type="investigation_started",
            payload={"context": context}
        )

        evidence = self._load_evidence()
        findings = self._analyze(evidence)

        result = {
            "findings_summary": "Evidence collected and analyzed.",
            "evidence": evidence,
            "hypotheses": findings["hypotheses"],
            "confidence_level": findings["confidence_level"]
        }

        log_event(
            event_type="investigation_completed",
            payload=result
        )

        return result

    def _load_evidence(self) -> List[Dict[str, Any]]:
        evidence_items = []

        for filename in os.listdir(self.evidence_path):
            if filename.endswith(".json"):
                with open(os.path.join(self.evidence_path, filename), "r") as f:
                    evidence_items.append(json.load(f))

        log_event(
            event_type="evidence_collected",
            payload={"count": len(evidence_items)}
        )

        return evidence_items

    def _analyze(self, evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
        hypotheses = []

        for item in evidence:
            hypotheses.append({
                "hypothesis": f"Potential risk detected: {item.get('alert_type')}",
                "severity": item.get("severity", "Unknown")
            })

        confidence = "Low"
        if any(h["severity"] == "High" for h in hypotheses):
            confidence = "High"
        elif hypotheses:
            confidence = "Medium"

        log_event(
            event_type="hypotheses_generated",
            payload={"count": len(hypotheses)}
        )

        return {
            "hypotheses": hypotheses,
            "confidence_level": confidence
        }
