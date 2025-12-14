from pdp.pdp import evaluate
from mcp.executor import execute
from telemetry.logger import log_event

class RemediatorAgent:
    def propose(self, investigation: dict):

        # Simple, explicit reasoning (deterministic for now)
        tools_to_run = []

        for hyp in investigation.get("hypotheses", []):
            text = hyp.get("hypothesis", "").lower()

            if "sign-in" in text:
                tools_to_run.append("signin_anomalies_last_180d")

            if "resource" in text or "deployment" in text:
                tools_to_run.append("azure_activity_last_180d")

            if "alert" in text:
                tools_to_run.append("security_alerts_last_180d")

        # De-duplicate
        tools_to_run = list(set(tools_to_run))

        action = "sentinel_read_only_query"
        pdp_result = evaluate(action, investigation)

        execution_results = {}
        if pdp_result["decision"] == "ALLOW":
            for tool in tools_to_run:
                execution_results[tool] = execute(tool)

        result = {
            "action": action,
            "tools_selected": tools_to_run,
            "pdp_decision": pdp_result,
            "execution": "Executed" if execution_results else "Not executed"
        }

        log_event(
            event_type="remediation_completed",
            payload=result
        )

        return result


