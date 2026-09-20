"""Integrity verification for canonical F7-LAS evidence sets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from .contracts import digest_payload
from .validation import REPO_ROOT, SCHEMA_PATH, load_json, validate_record_set


CANONICAL_RECORD_ORDER = (
    "request",
    "context",
    "plan",
    "proposed_action",
    "approval",
    "policy_decision",
    "execution_result",
    "audit_event",
)


class EvidenceIntegrityError(ValueError):
    """A canonical evidence set failed integrity or correlation checks."""


def evidence_digest(document: dict[str, Any]) -> str:
    """Return a domain-separated digest of the complete canonical evidence set."""

    return digest_payload("evidence-set", document)


def _schema_validator() -> Draft202012Validator:
    return Draft202012Validator(
        load_json(SCHEMA_PATH),
        format_checker=FormatChecker(),
    )


def verify_evidence(document: dict[str, Any]) -> str:
    """Verify contracts plus the stricter single-action canonical evidence profile."""

    if not isinstance(document, dict):
        raise EvidenceIntegrityError("evidence document must be a JSON object")
    if set(document) != {"contract_set_version", "records"}:
        raise EvidenceIntegrityError("evidence document fields do not match the canonical profile")

    errors = validate_record_set(document, _schema_validator())
    if errors:
        raise EvidenceIntegrityError("; ".join(errors))

    records = document["records"]
    record_types = tuple(record["record_type"] for record in records)
    if record_types != CANONICAL_RECORD_ORDER:
        raise EvidenceIntegrityError(
            "canonical evidence must contain exactly one record of each type in workflow order"
        )

    audit = records[-1]
    expected_sources = [
        {
            "record_type": record["record_type"],
            "record_id": record["record_id"],
            "record_digest": record["record_digest"],
        }
        for record in records[:-1]
    ]
    if audit["source_records"] != expected_sources:
        raise EvidenceIntegrityError(
            "final audit_event.source_records must bind every preceding record in order"
        )

    action = records[3]
    decision = records[5]
    result = records[6]
    expected_object = {
        "record_id": action["record_id"],
        "record_digest": action["record_digest"],
    }
    if audit["object_ref"] != expected_object:
        raise EvidenceIntegrityError("final audit event must identify the canonical proposed action")
    if audit["event_type"] != "workflow-completed":
        raise EvidenceIntegrityError("final audit event must be workflow-completed")
    if audit["details"].get("execution_status") != result["status"]:
        raise EvidenceIntegrityError("audit execution_status does not match execution_result")
    if audit["details"].get("policy_reason_code") != decision["reason_code"]:
        raise EvidenceIntegrityError("audit policy_reason_code does not match policy_decision")

    return evidence_digest(document)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", required=True, type=Path)
    args = parser.parse_args()

    try:
        document = load_json(args.evidence)
        digest = verify_evidence(document)
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"F7-LAS evidence verification FAILED: {exc}")
        return 4

    relative = args.evidence
    try:
        relative = args.evidence.resolve().relative_to(REPO_ROOT)
    except ValueError:
        pass
    print(f"F7-LAS evidence verification PASSED: file={relative} digest={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
