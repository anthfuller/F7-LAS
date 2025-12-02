# HashiCorp Sentinel — F7-LAS Layer-5 Policy Engine Example

This folder contains the **Sentinel (HashiCorp)** policy example for F7-LAS Layer 5 (Policy Engine).

HashiCorp Sentinel is a *policy-as-code engine* used in Terraform Enterprise, Vault, Consul, and Nomad.  
This example is included to demonstrate how F7-LAS Layer-5 guardrails can be implemented across multiple vendor PDP systems.

## Note  
> This is **not** Microsoft Sentinel.  
> This folder refers to **HashiCorp Sentinel**, a policy enforcement engine.

---

## Example Policy: `f7las_l5.sentinel`

This policy denies dangerous actions, such as terminating a production instance outside an approved change window.

```hcl
# F7-LAS Layer 5 — deny terminate_instance in production when time_ok == false

main = rule {
  request := input.request

  action := request.action
  env := request.environment
  time_ok := request.current_time_ok_for_change

  # Allow only if the unsafe combination is NOT true
  not (action == "terminate_instance" && env == "production" && time_ok == false)
}
