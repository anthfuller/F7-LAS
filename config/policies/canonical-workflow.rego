package f7las.canonical

default result := {
    "decision": "deny",
    "reason_code": "policy-denied",
    "obligations": ["audit-required"],
}

result := {
    "decision": "permit",
    "reason_code": "approved-synthetic-read",
    "obligations": ["audit-required", "offline-runtime-required"],
} if {
    input.policy_ref.policy_id == "constraints-default-v1"
    input.policy_ref.version == "v1.0"
    regex.match("^sha256:[0-9a-f]{64}$", input.policy_ref.policy_digest)
    input.request.dry_run == false
    input.request.scope.scope_id == "lab-boundary-0001"
    input.request.scope.environment == "lab"
    input.request.scope.resource_ids == ["workspace-0001"]
    input.actor.subject_id == "investigator-0001"
    input.actor.role == "investigator"
    regex.match("^sha256:[0-9a-f]{64}$", input.action.action_digest)
    input.approval.status == "approved"
    input.approval.request_ref == input.request.reference
    input.action.request_ref == input.request.reference
    input.approval.action_ref == {
        "record_id": input.action.record_id,
        "record_digest": input.action.record_digest,
        "action_digest": input.action.action_digest,
    }
    input.approval.authority == {
        "subject_id": "approver-0001",
        "subject_type": "human",
        "role": "security-reviewer",
    }
    input.approval.policy_ref == input.policy_ref
    input.approval.approved_scope == input.action.target
    issued_at := time.parse_rfc3339_ns(input.approval.issued_at)
    decision_at := time.parse_rfc3339_ns(input.decision_at)
    execution_at := time.parse_rfc3339_ns(input.execution_at)
    expires_at := time.parse_rfc3339_ns(input.approval.expires_at)
    issued_at <= decision_at
    decision_at <= execution_at
    execution_at < expires_at
    input.action.actor_id == input.actor.subject_id
    input.action.step_id == "step-0001"
    input.action.tool == {"tool_id": "siem-query", "version": "1.0.0"}
    input.action.operation == "workspace-health"
    input.action.arguments == {"workspace_id": "workspace-0001"}
    input.action.target == input.request.scope
    input.action.risk_tier == "low"
    input.action.requires_approval == true
}
