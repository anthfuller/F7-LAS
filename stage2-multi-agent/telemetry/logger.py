"""
F7-LAS Stage 2 – Telemetry Logger
Centralized logging for all agent activity (Layer 7).
"""

import json
import datetime
from typing import Any


def _json_safe(obj: Any):
    """
    Canonical serializer for telemetry events.
    Ensures logs never fail due to type errors.
    """
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    return str(obj)


def log_event(event_type: str, payload: dict):
    """
    Emit a structured log event.
    """
    event = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "event_type": event_type,
        "payload": payload,
    }

    print(json.dumps(event, default=_json_safe))
