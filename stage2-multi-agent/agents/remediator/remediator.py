from pdp.pdp import evaluate
from mcp.executor import execute
from telemetry.logger import log_event

class RemediatorAgent:
    def propose(self, investigation: dict):

        # Selection logic is explicit and auditable
        tool_name = "sentinel_read_only_signin"
        action = "sentinel_read_only_query"

        pdp_result = evaluate(action, investigation)

        execution_result = None
        if pdp_result["decision"] == "ALLOW":
            execution_result = execute("signin_anomalies_last_180d")
            execution_result = {
                "signin": execute("signin_anomalies_last_180d"),
                "activity": execute("azure_activity_last_180d"),
                "alerts": execute("security_alerts_last_180d")
            }

        result = {
            "action": action,
            "tools_executed": list(execution_result.keys()) if execution_result else [],
            "pdp_decision": pdp_result
        }

        log_event(
            event_type="remediation_completed",
            payload=result
        )

        return result

