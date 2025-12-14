"""
MCP Tool Registry
Read-only Sentinel tools only.
"""

SENTINEL_QUERIES = {
    "signin_anomalies_last_180d": """
SigninLogs
| where TimeGenerated > ago(180d)
| project TimeGenerated, UserPrincipalName, IPAddress, LocationDetails, ResultType
| take 20
"""
}

def get_tool(tool_name: str) -> str:
    if tool_name not in SENTINEL_QUERIES:
        raise ValueError("Tool not registered in MCP")
    return SENTINEL_QUERIES[tool_name]
