from telemetry.audit import write_audit
from telemetry.logger import log_event
from typing import List, Dict, Any
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
            raise RuntimeError(
                "Missing AZURE_TENANT_ID / AZURE_CLIENT_ID / AZURE_CLIENT_SECRET"
            )

        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
        )

        self.client = LogsQueryClient(credential)

    def investigate(self, context: str, run_id: str = "run-unknown") -> Dict[str, Any]:
        log_event("investigation_started", {"context": context})

        evidence = self._query_sentinel()

        # === Layer 7 Audit Boundary ===
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
            "confidence_level": "Medium"
            if any(e["count"] > 0 for e in evidence)
            else "Low",
        }

        log_event("investigation_completed", result)
        return result

    def _query_sentinel(self) -> List[Dict[str, Any]]:
        queries = [
            (
                "signin_logs",
                """
SigninLogs
| where TimeGenerated > ago(180d)
| project TimeGenerated, UserPrincipalName, IPAddress, LocationDetails, ResultType
| take 20
""",
            ),
            (
                "azure_activity",
                """
AzureActivity
| where TimeGenerated > ago(180d)
| project TimeGenerated, OperationNameValue, ActivityStatusValue, Caller, ResourceGroup, ResourceId
| take 20
""",
            ),
            (
                "security_alerts",
                """
SecurityAlert
| where TimeGenerated > ago(180d)
| project TimeGenerated, AlertName, AlertSeverity, CompromisedEntity, ProviderName, Description
| take 20
""",
            ),
        ]

        evidence: List[Dict[str, Any]] = []

        for name, query in queries:
            response = self.client.query_workspace(
                workspace_id=self.workspace_id,
                query=query,
                timespan=timedelta(days=180),
            )

            tables = (
                response.partial_data
                if response.status == LogsQueryStatus.PARTIAL
                else response.tables
            )

            rows: List[Dict[str, Any]] = []

            for table in tables:
                columns = [
                    col.name if hasattr(col, "name") else str(col)
                    for col in table.columns
                ]

                for row in table.rows:
                    rows.append(dict(zip(columns, row)))

            evidence.append(
                {
                    "source": "sentinel",
                    "query": name,
                    "rows": rows,
                    "count": len(rows),
                }
            )

            log_event(
                "sentinel_query_completed",
                {"query": name, "count": len(rows)},
            )

        return evidence

    def _hypotheses(self, evidence: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        hypotheses: List[Dict[str, str]] = []

        for item in evidence:
            if item["count"] > 0:
                hypotheses.append(
                    {
                        "hypothesis": f"Data present for {item['query']}",
                        "likelihood": "Medium",
                    }
                )

        if not hypotheses:
            hypotheses.append(
                {
                    "hypothesis": "No data returned (connectors may not be ingesting yet)",
                    "likelihood": "Low",
                }
            )

        return hypotheses
