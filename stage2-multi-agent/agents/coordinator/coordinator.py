"""
F7-LAS Stage 2 – Coordinator Agent (Layer 3)
Deterministic planner. No LLM-based tool selection.
Outputs an explicit investigation plan = registered read-only tool invocations.
"""

from __future__ import annotations

from typing import Any, Dict, List

from telemetry.audit import write_audit
from telemetry.logger import log_event


class CoordinatorAgent:
    def __init__(self):
        pass

    def handle_request(self, user_request: str, run_id: str) -> Dict[str, Any]:
        log_event("coordinator_started", {"run_id": run_id, "request": user_request})

        plan = self._plan(user_request)

        write_audit(run_id=run_id, stage="coordinator_plan", data={"request": user_request, "plan": plan})
        log_event("coordinator_plan_created", {"run_id": run_id, "steps": len(plan)})

        return {"plan": plan}

    def _plan(self, user_request: str) -> List[Dict[str, Any]]:
        """
        Minimal deterministic planning:
        - Select investigation lanes based on explicit keywords.
        - Default to identity + incident + azure activity if unclear.
        """
        q = (user_request or "").lower()

        steps: List[Dict[str, Any]] = []

        def add(tool: str, limit: int = 20):
            steps.append({"tool": tool, "params": {"limit": limit}})

        # Explicit lanes
        if any(k in q for k in ["sign-in", "signin", "mfa", "conditional access", "entra", "aad"]):
            add("signinlogs_last_24h")
            add("aaduserriskevents_last_7d")
            add("aadriskyusers_last_7d")

        if any(k in q for k in ["device", "endpoint", "mde", "process", "malware"]):
            add("deviceevents_last_24h")

        if any(k in q for k in ["azure", "resource", "subscription", "role", "rbac", "policy", "key vault", "nsg", "arm"]):
            add("azureactivity_last_24h")

        if any(k in q for k in ["windows", "server", "logon", "4625", "4624", "securityevent"]):
            add("securityevent_last_24h")

        if any(k in q for k in ["incident", "alert", "case"]):
            add("securityincident_last_30d")
            add("sentinelaudit_last_30d")

        # Default baseline if nothing matched (lowest-risk, broad visibility)
        if not steps:
            add("securityincident_last_30d")
            add("sentinelaudit_last_30d")
            add("signinlogs_last_24h")
            add("azureactivity_last_24h")

        return steps
