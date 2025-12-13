"""
F7-LAS Stage 2 – Coordinator Agent
Orchestration-only agent.
All actions are delegated; no direct tool or MCP execution.
Centralized PDP is mandatory before any remediation.
"""

from typing import Dict, List, Any
from telemetry.logger import log_event


class CoordinatorAgent:
    def __init__(self, policy_gateway_client=None):
        """
        policy_gateway_client: optional handle to PDP/gateway (read-only for coordinator)
        """
        self.policy_gateway = policy_gateway_client

    def handle_request(self, user_request: str) -> Dict[str, Any]:
        """
        Entry point for coordination.
        """
        log_event(
            event_type="coordinator_request_received",
            payload={"user_request": user_request}
        )

        plan = self._plan(user_request)
        delegated = self._delegate(plan)

        response = {
            "coordinator_summary": "Request analyzed and tasks delegated.",
            "delegated_tasks": delegated,
            "approvals_required": self._identify_approvals(delegated),
        }

        log_event(
            event_type="coordinator_response_emitted",
            payload=response
        )

        return response

    def _plan(self, user_request: str) -> Dict[str, Any]:
        """
        Explicit planning step (Layer 3).
        No hidden execution.
        """
        plan = {
            "investigation_required": True,
            "remediation_possible": True,
            "notes": "Initial triage indicates investigation before remediation."
        }

        log_event(
            event_type="coordinator_plan_created",
            payload=plan
        )
        return plan

    def _delegate(self, plan: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Delegate work to Investigator and/or Remediator agents.
        """
        tasks = []

        if plan.get("investigation_required"):
            tasks.append({
                "agent": "F7LAS-Investigator",
                "task": "Collect evidence and produce findings."
            })

        if plan.get("remediation_possible"):
            tasks.append({
                "agent": "F7LAS-Remediator",
                "task": "Propose remediation plan (no execution without PDP approval)."
            })

        log_event(
            event_type="coordinator_tasks_delegated",
            payload={"tasks": tasks}
        )
        return tasks

    def _identify_approvals(self, tasks: List[Dict[str, str]]) -> List[str]:
        """
        Identify approvals required (PDP and/or human).
        """
        approvals = []

        for task in tasks:
            if task["agent"] == "F7LAS-Remediator":
                approvals.append(
                    "Centralized PDP authorization and human approval required for any execution."
                )

        return approvals
