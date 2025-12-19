"""
F7-LAS Stage 2 – Orchestrator (Layer 3)
Coordinator -> Investigator -> Signal Extractor -> Summary Builder -> Remediator
"""

from __future__ import annotations

import uuid
import json
from pathlib import Path
from typing import Any, Dict

from telemetry.audit import write_audit
from telemetry.logger import log_event

from agents.coordinator.coordinator import CoordinatorAgent
from agents.investigator.investigator import InvestigatorAgent
from agents.remediator.remediator import RemediatorAgent

from signals.signal_extractor import extract_signals
from summaries.summary_builder import build_summary


class Orchestrator:
    def __init__(self):
        self.coordinator = CoordinatorAgent()
        self.investigator = InvestigatorAgent()
        self.remediator = RemediatorAgent()

    def run(self, user_request: str) -> Dict[str, Any]:
        run_id = f"run-{uuid.uuid4().hex[:12]}"

        # --- Run directory ---
        run_dir = Path("runs") / run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        log_event("orchestration_started", {"run_id": run_id, "request": user_request})
        write_audit(run_id=run_id, stage="run_started", data={"request": user_request})

        # --- Coordinator (planning only) ---
        coordination = self.coordinator.handle_request(
            user_request,
            run_id=run_id
        )
        plan = coordination.get("plan", [])

        # --- Investigator (real Sentinel evidence) ---
        investigation = self.investigator.investigate(
            plan,
            run_id=run_id
        )

        # --- Signal Extraction (domain metrics) ---
        signals = extract_signals(
            investigation=investigation,
            run_id=run_id
        )

        with open(run_dir / "signals.json", "w", encoding="utf-8") as f:
            json.dump(signals, f, indent=2)

        # --- SOC Case Summary ---
        case_summary = build_summary(
            signals=signals,
            run_id=run_id
        )

        with open(run_dir / "case_summary.json", "w", encoding="utf-8") as f:
            json.dump(case_summary, f, indent=2)

        # --- Remediator (proposal only) ---
        remediation = self.remediator.propose(
            case_summary=case_summary,
            evidence=investigation,
            run_id=run_id
        )

        result = {
            "run_id": run_id,
            "case_summary": case_summary,
            "signals": signals,
            "remediation": remediation,
        }

        write_audit(
            run_id=run_id,
            stage="run_completed",
            data={"summary": {"domains": list(signals.keys())}},
        )
        log_event(
            "orchestration_completed",
            {"run_id": run_id, "domains": list(signals.keys())},
        )

        return result
