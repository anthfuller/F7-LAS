"""
F7-LAS Stage 2 – Telemetry Logger
Centralized logging for all agent activity (Layer 7).
"""

import json
import datetime


def log_event(event_type: str, payload: dict):
    """
    Emit a structured log event.
    """
    event = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "event_type": event_type,
        "payload": payload
    }

    # Stage-2: stdout logging (can be replaced with Log Analytics, Sentinel, etc.)
    print(json.dumps(event))
