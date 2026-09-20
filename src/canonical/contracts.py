"""Deterministic digest helpers shared by canonical producers and validators."""

from __future__ import annotations

import hashlib
from typing import Any

import rfc8785


ACTION_DIGEST_FIELDS = (
    "request_ref",
    "context_ref",
    "plan_ref",
    "step_id",
    "actor_id",
    "tool",
    "operation",
    "arguments",
    "target",
    "risk_tier",
    "requires_approval",
)


def digest_payload(domain: str, value: Any) -> str:
    canonical = rfc8785.dumps(value)
    material = f"F7-LAS:{domain}:1.0.0\n".encode("utf-8") + canonical
    return f"sha256:{hashlib.sha256(material).hexdigest()}"


def calculate_record_digest(record: dict[str, Any]) -> str:
    payload = {key: value for key, value in record.items() if key != "record_digest"}
    return digest_payload(f"record:{record['record_type']}", payload)


def calculate_action_digest(action: dict[str, Any]) -> str:
    return digest_payload(
        "action",
        {field: action[field] for field in ACTION_DIGEST_FIELDS},
    )


def calculate_output_digest(output: dict[str, Any]) -> str:
    return digest_payload("output", output)


def calculate_policy_bundle_digest(metadata: dict[str, Any], rego_source: bytes) -> str:
    """Bind versioned policy metadata to the exact executable Rego bytes."""

    return digest_payload(
        "policy-bundle",
        {
            "metadata": metadata,
            "rego_sha256": f"sha256:{hashlib.sha256(rego_source).hexdigest()}",
        },
    )
