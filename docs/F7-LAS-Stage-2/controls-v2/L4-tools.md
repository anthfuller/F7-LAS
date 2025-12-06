tool:
  name: string
  description: string
  capability_class: enum("safe", "medium_risk", "high_impact")
  allowed_actions: list(string)      # Explicit verbs only
  required_policy: boolean           # Must pass PEP/PDP
  sandbox_profile: enum("S1","S2","S3")
  inputs:
    - name: string
      type: string                   # strict types only
      required: boolean
      sanitize: enum("text","path","url","id")
  outputs:
    - name: string
      type: string
      sanitize: enum("text","path","url","id")
  supports_dry_run: boolean
