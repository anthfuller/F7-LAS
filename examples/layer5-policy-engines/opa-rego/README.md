# OPA Rego PDP Demo (Layer 5)

This folder provides a runnable demonstration of the **F7-LAS Layer 5 Policy Decision Point (PDP)** using **Open Policy Agent (OPA)** and the Rego policy located at:

```
config/policies/l5/opa/agent_security_enforcement.rego
```

The demo shows how the PDP evaluates agent actions such as:

- `terminate_instance`
- `describe_instance`
- `list_instances`

…and how the **PEP (Policy Enforcement Point)** queries the PDP before tools are executed.

---

## Run the OPA PDP Locally

From the **repo root**, start the OPA container using:

```bash
docker compose -f examples/layer5-policy-engines/opa-rego/docker-compose.yml up
```

This will:

- Start OPA on `http://localhost:8181`
- Load the Layer-5 Rego policy automatically
- Watch policy files for changes

---

## Test the Policy Manually

### 1. Check the `allow` rule

```bash
curl -s -X POST   http://localhost:8181/v1/data/f7las/l5/enforcement/allow   -H 'Content-Type: application/json'   -d '{
        "input": {
          "action": "terminate_instance",
          "environment": "production",
          "current_time_ok_for_change": false
        }
      }'
```

**Expected Output:**

```json
{"result": false}
```

---

### 2. Retrieve the denial reason

```bash
curl -s -X POST   http://localhost:8181/v1/data/f7las/l5/enforcement/deny_message   -H 'Content-Type: application/json'   -d '{
        "input": {
          "action": "terminate_instance",
          "environment": "production",
          "current_time_ok_for_change": false
        }
      }'
```

**Example Output:**

```json
{"result": "Agent action denied by L5 Policy: Production modification outside of approved maintenance window or environment."}
```

---

## Using the PDP from the Python PEP

If you are using the OPA-backed PEP module located at:

```
src/policy/pep_opa.py
```

Example wiring:

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
```

---

## Notes

This is a **Stage‑1 demo PDP**, not a production deployment.

Future stages will add:

- Input validation  
- Authenticated PDP queries  
- Layer‑7 telemetry integration  
- Structured logs for every authorization request  
- Secure bundle mounting  
