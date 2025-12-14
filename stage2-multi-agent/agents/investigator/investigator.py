from typing import Dict, Any, List
from telemetry.logger import log_event
import os
from azure.identity import ClientSecretCredential
from azure.monitor.query import LogsQueryClient
from azure.monitor.query import LogsQueryStatus

class InvestigatorAgent:
    def __init__(self):
        self.workspace_id = os.getenv("SENTINEL_WORKSPACE_ID")

        cred = ClientSecretCredential(
            tenant_id=os.getenv("AZURE_TENANT_ID"),
            client_id=os.getenv("AZURE_CLIENT_ID"),
            client_secret=os.getenv("AZURE_CLIENT_SECRET"),
        )
        self.client = LogsQueryClient(cred)

    def investigate(self, context: str) -> Dict[str, Any]:
        log_event("investigation_started", {"context": context})

        evidence = self._query_sentinel()

        result = {
            "findings_summary": "Sentinel evidence collected (read-only).",
            "evidence": evidence,
            "hypotheses": self._hypotheses(evidence),
            "confidence_level": "Medium" if evidence else "Low"
        }

        log_event("investigation_completed", result)
        return result

    def _query_sentinel(self) -> List[Dict[str, Any]]:
        if not self.workspace_id:
            raise RuntimeError("Missing SENTINEL_WORKSPACE_ID")

        queries = [
            # 1) Sign-ins (if connected)
            ("signin_logs", """
SigninLogs
| where TimeGenerated > ago(180d)
| project TimeGenerated, UserPrincipalName, IPAddress, LocationDetails, ResultType
| take 20
"""),
            # 2) Azure Activity (if connected)
            ("azure_activity", """
AzureActivity
| where TimeGenerated > ago(180d)
| project TimeGenerated, OperationNameValue, ActivityStatusValue, Caller, ResourceGroup, ResourceId
| take 20
"""),
            # 3) SecurityAlert (if connected)
            ("security_alerts", """
SecurityAlert
| where TimeGenerated > ago(180d)
| project TimeGenerated, AlertName, Severity, CompromisedEntity, ProviderName, Description
| take 20
"""),
        ]

        evidence = []
        for name, q in queries:
            resp = self.client.query_workspace(self.workspace_id, q)
            if resp.status == LogsQueryStatus.PARTIAL:
                tables = resp.partial_data
            else:
                tables = resp.tables

            rows = []
            for table in tables:
                cols = [c.name for c in table.columns]
                for r in table.rows:
                    rows.append(dict(zip(cols, r)))

            evidence.append({"source": "sentinel", "query": name, "rows": rows, "count": len(rows)})

            log_event("sentinel_query_completed", {"query": name, "count": len(rows)})

        return evidence

    def _hypotheses(self, evidence: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        hyps = []
        for item in evidence:
            if item["count"] > 0:
                hyps.append({"hypothesis": f"Data present for {item['query']}", "likelihood": "Medium"})
        if not hyps:
            hyps.append({"hypothesis": "No data returned (connectors may not be ingesting yet)", "likelihood": "Low"})
        return hyps
