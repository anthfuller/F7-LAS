"""Offline OPA CLI adapter with deterministic fail-closed behavior."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any


QUERY = "data.f7las.canonical.result"
IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[-_][a-z0-9]+)*$")


def _is_identifier(value: Any) -> bool:
    return (
        isinstance(value, str)
        and 3 <= len(value) <= 128
        and IDENTIFIER.fullmatch(value) is not None
    )


class OfflineOPA:
    """Evaluate one Rego decision without starting a network service."""

    def __init__(self, binary: str, policy_path: Path, timeout_seconds: float = 5.0) -> None:
        self.binary = binary
        self.policy_path = policy_path
        self.timeout_seconds = timeout_seconds

    @staticmethod
    def _deny(reason_code: str) -> dict[str, Any]:
        return {
            "decision": "deny",
            "reason_code": reason_code,
            "obligations": ["audit-required"],
        }

    def evaluate(self, policy_input: dict[str, Any]) -> dict[str, Any]:
        command = [
            self.binary,
            "eval",
            "--format=json",
            "--strict",
            "--fail",
            "--stdin-input",
            "--data",
            str(self.policy_path),
            QUERY,
        ]
        try:
            completed = subprocess.run(
                command,
                input=json.dumps(policy_input, sort_keys=True, separators=(",", ":")),
                capture_output=True,
                check=False,
                text=True,
                timeout=self.timeout_seconds,
            )
        except (OSError, subprocess.TimeoutExpired):
            return self._deny("pdp-unavailable")

        if completed.returncode != 0:
            return self._deny("pdp-evaluation-failed")

        try:
            payload = json.loads(completed.stdout)
            result = payload["result"][0]["expressions"][0]["value"]
            if set(result) != {"decision", "reason_code", "obligations"}:
                raise ValueError("unexpected decision fields")
            if result["decision"] not in {"permit", "deny"}:
                raise ValueError("unexpected decision")
            if not _is_identifier(result["reason_code"]):
                raise ValueError("unexpected reason code")
            if not isinstance(result["obligations"], list) or not all(
                _is_identifier(item) for item in result["obligations"]
            ):
                raise ValueError("unexpected obligations")
            if len(result["obligations"]) != len(set(result["obligations"])):
                raise ValueError("duplicate obligations")
            return result
        except (IndexError, KeyError, TypeError, ValueError, json.JSONDecodeError):
            return self._deny("pdp-invalid-response")
