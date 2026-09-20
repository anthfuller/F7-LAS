package f7las.canonical

default result := {
    "decision": "deny",
    "reason_code": "policy-denied",
    "obligations": ["audit-required"],
}

expected_policy_ref := {
    "policy_id": "constraints-default-v1",
    "version": "v1.0",
    "policy_digest": "sha256:091de3f0a96ec85a610f42456aaba98c8d04e148b9f910c570f96af37795b44d",
}

result := {
    "decision": "permit",
    "reason_code": "permitted-synthetic-read",
    "obligations": ["audit-required", "offline-runtime-required"],
} if {
    input.policy_ref == expected_policy_ref
    input.approval_status == "not_required"
    input.request.dry_run == false
    input.request.scope.scope_id == "lab-boundary-0001"
    input.request.scope.environment == "lab"
    input.request.scope.resource_ids == ["workspace-0001"]
    input.actor.subject_id == "investigator-0001"
    input.actor.role == "investigator"
    regex.match("^sha256:[0-9a-f]{64}$", input.action.action_digest)
    input.action.action_digest == input.authorized_action_digest
    input.action.actor_id == input.actor.subject_id
    input.action.step_id == "step-0001"
    input.action.tool == {"tool_id": "siem-query", "version": "1.0.0"}
    input.action.operation == "workspace-health"
    input.action.arguments == {"workspace_id": "workspace-0001"}
    input.action.target == input.request.scope
    input.action.risk_tier == "low"
    input.action.requires_approval == false
}
