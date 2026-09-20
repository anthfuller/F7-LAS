import copy
import importlib.util
import os
import shutil
import subprocess
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from src.canonical import cli
from src.canonical.contracts import calculate_action_digest, calculate_record_digest
from src.canonical.opa import OfflineOPA
from src.canonical.workflow import CanonicalWorkflow, DEFAULT_POLICY_PATH, WorkflowError


MODULE_PATH = Path("scripts/validate-contracts.py")
SPEC = importlib.util.spec_from_file_location("validate_contracts_workflow", MODULE_PATH)
assert SPEC and SPEC.loader
contracts = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(contracts)

SCHEMA_PATH = Path("schemas/contracts/f7las-records-v1.schema.json")
INPUT_PATH = Path("examples/canonical-workflow/request.json")
OPA_BINARY = os.environ.get("OPA_BIN") or shutil.which("opa")


def workflow_input():
    return contracts.load_json(INPUT_PATH)


def validator():
    return Draft202012Validator(
        contracts.load_json(SCHEMA_PATH),
        format_checker=FormatChecker(),
    )


def record(document, record_type):
    return next(item for item in document["records"] if item["record_type"] == record_type)


def assert_valid(document):
    assert contracts.validate_record_set(document, validator()) == []


def set_nested(document, path, value):
    target = document
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def rebind_approval(approval, decision):
    approval["record_digest"] = calculate_record_digest(approval)
    decision["approval_ref"] = {
        "record_id": approval["record_id"],
        "record_digest": approval["record_digest"],
    }


def capture_policy_input():
    captured = {}
    workflow = CanonicalWorkflow(opa_binary="/does/not/matter")

    def capture(value):
        captured.update(copy.deepcopy(value))
        return {
            "decision": "deny",
            "reason_code": "captured-for-test",
            "obligations": ["audit-required"],
        }

    workflow.opa.evaluate = capture
    workflow.run(workflow_input())
    return captured


@pytest.mark.skipif(OPA_BINARY is None, reason="OPA CLI is not installed")
def test_real_opa_path_is_deterministic_permitted_and_contract_valid():
    workflow = CanonicalWorkflow(opa_binary=OPA_BINARY)

    first = workflow.run(workflow_input())
    second = workflow.run(workflow_input())

    assert first == second
    assert record(first, "proposed_action")["requires_approval"] is True
    assert record(first, "approval")["status"] == "approved"
    assert record(first, "policy_decision")["decision"] == "permit"
    assert record(first, "policy_decision")["authorization_basis"] == "approved"
    assert record(first, "execution_result")["status"] == "succeeded"
    assert record(first, "audit_event")["outcome"] == "success"
    assert_valid(first)


@pytest.mark.skipif(OPA_BINARY is None, reason="OPA CLI is not installed")
def test_real_opa_policy_denies_tampered_scope():
    opa = OfflineOPA(OPA_BINARY, DEFAULT_POLICY_PATH)
    policy_input = capture_policy_input()
    policy_input["request"]["scope"]["scope_id"] = "other-boundary"
    policy_input["action"]["target"]["scope_id"] = "other-boundary"
    result = opa.evaluate(policy_input)

    assert result["decision"] == "deny"
    assert result["reason_code"] == "policy-denied"


@pytest.mark.skipif(OPA_BINARY is None, reason="OPA CLI is not installed")
def test_real_opa_policy_binds_arguments_and_action_digest():
    opa = OfflineOPA(OPA_BINARY, DEFAULT_POLICY_PATH)
    policy_input = capture_policy_input()
    assert opa.evaluate(policy_input)["decision"] == "permit"

    tampered_arguments = copy.deepcopy(policy_input)
    tampered_arguments["action"]["arguments"]["workspace_id"] = "workspace-other"
    assert opa.evaluate(tampered_arguments)["decision"] == "deny"

    tampered_digest = copy.deepcopy(policy_input)
    tampered_digest["action"]["action_digest"] = "sha256:" + "f" * 64
    assert opa.evaluate(tampered_digest)["decision"] == "deny"


@pytest.mark.skipif(OPA_BINARY is None, reason="OPA CLI is not installed")
@pytest.mark.parametrize(
    ("path", "value"),
    [
        (("approval", "request_ref", "record_digest"), "sha256:" + "f" * 64),
        (("approval", "action_ref", "action_digest"), "sha256:" + "f" * 64),
        (("approval", "approved_scope", "scope_id"), "other-boundary"),
        (("approval", "policy_ref", "version"), "v2.0"),
        (("approval", "authority", "subject_id"), "other-approver"),
        (("approval", "expires_at"), None),
        (("execution_at",), "2026-01-15T12:00:35Z"),
    ],
)
def test_real_opa_policy_denies_invalid_approval_binding(path, value):
    policy_input = capture_policy_input()
    set_nested(policy_input, path, value)

    result = OfflineOPA(OPA_BINARY, DEFAULT_POLICY_PATH).evaluate(policy_input)

    assert result["decision"] == "deny"
    assert result["reason_code"] == "policy-denied"


