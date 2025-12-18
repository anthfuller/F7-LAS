"""
F7-LAS Stage 2 – Coordinator Agent (Deterministic)
- No tool execution
- No LLM "planning"
- Produces an explicit investigation plan: a list of registered read-only tools to run
"""

from typing import Dict, List, Any
from telemetry.logger import log_event
from telemetry.audit import write_audit


# Keyword -> tool mapping (contract-locked; no hidden tables)
DOMAIN_TOOLSETS = {
    "identity": ["signinlogs_recent_24h", "aaduserriskevents_recent_24h", "aadriskyusers_recent_24h"],
    "endpoint": ["deviceevents_recent_24h"],
    "azure": ["azureactivity_recent_24h"],
    "windows_auth": ["securityevent_failed_logons_24h", "securityevent_success_logons_24h"],
    "incidents": ["securityincident_recent_24h", "sentinelaudit_recent_24h"],
}

KEYWORDS = {
    "identity": ["signin", "sign-in", "login", "mfa", "conditional access", "entra", "azure ad", "aad", "risky"],
    "endpoint": ["device", "endpoint", "mde", "defender for endpoint", "process", "lateral", "edr"],
    "azure": ["azure", "subscription", "resource", "arm", "nsg", "rbac", "role", "policy", "key vault", "storage"],
    "windows_auth": ["4624", "4625", "logon", "securityevent", "windows server", "dc", "domain controller"],
    "incidents": ["incident", "sentinel", "analytics rule", "rule fired", "sentinelaudit"],
}

def _dedupe(seq: List[str]) -> List[str]:
    out=[]
    for x in seq:
        if x not in out:
            out.append(x)
    return out


class CoordinatorAgent:
    def handle_request(self, user_request: str, run_id: str = "run-unknown") -> Dict[str, Any]:
        text = (user_request or "").lower()

        selected_domains: List[str] = []
        for domain, kws in KEYWORDS.items():
            if any(k in text for k in kws):
                selected_domains.append(domain)

        # If no keywords hit, run a minimal baseline (safe + broad)
        if not selected_domains:
            selected_domains = ["incidents", "identity", "azure", "endpoint", "windows_auth"]

        tools: List[str] = []
        for d in selected_domains:
            tools.extend(DOMAIN_TOOLSETS[d])
        tools = _dedupe(tools)

        plan = {"domains": selected_domains, "tools": tools}

        write_audit(run_id=run_id, stage="coordinator_plan", data=plan)
        log_event(event_type="coordinator_plan_created", payload=plan)

        return plan
