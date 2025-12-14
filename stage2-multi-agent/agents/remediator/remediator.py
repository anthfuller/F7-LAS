from telemetry.audit import write_audit
from pdp.pdp import evaluate
from mcp.executor import execute
from hitl.approval import request_approval
from telemetry.logger import log_event
from llm.azure_openai_client import AzureOpenAIClient


class RemediatorAgent:
    def __init__(self):
        self.llm = AzureOpenAIClient()

    def propose(self, investigation: dict):

        approved_tools = [
            "signin_anomalies_last_180d",
            "azure_activity_last_180d",
            "security_alerts_last_180d"
        ]

        system_prompt = (
            "You are a security remediation agent. "
            "Given investigation findings, select the most relevant tools "
            "from the approved list. Respond ONLY with a JSON array of tool names."
        )

        user_prompt = f"""
Investigation findings:
{investigation}

Approved tools:
{approved_tools}
"""

        llm_response = self.llm.complete(system_prompt, user_prompt)

        # Defensive parsing: allow only registered tools
        tools_to_run = [t for t in approved_tools if t in llm_response]

        action = "sentinel_read_only_query"
        pdp_result = evaluate(action, investigation)

        execution_results = {}

        if pdp_result["decision"] == "REQUIRES_HUMAN_APPROVAL":
            approved = request_approval(action, investigation)

            if approved:
                for tool in tools_to_run:
                    execution_results[tool] = execute(tool)

        result = {
            "tools_selected": tools_to_run,
            "pdp_decision": pdp_result,
            "human_approved": bool(execution_results),
            "execution": "Executed" if execution_results else "Not executed"
        }

        log_event(
            event_type="remediation_completed",
            payload=result
        )

        return result

