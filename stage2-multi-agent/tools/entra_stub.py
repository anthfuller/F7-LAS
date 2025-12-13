"""
Entra ID tool stub (read-only).
"""

from telemetry.logger import log_event


class EntraStub:
    def get_user(self, user_id: str):
        log_event("entra_get_user_called", {"user_id": user_id})
        return {"status": "stub", "user": None}
