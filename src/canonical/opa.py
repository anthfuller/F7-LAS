"""Offline OPA CLI adapter with deterministic fail-closed behavior."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

from .contracts import calculate_policy_bundle_digest


QUERY = "data.f7las.canonical.result"
IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[-_][a-z0-9]+)*$")
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_POLICY_METADATA_PATH = REPO_ROOT / "config" / "policies" / "policy-constraints-default.json"


def _is_identifier(value: Any) -> bool:
    return (
        isinstance(value, str)
        and 3 <= len(value) <= 128
        and IDENTIFIER.fullmatch(value) is not None
    )


class OfflineOPA:
    """Evaluate one Rego decision without starting a network service."""

    def __init__(
        self,
        binary: str,
        policy_path: Path,
        timeout_seconds: float = 5.0,
        policy_metadata_path: Path = DEFAULT_POLICY_METADATA_PATH,
    ) -> None:
        self.binary = binary
        self.policy_path = policy_path
        self.timeout_seconds = timeout_seconds
        self.policy_metadata_path = policy_metadata_path

    @staticmethod
    def _deny(reason_code: str) -> dict[str, Any]:
        return {
            "decision": "deny",
            "reason_code": reason_code,
            "obligations": ["audit-required"],
        }

    def policy_ref(self) -> dict[str, str]:
        """Describe the exact metadata and Rego bytes used by this adapter."""

        with self.policy_metadata_path.open("r", encoding="utf-8") as handle:
            metadata = json.load(handle)
        rego_source = self.policy_path.read_bytes()
        return {
            "policy_id": metadata["policy_id"],
            "version": metadata["version"],
            "policy_digest": calculate_policy_bundle_digest(metadata, rego_source),
        }

    def evaluate(self, policy_input: dict[str, Any]) -> dict[str, Any]:
        try:
            expected_policy_ref = self.policy_ref()
        except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError):
            return self._deny("pdp-policy-bundle-invalid")
        if (
            policy_input.get("policy_ref") != expected_policy_ref
            or policy_input.get("approval", {}).get("policy_ref") != expected_policy_ref
        ):
            return self._deny("pdp-policy-bundle-mismatch")

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
