from telemetry.logger import log_event
from mcp.tools import get_tool
from azure.identity import ClientSecretCredential
from azure.monitor.query import LogsQueryClient
import os

def execute(tool_name: str):
    query = get_tool(tool_name)

    credential = ClientSecretCredential(
        tenant_id=os.getenv("AZURE_TENANT_ID"),
        client_id=os.getenv("AZURE_CLIENT_ID"),
        client_secret=os.getenv("AZURE_CLIENT_SECRET"),
    )

    client = LogsQueryClient(credential)
    workspace_id = os.getenv("SENTINEL_WORKSPACE_ID")

    response = client.query_workspace(workspace_id, query)

    log_event(
        event_type="mcp_tool_executed",
        payload={"tool": tool_name}
    )

    return response
