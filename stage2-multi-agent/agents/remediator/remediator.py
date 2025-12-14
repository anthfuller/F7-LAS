from pdp.pdp import evaluate
from mcp.executor import execute
from telemetry.logger import log_event
from llm.azure_openai_client import AzureOpenAIClient

class RemediatorAgent:
    def __init__(self):
        self.llm = AzureOpenAIClient()

    def propose(self, investigation: dict):

        available_tools = [
            "signin_anomalies_last_180d",
            "azure_activity_last_180d",
            "security_alerts_last_180d"
        ]

        system_prompt = (
            "You are a security remediation agent. "
            "Given investigation findings, select the MOST relevant tools to run "
            "from the approved list. Respond with a JSON array of tool names only."
        )

        user_prompt = f"""
Investigation findings:
{investigation}

Approved tools:
{available_tools}
"""

        ranked_tools = self.llm.complete(system_prompt, user_prompt)

        # Defensive parse (no free-form execution)
        tools_to_run = [
            t for t in available_tools if t in ranked_tools
        ]

        action = "sentinel_read_only_query"
        pdp_result = evaluate(action, investigation)

        execution_results = {}
        if pdp_result["decision"] == "ALLOW":
            for tool in tools_to_run:
                execution_results[tool] = execute(tool)

        result = {
            "tools_selected": tools_to_run,
            "pdp_decision": pdp_result,
            "execution": "Executed" if execution_results else "Not executed"
        }

        log_event(
            event_type="remediation_completed",
            payload=result
        )

        return result
