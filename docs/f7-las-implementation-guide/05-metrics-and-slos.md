## 5.1 Risk Score Formula
risk_score = base_risk(tool_risk_tier)
× context_multiplier
× agent_factor

## 5.2 Key SLOs
- Prompt violation rate < 0.1%
- Retrieval trust score ≥ 0.8
- Planner loop termination < 8 steps
- Tool failure rate < 3%
- Sandbox escape attempts = 0
- Telemetry completeness > 99%
