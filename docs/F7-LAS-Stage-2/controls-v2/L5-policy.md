policy_request:
  action: string                   # requested verb
  tool_name: string                # declared at L4
  risk_class: enum("safe","medium_risk","high_impact")
  environment: enum("dev","test","prod","unknown")
  user_role: string                # optional stub for now
  time_window: string              # "business_hours" / "approved_window"
  sandbox_profile: enum("S1","S2","S3")
  supports_dry_run: boolean

policy_response:
  decision: enum(
    "allow",
    "allow_with_logging",
    "require_human_approval",
    "deny"
  )
  reason: string
  risk_score: enum("low","medium","high","block")
  dry_run_required: boolean
