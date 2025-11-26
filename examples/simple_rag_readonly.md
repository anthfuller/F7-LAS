# Simple Read-Only RAG Query (Stage 0 — Experimental)

A minimal, safe, read-only example showing how F7-LAS governs a simple RAG lookup.

---

## Scenario

A security analyst asks:

> **“Summarize known indicators associated with QakBot.”**

This is a **low-risk**, read-only request:
- No tool execution  
- No remediation  
- No write actions  
- RAG-only lookup

Perfect for Stage 0 validation.

---

## 1. Coordinator (Layer 1 + Layer 3)

The coordinator applies PSP constraints and classifies the request:

- **Intent:** threat intelligence lookup  
- **Risk tier:** low  
- **Action type:** read-only

Policy result from `agent-policy.json`:

- ✔ Allowed  
- ✔ No HITL required  
- ✔ RAG retrieval permitted  
- ❌ Tool execution not allowed in this scenario

---

## 2. RAG Retrieval (Layer 2 — Grounding)

According to `rag-policy.json`, the coordinator may query:

- `kb_malware_intel`
- `kb_threat_reports`
- `kb_detection_engineering`

Disallowed:

- `customer_pii_raw`
- `internal_hr_data`

The RAG engine returns:

- MITRE ATT&CK references  
- Known QakBot C2 domains  
- Lateral movement notes  
- Persistence techniques

Telemetry (Layer 7):

- RAG collections used  
- Retrieval trace ID  
- Policy allow/deny reasoning  

---

## 3. Response Synthesis (Layer 3)

Under Stage 0 constraints:

- Coordinator summarizes retrieved intel  
- No tool calls attempted  
- No operational actions suggested  
- No speculative attribution included  
- PSP ensures neutral, safety-aligned tone

---

## 4. Policy Enforcement (Layer 5)

Even for safe queries, Layer 5 validates:

- Risk tier classification  
- No forbidden RAG collections accessed  
- No `write` / `modify` / `execute` actions  
- Decision reasoning logged

Outcome:  
✔ Allowed • ✔ Logged • ✔ Telemetry Recorded

---

## 5. Final Output (Layer 7)

Example structure included in the returned answer:

F7-LAS Trace ID: qbot-7741
Action Summary: Read-only RAG lookup
Tools Executed: None
Risk Tier: Low
Collections Queried: malware_intel, threat_reports


The answer is delivered to the analyst with no side effects.

---

## Purpose of This Example

This file provides:

- A **minimal, safe** Stage 0 example  
- A companion to the more complex multi-agent walkthrough  
- A “Hello World” demonstration for GitHub visitors  
- Clarity on how grounding + policy + telemetry work together  





