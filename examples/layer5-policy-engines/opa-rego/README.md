# OPA Rego PDP Demo (Layer 5)

This folder shows how to run the F7-LAS Layer 5 Policy Decision Point (PDP)
using **Open Policy Agent (OPA)** and the Rego policy in:

`config/policies/l5/opa/agent_security_enforcement.rego`

## Run OPA locally

From the repo root:

```bash
docker compose -f examples/layer5-policy-engines/opa-rego/docker-compose.yml up

OPA will listen on http://localhost:8181 and load the L5 policy.

Test the policy manually
curl -s -X POST \
  http://localhost:8181/v1/data/f7las/l5/enforcement/allow \
  -H 'Content-Type: application/json' \
  -d '{
    "input": {
      "action": "terminate_instance",
      "environment": "production",
      "current_time_ok_for_change": false
    }
  }'


Expected result:

{"result": false}


To see the deny reason:

curl -s -X POST \
  http://localhost:8181/v1/data/f7las/l5/enforcement/deny_message \
  -H 'Content-Type: application/json' \
  -d '{
    "input": {
      "action": "terminate_instance",
      "environment": "production",
      "current_time_ok_for_change": false
    }
  }'


---

## (Optional) Quick usage snippet in your demo agent

Somewhere in `src/demo_runner/` (or examples) you can wire the PEP like this:

```python
from src.policy.pep_opa import OPAPEP

pep = OPAPEP()

tool_call = {
    "tool_name": "aws_ec2_client",
    "action": "terminate_instance",
    "arguments": {"instance_id": "i-prod-1234"},
}

context = {
    "agent_id": "OpsAgent-v1",
    "target_environment": "production",
    "initiating_user_role": "devops_engineer",
}

decision = pep.authorize(tool_call, context)

if decision.is_allowed:
    print("L5: ALLOW → call tool")
else:
    print(f"L5: DENY → {decision.reason}")
