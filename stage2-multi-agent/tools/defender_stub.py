"""
Defender tool stub (read-only).
"""

from telemetry.logger import log_event


class DefenderStub:
    def get_alert(self, alert_id: str):
        log_event("defender_get_alert_called", {"alert_id": alert_id})
        return {"status": "stub", "alert": None}
