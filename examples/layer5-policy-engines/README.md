# Layer 5 — Policy Engine (PDP/PEP)

Layer 5 provides the **hard guardrails** of F7-LAS.

Every tool call proposed by Layer 3 must pass through:
- **PEP (Policy Enforcement Point)** — Python middleware  
- **PDP (Policy Decision Point)** — vendor policy engine  

This layer contains vendor-specific implementations for evaluating:

