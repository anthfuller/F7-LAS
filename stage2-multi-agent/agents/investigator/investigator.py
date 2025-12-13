"""
F7-LAS Stage 2 – Investigator Agent
Analysis-only agent.
No remediation, no execution, no PDP calls.
"""

from typing import Dict, List, Any
from telemetry.logger import log_event


class InvestigatorAgent:
    def __init__(self, read_only_tools=None):
        """
        read_only_tools: optional interface for query-only data access
        (e.g., Sentinel/Defender stubs in read mode)
        """
        self.tools = read_only_tools

    def investigate(self, investigation_context: str) -> Dict[str, Any]:
        """
        Entry point for investigation.
        """
        log_event(
            event_type="investigation_started",
            payload={"context": investigation_context}
        )

        evidence = self._collect_evidence(investigation_context)
        hypotheses = self._analyze(evidence)

        result = {
            "findings_summary": "Evidence collected and analyzed.",
            "evidence": evidence,
            "hypotheses": hypotheses,
            "confidence_level": self._confidence(hypotheses),
        }

        log_event(
            event_type="investigation_completed",
            payload=result
        )

        return result

    def _collect_evidence(self, context: str) -> List[Dict[str, str]]:
        """
        Collect evidence using read-only sources.
        """
        evidence = [
            {
                "source": "placeholder",
                "detail": "Evidence collection stub"
            }
        ]

        log_event(
            event_type="evidence_collected",
            payload={"count": len(evidence)}
        )

        return evidence

    def _analyze(self, evidence: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Analyze evidence and generate hypotheses.
        """
        hypotheses = [
            {
                "hypothesis": "Potential suspicious activity detected",
                "likelihood": "Medium"
            }
        ]

        log_event(
            event_type="hypotheses_generated",
            payload={"count": len(hypotheses)}
        )

        return hypotheses

    def _confidence(self, hypotheses: List[Dict[str, str]]) -> str:
        """
        Determine confidence level.
        """
        return "Medium"
