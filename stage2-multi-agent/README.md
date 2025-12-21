# Stage 2 — Multi-Agent Investigation for Microsoft Sentinel (F7-LAS)

## Overview

Stage 2 implements a policy-governed, evidence-first, multi-agent investigation pipeline for Microsoft Sentinel / Defender XDR environments, aligned to the F7-LAS (Fuller 7-Layer Agentic Security) model.

This stage demonstrates how agentic systems can be safely applied in a SOC context by enforcing strict separation of planning, evidence collection, judgment, and execution.

The system performs real KQL queries against Microsoft Sentinel and produces auditable investigation artifacts, without auto-remediation or uncontrolled reasoning.

---

## What This Is (and Is Not)

### ✅ This is:
- A real Sentinel investigation engine  
- A multi-agent SOC workflow  
- A policy-enforced execution model  
- A proof of F7-LAS in practice  
- A foundation for SOAR, hunting, or incident triage  

### ❌ This is not:
- A demo chatbot  
- A free-form “AI SOC analyst”  
- An auto-remediation system  
- A dashboard or visualization tool  

---

## Architecture Summary

```
Trigger (Analytic Rule / Playbook / Schedule / CLI)
        ↓
      main.py
        ↓
   Orchestrator
        ↓
  ┌───────────────┐
  │ Coordinator   │  ← Planning (no data access)
  └───────────────┘
        ↓
  ┌───────────────┐
  │ Investigator  │  ← Evidence collection (read-only KQL)
  └───────────────┘
        ↓
  ┌───────────────┐
  │ Remediator    │  ← Review + recommendation (HITL)
  └───────────────┘
        ↓
Evidence Bundle + SOC Case Summary
```

All Sentinel access flows through a centralized policy enforcement point (PDP/PEP).

---

## The Three Agent Roles

### 1️⃣ Coordinator (Planner)

**Purpose**
- Determines what evidence must be collected
- Produces a deterministic investigation plan

**Key Characteristics**
- ❌ Does NOT see logs  
- ❌ Does NOT interpret evidence  
- ❌ Does NOT execute queries  
- ✅ Uses tool contracts and policies only  

**SOC Analogy**
- Playbook author / investigation orchestrator

---

### 2️⃣ Investigator (Evidence Collector)

**Purpose**
- Executes the investigation plan
- Collects raw Sentinel telemetry only

**Key Characteristics**
- ✅ Executes read-only KQL queries  
- ✅ Enforced by PDP/PEP  
- ❌ No interpretation  
- ❌ No remediation  

**Data Sources**
- SigninLogs  
- AzureActivity  
- DeviceEvents  
- SecurityEvent  
- SecurityIncident  
- SentinelAudit  
- AAD risk tables (if enabled)  

**SOC Analogy**
- Tier-1 analyst gathering evidence

---

### 3️⃣ Remediator (Reviewer)

**Purpose**
- Reviews evidence
- Applies domain-based case logic
- Produces a recommendation only

**Key Characteristics**
- ✅ May re-query logs (read-only)  
- ❌ Cannot execute actions  
- ❌ Cannot bypass policy  
- ✅ Requires Human-in-the-Loop (HITL)  

**SOC Analogy**
- Tier-2 / Tier-3 analyst or incident commander

---

## Policy Enforcement (Critical)

All tool execution passes through:
- **MCP Executor (L4)** — centralized execution gateway
- **PDP/PEP (L5)** — YAML-defined policy enforcement

**Enforced Guarantees**
- Read-only KQL only  
- Approved tables only  
- Required time filters  
- Query limits enforced  
- Full audit trail (L7)  

**Agents cannot:**
- Invent tools  
- Bypass policy  
- Execute remediation  
- Escalate privileges  

---

## Evidence-First Design

The system produces structured investigation artifacts, not terminal output:

```
runs/<run_id>/
├── evidence/
│   ├── signinlogs.json
│   ├── azureactivity.json
│   ├── deviceevents.json
│   └── ...
├── domain_signals.json
├── summary.json
└── audit.json
```

### Why This Matters
- Analysts review cases, not logs  
- Evidence is reproducible  
- Summaries are traceable  
- Auditors can verify decisions  

---

## Domain-Based SOC Reasoning (Key Design)

The system does not reason per table.  
It reasons by **signal domains**:

| Domain            | Sentinel Tables                                           |
|-------------------|----------------------------------------------------------|
| Identity          | SigninLogs, AADUserRiskEvents, AADRiskyUsers             |
| Endpoint          | DeviceEvents, SecurityEvent                              |
| Azure Control Plane | AzureActivity                                          |
| Security Operations | SecurityIncident, SentinelAudit                        |
| Platform Health   | SentinelHealth                                           |
| Context           | Watchlists                                               |

This matches how real SOCs think and triage.

---

## What `main.py` Represents

`main.py` is **not** a production trigger.  
It simulates what would normally invoke the system.

### Real-World Equivalents:
- Microsoft Sentinel Analytics Rule  
- Sentinel Automation Rule / Playbook  
- Defender XDR incident lifecycle event  
- Scheduled hunting job  
- Analyst-initiated investigation  

### In production, `main.py` would be replaced by:
- Event Grid  
- Logic App  
- Azure Function  
- Sentinel playbook connector  

---

## F7-LAS Layer Mapping

| Layer               | Implementation                        |
|---------------------|----------------------------------------|
| L1 — Prompt         | Fixed role prompts per agent           |
| L2 — Grounding      | Sentinel alerts / incident context     |
| L3 — Planning       | Coordinator                            |
| L4 — Tools          | MCP Executor                           |
| L5 — Policy         | PDP / PEP (YAML)                       |
| L6 — Blast Radius   | No auto-remediation, HITL              |
| L7 — Monitoring     | Audit logs, summaries                  |

This stage exists to prove L3–L7 in real telemetry.

---

## Why This Matters

This design shows:
- ✅ How agentic systems can be safe in security  
- ✅ How AI can assist SOCs without replacing humans  
- ✅ How to prevent hallucination, drift, and overreach  
- ✅ How F7-LAS translates from theory to implementation  

---

## Status

- **Stage**: Investigation & Evidence  
- **Remediation**: Proposal-only  
- **Execution**: Disabled by design  

*This is intentional.*

---

## Next Stages (Future)

- Integration with Sentinel playbooks  
- Case persistence in external systems  
- Controlled remediation workflows  
- Multi-tenant policy isolation  
- Advanced domain signal extraction  

---
