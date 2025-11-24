# 4. Model Security Annex

## Common Threats
- Model extraction
- Surrogate replication
- Training-time poisoning
- Weight backdoors
- Membership inference
- Unauthorized fine-tuning
- Prompt-based introspection attacks

## Controls
- Hosted model endpoints with restricted access
- Model-version pinning
- Drift detection
- Evasion detection using adversarial probes
- Logging of input/output fingerprints

## Implementation
- Use Azure AI Studio gated deployments
- Monitor token distribution shifts
- Detect anomalous prompt entropy