@pytest.mark.skipif(OPA_BINARY is None, reason="OPA CLI is not installed")
def test_real_opa_policy_denies_execution_exactly_at_expiration():
    policy_input = capture_policy_input()
    policy_input["execution_at"] = policy_input["approval"]["expires_at"]

    result = OfflineOPA(OPA_BINARY, DEFAULT_POLICY_PATH).evaluate(policy_input)

    assert result["decision"] == "deny"


@pytest.mark.skipif(OPA_BINARY is None, reason="OPA CLI is not installed")
def test_real_opa_policy_denies_decision_and_execution_at_expiration():
    policy_input = capture_policy_input()
    expires_at = policy_input["approval"]["expires_at"]
    policy_input["decision_at"] = expires_at
    policy_input["execution_at"] = expires_at

    result = OfflineOPA(OPA_BINARY, DEFAULT_POLICY_PATH).evaluate(policy_input)

    assert result["decision"] == "deny"


@pytest.mark.skipif(OPA_BINARY is None, reason="OPA CLI is not installed")
def test_real_opa_policy_denies_zero_length_approval_window():
    policy_input = capture_policy_input()
    issued_at = policy_input["approval"]["issued_at"]
    policy_input["approval"]["expires_at"] = issued_at
    policy_input["decision_at"] = issued_at
    policy_input["execution_at"] = issued_at

    result = OfflineOPA(OPA_BINARY, DEFAULT_POLICY_PATH).evaluate(policy_input)

    assert result["decision"] == "deny"


def test_missing_opa_fails_closed_and_emits_valid_evidence():
    document = CanonicalWorkflow(opa_binary="/does/not/exist/opa").run(workflow_input())

    decision = record(document, "policy_decision")
    assert decision["decision"] == "deny"
    assert decision["authorization_basis"] == "none"
    assert decision["reason_code"] == "pdp-unavailable"
    assert record(document, "execution_result")["status"] == "not_executed"
    assert record(document, "audit_event")["outcome"] == "denied"
    assert_valid(document)


def test_permit_missing_required_obligation_is_not_executed():
    workflow = CanonicalWorkflow(opa_binary="/does/not/matter")
    workflow.opa.evaluate = lambda _: {
        "decision": "permit",
        "reason_code": "mocked-permit",
        "obligations": ["audit-required"],
    }

    document = workflow.run(workflow_input())

    result = record(document, "execution_result")
    assert result["status"] == "not_executed"
    assert result["output"] == {
        "reason_code": "unfulfilled-policy-obligation",
        "missing_obligations": ["offline-runtime-required"],
        "unsupported_obligations": [],
    }
    assert record(document, "audit_event")["outcome"] == "not_executed"
    assert_valid(document)


def test_permit_with_unsupported_obligation_is_not_executed():
    workflow = CanonicalWorkflow(opa_binary="/does/not/matter")
    workflow.opa.evaluate = lambda _: {
        "decision": "permit",
        "reason_code": "mocked-permit",
        "obligations": ["audit-required", "offline-runtime-required", "unknown-obligation"],
    }

    document = workflow.run(workflow_input())

    result = record(document, "execution_result")
    assert result["status"] == "not_executed"
    assert result["output"]["unsupported_obligations"] == ["unknown-obligation"]
    assert_valid(document)


@pytest.mark.skipif(OPA_BINARY is None, reason="OPA CLI is not installed")
def test_executor_independently_rejects_tampered_action_binding():
    document = CanonicalWorkflow(opa_binary=OPA_BINARY).run(workflow_input())
    request = record(document, "request")
    action = copy.deepcopy(record(document, "proposed_action"))
    approval = record(document, "approval")
    decision = record(document, "policy_decision")
    action["arguments"]["workspace_id"] = "workspace-other"
    action["action_digest"] = calculate_action_digest(action)

    execution = CanonicalWorkflow._execute(
        request,
        action,
        approval,
        decision,
        "2026-01-15T12:00:06Z",
    )

    assert execution == {
        "status": "not_executed",
        "output": {"reason_code": "executor-binding-mismatch"},
    }


