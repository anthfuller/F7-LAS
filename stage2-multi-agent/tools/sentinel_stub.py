"""
Sentinel tool stub (read-only).
Replace internals with real MCP or API calls later.
"""

from telemetry.logger import log_event


class SentinelStub:
    def query(self, kql: str):
        log_event("sentinel_query_called", {"kql": kql})
        return {"status": "stub", "data": []}
