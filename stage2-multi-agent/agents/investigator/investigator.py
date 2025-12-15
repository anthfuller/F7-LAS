from typing import List, Dict, Any
from datetime import timedelta

def _query_sentinel(self) -> List[Dict[str, Any]]:
    if not self.workspace_id:
        raise RuntimeError("Missing SENTINEL_WORKSPACE_ID")

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

    evidence = []

    for name, query in queries:
        resp = self.client.query_workspace(
            workspace_id=self.workspace_id,
            query=query,
            timespan=timedelta(days=180)
        )

        tables = []
        if hasattr(resp, "tables") and resp.tables:
            tables = resp.tables
        elif hasattr(resp, "partial_data") and resp.partial_data:
            tables = resp.partial_data

        rows = []

        for table in tables:
            # Normalize column names safely
            if table.columns:
                if isinstance(table.columns[0], str):
                    cols = table.columns
                else:
                    cols = [c.name for c in table.columns]
            else:
                cols = []

            for r in table.rows:
                rows.append(dict(zip(cols, r)))

        evidence.append({
            "source": "sentinel",
            "query": name,
            "rows": rows,
            "count": len(rows)
        })

        log_event(
            "sentinel_query_completed",
            {"query": name, "count": len(rows)}
        )

    return evidence
