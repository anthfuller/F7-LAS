"""
MCP Tool Registry
Approved read-only Sentinel queries only.
"""

SENTINEL_QUERIES = {
    "signin_anomalies_last_180d": """
SigninLogs
| where TimeGenerated > ago(180d)
| project TimeGenerated, UserPrincipalName, IPAddress, LocationDetails, ResultType
| take 20
""",

    "azure_activity_last_180d": """
AzureActivity
| where TimeGenerated > ago(180d)
| project TimeGenerated, OperationNameValue, ActivityStatusValue, Caller, ResourceGroup
| take 20
""",

    "security_alerts_last_180d": """
SecurityAlert
| where TimeGenerated > ago(180d)
| project TimeGenerated, AlertName, Severity, CompromisedEntity, ProviderName
| take 20
"""
}

def get_tool(tool_name: str) -> str:
    if tool_name not in SENTINEL_QUERIES:
        raise ValueError("Tool not registered in MCP")
    return SENTINEL_QUERIES[tool_name]
