from telemetry.audit import write_audit
from typing import List, Dict, Any
from telemetry.logger import log_event
import os
from datetime import timedelta

from azure.identity import ClientSecretCredential
from azure.monitor.query import LogsQueryClient
from azure.monitor.query import LogsQueryStatus


class InvestigatorAgent:
    def __init__(self):
        self.workspace_id = os.getenv("SENTINEL_WORKSPACE_ID")
        if not self.workspace_id:
            raise RuntimeError("Missing SENTINEL_WORKSPACE_ID")

        tenant_id = os.getenv("AZURE_TENANT_ID")
        client_id = os.getenv("AZURE_CLIENT_ID")
        client_secret = os.getenv("AZURE_CLIENT_SECRET")

        if not tenant_id or not client_id or not client_secret:
            raise RuntimeError("Missing AZURE_TENANT_ID / AZURE_CLIENT_ID / AZURE_CLIENT_SECRET")

        cred = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
        )
        self.client = LogsQueryClient(cred)

    def investigate(self, context: str, run_id: str = "run-unknown") -> Dict[str, Any]:
        log_event("investigation_started", {"context": context})

        evidence = self._query_sentinel()

        # Audit at decision boundary only (Layer 7)
        write_audit(
            run_id=run_id,
            stage="investigator_query",
            data={
                "workspace_id": self.workspace_id,
                "queries_executed": [e["query"] for e in evidence],
                "total_records": sum(e["count"] for e in evidence),
            },
        )

        result = {
            "findings_summary": "Sentinel evidence collected (read-only).",
            "evidence": evidence,
            "hypotheses": self._hypotheses(evidence),
            "confidence_level": "Medium" if any(e["count"] > 0 for e in evidence) else "Low",
        }

        log_event("investigation_completed", result)
        return result

    def _query_sentinel(self) -> List[Dict[str, Any]]:
        queries = [
            ("signin_logs", """
SigninLogs
| where TimeGenerated > ago(180d)
| project TimeGenerated, UserPrincipalName, IPAddress, LocationDetails, ResultType
| take 20
"""),
            ("azure_activity", """
AzureActivity
| where TimeGenerated > ago(180d)
| project TimeGenerated, OperationNameValue, ActivityStatusValue, Caller, ResourceGroup, ResourceId
| take 20
"""),
            ("security_alerts", """
SecurityAlert
| where TimeGenerated > ago(180d)
| project TimeGenerated, AlertName, Severity, CompromisedEntity, ProviderName, Description
| take 20
"""),
        ]

        evidence: List[Dict[str, Any]] = []

        for name, q in queries:
            resp = self.client.query_workspace(
                self.workspace_id,
                q,
                timespan=timedelta(days=180),
            )

            tables = resp.partial_data if resp.status == LogsQueryStatus.PARTIAL else resp.tables

            rows: List[Dict[str, Any]] = []
            for table in tables:
                # Some SDK shapes return column objects with .name, others can be strings.
                cols = []
                for c in table.columns:
                    cols.append(c.name if hasattr(c, "name") else str(c))

                for r in table.rows:
                    rows.append(dict(zip(cols, r)))

            evidence.append({
                "source": "sentinel",
                "query": name,
                "rows": rows,
                "count": len(rows),
            })

            log_event("sentinel_query_completed", {"query": name, "count": len(rows)})

        return evidence

    def _hypotheses(self, evidence: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        hyps: List[Dict[str, str]] = []
        for item in evidence:
            if item["count"] > 0:
                hyps.append({"hypothesis": f"Data present for {item['query']}", "likelihood": "Medium"})

        if not hyps:
            hyps.append({"hypothesis": "No data returned (connectors may not be ingesting yet)", "likelihood": "Low"})

        return hyps
