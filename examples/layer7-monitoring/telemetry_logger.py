import json
import uuid
from datetime import datetime

def log_event(event: dict):
    """
    Lightweight L7 telemetry logger.
    Adds timestamp, correlation ID, and ensures schema consistency.
    """
    
    enriched = {
        "timestamp": datetime.utcnow().isoformat(),
        "layer": "L7",
        "correlation_id": event.get("correlation_id", str(uuid.uuid4())),
        "agent_id": event.get("agent_id", "unknown-agent"),
        "tool_name": event.get("tool_name", "none"),
        "action": event.get("action", "none"),
        "environment": event.get("environment", "none"),
        "arguments": event.get("arguments", {}),
        "policy_decision": event.get("policy_decision", "unknown"),
        "policy_reason": event.get("policy_reason", "N/A"),
        "status": event.get("status", "unknown"),
        "execution_time_ms": event.get("execution_time_ms", 0)
    }

    print(json.dumps(enriched))
