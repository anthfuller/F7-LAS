"""
F7-LAS Stage 2 – Telemetry Logger
Centralized logging for all agent activity (Layer 7).
"""

import json
from datetime import datetime
from typing import Any
from uuid import UUID


def _json_safe(obj: Any):
    """
    Explicit JSON serializer.
    Fails loudly on unsupported types (by design).
    """
    if isinstance(obj, datetime):
        return obj.isoformat() + "Z"
    if isinstance(obj, UUID):
        return str(obj)
    if hasattr(obj, "__dict__"):
        return obj.__dict__

    raise TypeError(
        f"Object of type {obj.__class__.__name__} is not JSON serializable"
    )


def log_event(event_type: str, payload: dict):
    """
    Emit a structured telemetry event.
    """
    event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": event_type,
        "payload": payload,
    }

    # Stage-2: stdout logging (upgradeable to OTEL / Log Analytics)
    print(json.dumps(event, default=_json_safe))

