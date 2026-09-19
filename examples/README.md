# F7-LAS Examples

This folder contains minimal, instructional examples for each layer of the F7-LAS™ (Fuller 7-Layer Agentic Security) model.

These examples are **not production implementations**.  
They are **illustrative prototype demonstrations** of individual layer concepts. They do not prove end-to-end enforcement or production-ready hard guardrails.

## Included Layers

### Layer 1 — System Prompt  
Soft policy that defines intent, scope, and role boundaries for each agent persona.

### Layer 2 — Grounding  
Epistemic guardrails including allowlists and grounding profiles.

### Layer 3 — Planner  
A minimal planner stub that converts user intent into structured tool calls.

### Layer 4 — Tools  
Simple placeholder tools and schemas representing the Action Surface.

### Layer 5 — Policy Engine (PDP/PEP)  
Illustrative policy-engine patterns; these are not equivalent verified implementations:
- OPA / Rego  
- AWS Cedar  
- Azure custom PDP  
- Google SpiceDB  
- HashiCorp Sentinel  
- Kyverno  

### Layer 6 — Sandbox  
A minimal simulated execution wrapper and container example. Containment is not verified.

### Layer 7 — Monitoring & Telemetry  
A simple event schema + Python logger for auditability.

Each layer folder contains its own README with instructions.
