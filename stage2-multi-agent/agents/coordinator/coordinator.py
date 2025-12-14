"""
F7-LAS Stage 2 – Coordinator Agent
Orchestration-only agent.
All actions are delegated; no direct tool or MCP execution.
Centralized PDP is mandatory before any remediation.
"""

from telemetry.audit import write_audit
from typing import Dict, List, Any
from telemetry.logger import log_event
from llm.azure_openai_client import AzureOpenAIClient


class CoordinatorAgent:
    def __init__(self, policy_gateway_client=None):
        """
        policy_gateway_client: optional handle to PDP/gateway (read-only for coordinator)
        """
        self.policy_gateway = policy_gateway_client
        self.llm = AzureOpenAIClient()

    def handle_request(self, user_request: str, run_id: str = "run-unknown") -> Dict[str, Any]:
        log_event(
            event_type="coordinator_request_received",
            payload={"user_request": user_request}
        )

        # === Decision point: planning ===
        plan = self._plan(user_request)

        # === Audit the decision (Layer 7) ===
        write_audit(
            run_id=run_id,
            stage="coordinator_plan",
            data=plan
        )

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
        system_prompt = (
            "You are the F7-LAS Coordinator. "
            "Plan investigation and remediation phases. "
            "Do NOT execute tools. Do NOT bypass the centralized PDP."
        )

        plan_text = self.llm.complete(system_prompt, user_request)

        plan = {
            "investigation_required": True,
            "remediation_possible": True,
            "llm_plan_summary": plan_text
        }

        log_event(
            event_type="coordinator_plan_created",
            payload=plan
        )

        return plan

    def _delegate(self, plan: Dict[str, Any]) -> List[Dict[str, str]]:
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
        approvals = []

        for task in tasks:
            if task["agent"] == "F7LAS-Remediator":
                approvals.append(
                    "Centralized PDP authorization and human approval required for any execution."
                )

        return approvals
