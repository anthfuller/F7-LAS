"""
OPA-backed Policy Enforcement Point (PEP) for F7-LAS Layer 5.

This module:
- Builds the PDP input from the agent's tool call + execution context
- Calls the OPA HTTP API for `allow` and `deny_message`
- Returns a structured PolicyDecision
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict

import requests
from zoneinfo import ZoneInfo

from .pep_core import BasePEP, PolicyDecision

# OPA endpoints (can be overridden via config/env in future)
DEFAULT_ALLOW_URL = "http://localhost:8181/v1/data/f7las/l5/enforcement/allow"
DEFAULT_DENY_MSG_URL = "http://localhost:8181/v1/data/f7las/l5/enforcement/deny_message"

EASTERN_TZ = ZoneInfo("America/New_York")


class OPAPEP(BasePEP):
    """OPA-based Policy Enforcement Point implementation."""

    def __init__(
        self,
        allow_url: str = DEFAULT_ALLOW_URL,
        deny_msg_url: str = DEFAULT_DENY_MSG_URL,
        timeout: float = 3.0,
    ) -> None:
        self.allow_url = allow_url
        self.deny_msg_url = deny_msg_url
        self.timeout = timeout

    # ---------- internal helpers ----------

    def _build_pdp_input(self, tool_call: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Construct the `input` object sent to OPA.

        NOTE: For Stage-1 we derive `current_time_ok_for_change` from
        a simple 9–17 ET change-freeze window.
        """
        now_est = datetime.now(tz=EASTERN_TZ)
        current_time_ok = (now_est.hour < 9) or (now_est.hour >= 17)

        return {
            "tool_name": tool_call.get("tool_name"),
            "action": tool_call.get("action"),
            "environment": context.get("target_environment"),
            "user_role": context.get("initiating_user_role"),
            "current_time_ok_for_change": current_time_ok,
            "arguments": tool_call.get("arguments"),
        }

    def _extract_deny_message(self, raw_result: Any) -> str:
        """Handle OPA returning either a scalar or a list of messages."""
        if isinstance(raw_result, list) and raw_result:
            return str(raw_result[0])
        if isinstance(raw_result, str):
            return raw_result
        return "L5: Unknown policy denial reason."

    # ---------- public API ----------

    def authorize(self, tool_call: Dict[str, Any], context: Dict[str, Any]) -> PolicyDecision:
        """
        Evaluate the proposed tool call against the OPA PDP.

        Returns:
            PolicyDecision(allowed=True/False, reason=..., raw=...)
        """
        pdp_input = self._build_pdp_input(tool_call, context)
        payload = {"input": pdp_input}

        try:
            # 1) ask OPA if the action is allowed
            resp = requests.post(self.allow_url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            allow_result = resp.json().get("result", False)

            if allow_result is True:
                return PolicyDecision(
                    allowed=True,
                    reason="allow",
                    raw={"pdp_input": pdp_input, "pdp_result": allow_result},
                )

            # 2) if denied, ask for human-readable reason
            deny_resp = requests.post(self.deny_msg_url, json=payload, timeout=self.timeout)
            deny_resp.raise_for_status()
            deny_raw = deny_resp.json().get("result")
            deny_message = self._extract_deny_message(deny_raw)

            return PolicyDecision(
                allowed=False,
                reason=deny_message,
                raw={
                    "pdp_input": pdp_input,
                    "pdp_result": allow_result,
                    "deny_result": deny_raw,
                },
            )

        except requests.RequestException as exc:
            # Fail-closed: PDP unavailable → deny
            return PolicyDecision(
                allowed=False,
                reason=f"L5 PDP unavailable: {exc}",
                raw={"pdp_input": pdp_input},
            )
