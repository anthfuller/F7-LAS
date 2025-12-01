# examples/layer5-policy-engines/kyverno/pep_kyverno.py
from kubernetes import client, config

def submit_agent_action(tool_call: dict, ctx: dict) -> bool:
    """
    PEP: instead of executing directly, create an AgentAction CRD.
    Kyverno will validate; if denied, the create fails.
    """
    config.load_incluster_config()
    api = client.CustomObjectsApi()

    body = {
        "apiVersion": "agent.f7las.io/v1alpha1",
        "kind": "AgentAction",
        "metadata": {"name": "terminate-instance-request"},
        "spec": {
            "tool_action": tool_call.get("action"),
            "environment": ctx.get("environment"),
            "context": {
                "time_ok": ctx.get("current_time_ok_for_change", False)
            }
        }
    }

    try:
        api.create_cluster_custom_object(
            group="agent.f7las.io",
            version="v1alpha1",
            plural="agentactions",
            body=body,
        )
        # If we got here, Kyverno admitted it
        return True
    except client.ApiException as e:
        # If Kyverno denies, this will be a 4xx
        print("AgentAction denied by Kyverno / L5:", e)
        return False
