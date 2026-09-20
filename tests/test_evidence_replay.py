import copy
import json
import os
import shutil
from pathlib import Path

import pytest

from src.canonical import evidence, replay
from src.canonical.contracts import calculate_record_digest
from src.canonical.evidence import EvidenceIntegrityError, evidence_digest, verify_evidence
from src.canonical.replay import ReplayMismatchError, replay_evidence
from src.canonical.validation import load_json
from src.canonical.workflow import CanonicalWorkflow


INPUT_PATH = Path("examples/canonical-workflow/request.json")
OPA_BINARY = os.environ.get("OPA_BIN") or shutil.which("opa")


def workflow_input():
    return load_json(INPUT_PATH)


def denied_evidence():
    return CanonicalWorkflow(opa_binary="/does/not/exist/opa").run(workflow_input())


def record(document, record_type):
    return next(item for item in document["records"] if item["record_type"] == record_type)


def test_evidence_verifier_accepts_complete_denial_and_is_deterministic():
    document = denied_evidence()

    first_digest = verify_evidence(document)
    second_digest = verify_evidence(copy.deepcopy(document))

    assert first_digest == second_digest == evidence_digest(document)
    assert first_digest.startswith("sha256:")


@pytest.mark.skipif(OPA_BINARY is None, reason="OPA CLI is not installed")
def test_evidence_verifier_accepts_complete_permit_path():
    document = CanonicalWorkflow(opa_binary=OPA_BINARY).run(workflow_input())

    assert verify_evidence(document) == evidence_digest(document)


@pytest.mark.parametrize(
    ("record_type", "field", "value"),
    [
        ("request", "mission", "tampered mission"),
        ("proposed_action", "action_digest", "sha256:" + "f" * 64),
        ("execution_result", "output_digest", "sha256:" + "f" * 64),
        ("audit_event", "outcome", "success"),
    ],
)
def test_evidence_verifier_detects_record_tampering(record_type, field, value):
    document = denied_evidence()
    record(document, record_type)[field] = value

    with pytest.raises(EvidenceIntegrityError):
        verify_evidence(document)


def test_evidence_verifier_requires_complete_ordered_audit_sources():
    document = denied_evidence()
    audit = record(document, "audit_event")
    audit["source_records"] = audit["source_records"][:-1]
    audit["record_digest"] = calculate_record_digest(audit)

    with pytest.raises(EvidenceIntegrityError, match="bind every preceding record"):
        verify_evidence(document)


def test_evidence_verifier_binds_audit_summary_to_decision_and_result():
    document = denied_evidence()
    audit = record(document, "audit_event")
    audit["details"]["policy_reason_code"] = "different-reason"
    audit["record_digest"] = calculate_record_digest(audit)

    with pytest.raises(EvidenceIntegrityError, match="policy_reason_code"):
        verify_evidence(document)


def test_evidence_verifier_rejects_extra_envelope_fields():
    document = denied_evidence()
    document["unsigned_note"] = "not covered by record digests"

    with pytest.raises(EvidenceIntegrityError, match="document fields"):
        verify_evidence(document)


def test_strict_evidence_loading_rejects_duplicate_keys(tmp_path):
    path = tmp_path / "duplicate.json"
    path.write_text('{"contract_set_version":"1.0.0","records":[],"records":[]}', encoding="utf-8")

    with pytest.raises(ValueError, match="duplicate JSON object key: records"):
        load_json(path)


def test_denied_outcome_replays_exactly_and_is_a_successful_replay():
    expected = denied_evidence()

    replayed = replay_evidence(
        workflow_input(),
        expected,
        opa_binary="/does/not/exist/opa",
    )

    assert replayed == expected
    assert record(replayed, "policy_decision")["decision"] == "deny"


@pytest.mark.skipif(OPA_BINARY is None, reason="OPA CLI is not installed")
def test_permitted_outcome_replays_exactly_with_real_opa():
    expected = CanonicalWorkflow(opa_binary=OPA_BINARY).run(workflow_input())

    assert replay_evidence(workflow_input(), expected, OPA_BINARY) == expected


def test_replay_detects_different_admitted_input():
    expected = denied_evidence()
    changed_input = workflow_input()
    changed_input["started_at"] = "2026-01-15T12:01:00Z"

    with pytest.raises(ReplayMismatchError, match="deterministic replay differs"):
        replay_evidence(changed_input, expected, opa_binary="/does/not/exist/opa")


def test_evidence_cli_returns_nonzero_for_tampering(tmp_path, monkeypatch):
    document = denied_evidence()
    record(document, "request")["mission"] = "tampered"
    path = tmp_path / "tampered.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["f7las-evidence", "--evidence", str(path)])

    assert evidence.main() == 4


def test_replay_cli_writes_exact_reproduction(tmp_path, monkeypatch):
    expected_path = tmp_path / "expected.json"
    output_path = tmp_path / "replayed.json"
    expected_path.write_text(json.dumps(denied_evidence()), encoding="utf-8")
    monkeypatch.setattr(
        "sys.argv",
        [
            "f7las-replay",
            "--input",
            str(INPUT_PATH),
            "--evidence",
            str(expected_path),
            "--output",
            str(output_path),
            "--opa-binary",
            "/does/not/exist/opa",
        ],
    )

    assert replay.main() == 0
    assert load_json(output_path) == load_json(expected_path)


def test_replay_cli_does_not_overwrite_reviewed_evidence(tmp_path, monkeypatch):
    expected_path = tmp_path / "expected.json"
    expected_path.write_text(json.dumps(denied_evidence()), encoding="utf-8")
    monkeypatch.setattr(
        "sys.argv",
        [
            "f7las-replay",
            "--input",
            str(INPUT_PATH),
            "--evidence",
            str(expected_path),
            "--output",
            str(expected_path),
        ],
    )

    assert replay.main() == 4