@pytest.mark.skipif(OPA_BINARY is None, reason="OPA CLI is not installed")
@pytest.mark.parametrize(
    ("field", "value", "expected_reason"),
    [
        (
            "request_ref",
            {"record_id": "request-0001", "record_digest": "sha256:" + "f" * 64},
            "executor-approval-binding-mismatch",
        ),
        (
            "approved_scope",
            {
                "scope_id": "other-boundary",
                "environment": "lab",
                "resource_ids": ["workspace-0001"],
            },
            "executor-approval-binding-mismatch",
        ),
        (
            "policy_ref",
            {
                "policy_id": "constraints-default-v1",
                "version": "v2.0",
                "policy_digest": "sha256:" + "f" * 64,
            },
            "executor-approval-binding-mismatch",
        ),
        (
            "expires_at",
            "2026-01-15T12:00:05Z",
            "executor-approval-invalid-at-execution",
        ),
        ("expires_at", None, "executor-approval-invalid-at-execution"),
    ],
)
def test_executor_independently_rejects_invalid_approval(field, value, expected_reason):
    document = CanonicalWorkflow(opa_binary=OPA_BINARY).run(workflow_input())
    request = record(document, "request")
    action = record(document, "proposed_action")
    approval = copy.deepcopy(record(document, "approval"))
    decision = copy.deepcopy(record(document, "policy_decision"))
    approval[field] = value
    if field == "policy_ref":
        decision["policy_ref"] = copy.deepcopy(value)
    rebind_approval(approval, decision)

    execution = CanonicalWorkflow._execute(
        request,
        action,
        approval,
        decision,
        "2026-01-15T12:00:06Z",
    )

    assert execution == {
        "status": "not_executed",
        "output": {"reason_code": expected_reason},
    }


@pytest.mark.skipif(OPA_BINARY is None, reason="OPA CLI is not installed")
@pytest.mark.parametrize(
    ("expires_at", "decision_at", "execution_at"),
    [
        ("2026-01-15T12:00:06Z", "2026-01-15T12:00:05Z", "2026-01-15T12:00:06Z"),
        ("2026-01-15T12:00:34Z", "2026-01-15T12:00:34Z", "2026-01-15T12:00:34Z"),
        ("2026-01-15T12:00:04Z", "2026-01-15T12:00:04Z", "2026-01-15T12:00:04Z"),
    ],
)
def test_executor_rejects_expiration_boundary_windows(expires_at, decision_at, execution_at):
    document = CanonicalWorkflow(opa_binary=OPA_BINARY).run(workflow_input())
    request = record(document, "request")
    action = record(document, "proposed_action")
    approval = copy.deepcopy(record(document, "approval"))
    decision = copy.deepcopy(record(document, "policy_decision"))
    approval["expires_at"] = expires_at
    decision["occurred_at"] = decision_at
    rebind_approval(approval, decision)

    execution = CanonicalWorkflow._execute(
        request,
        action,
        approval,
        decision,
        execution_at,
    )

    assert execution == {
        "status": "not_executed",
        "output": {"reason_code": "executor-approval-invalid-at-execution"},
    }


def test_malformed_opa_response_fails_closed(monkeypatch):
    completed = subprocess.CompletedProcess(args=["opa"], returncode=0, stdout="{}", stderr="")
    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: completed)

    result = OfflineOPA("opa", DEFAULT_POLICY_PATH).evaluate({})

    assert result == {
        "decision": "deny",
        "reason_code": "pdp-invalid-response",
        "obligations": ["audit-required"],
    }


def test_opa_evaluation_error_fails_closed(monkeypatch):
    completed = subprocess.CompletedProcess(args=["opa"], returncode=2, stdout="", stderr="bad policy")
    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: completed)

    result = OfflineOPA("opa", DEFAULT_POLICY_PATH).evaluate({})

    assert result["decision"] == "deny"
    assert result["reason_code"] == "pdp-evaluation-failed"


def test_workflow_refuses_identity_outside_fixed_path():
    request = workflow_input()
    request["actor"]["subject_id"] = "other-agent"

    with pytest.raises(WorkflowError, match="actor is outside"):
        CanonicalWorkflow(opa_binary="/does/not/matter").run(request)


def test_cli_returns_nonzero_for_denial_and_preserves_records(tmp_path, monkeypatch):
    output_path = tmp_path / "denied-records.json"
    monkeypatch.setattr(
        "sys.argv",
        [
            "f7las-canonical",
            "--input",
            str(INPUT_PATH),
            "--output",
            str(output_path),
            "--opa-binary",
            "/does/not/exist/opa",
        ],
    )

    assert cli.main() == 3
    document = contracts.load_json(output_path)
    assert record(document, "policy_decision")["decision"] == "deny"
    assert record(document, "execution_result")["status"] == "not_executed"
    assert_valid(document)
