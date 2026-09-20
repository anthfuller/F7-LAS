"""Deterministically replay and compare a canonical F7-LAS evidence set."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import rfc8785

from .evidence import EvidenceIntegrityError, evidence_digest, verify_evidence
from .validation import load_json
from .workflow import CanonicalWorkflow, WorkflowError


class ReplayMismatchError(ValueError):
    """A valid evidence set was not reproduced exactly by replay."""


def replay_evidence(
    workflow_input: dict[str, Any],
    expected: dict[str, Any],
    opa_binary: str = "opa",
) -> dict[str, Any]:
    """Verify prior evidence, rerun the workflow, and require canonical equality."""

    expected_digest = verify_evidence(expected)
    replayed = CanonicalWorkflow(opa_binary=opa_binary).run(workflow_input)
    replayed_digest = verify_evidence(replayed)
    if rfc8785.dumps(replayed) != rfc8785.dumps(expected):
        expected_records = expected["records"]
        replayed_records = replayed["records"]
        mismatch = "document structure"
        for old, new in zip(expected_records, replayed_records):
            if old != new:
                mismatch = old.get("record_type", "unknown record")
                break
        raise ReplayMismatchError(
            "deterministic replay differs at "
            f"{mismatch}: expected={expected_digest} replayed={replayed_digest}"
        )
    return replayed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--evidence", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--opa-binary", default="opa")
    args = parser.parse_args()

    if args.output is not None and args.output.resolve() in {
        args.input.resolve(),
        args.evidence.resolve(),
    }:
        print("F7-LAS replay FAILED: output must not overwrite input or reviewed evidence")
        return 4

    try:
        workflow_input = load_json(args.input)
        expected = load_json(args.evidence)
        replayed = replay_evidence(workflow_input, expected, args.opa_binary)
        if args.output is not None:
            args.output.write_text(json.dumps(replayed, indent=2) + "\n", encoding="utf-8")
    except (
        OSError,
        json.JSONDecodeError,
        KeyError,
        TypeError,
        ValueError,
        WorkflowError,
        EvidenceIntegrityError,
    ) as exc:
        print(f"F7-LAS replay FAILED: {exc}")
        return 4

    print(f"F7-LAS replay PASSED: digest={evidence_digest(replayed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
