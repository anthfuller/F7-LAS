import importlib.util
import os
import shutil
import subprocess
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

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


@pytest.mark.skipif(OPA_BINARY is None, reason="OPA CLI is not installed")
def test_real_opa_path_is_deterministic_permitted_and_contract_valid():
    workflow = CanonicalWorkflow(opa_binary=OPA_BINARY)

    first = workflow.run(workflow_input())
    second = workflow.run(workflow_input())

    assert first == second
    assert record(first, "policy_decision")["decision"] == "permit"
    assert record(first, "execution_result")["status"] == "succeeded"
    assert record(first, "audit_event")["outcome"] == "success"
    assert_valid(first)


@pytest.mark.skipif(OPA_BINARY is None, reason="OPA CLI is not installed")
def test_real_opa_policy_denies_tampered_scope():
    opa = OfflineOPA(OPA_BINARY, DEFAULT_POLICY_PATH)
    result = opa.evaluate(
        {
            "request": {
                "dry_run": False,
                "scope": {
                    "scope_id": "other-boundary",
                    "environment": "lab",
                    "resource_ids": ["workspace-0001"],
                },
            },
            "actor": {
                "subject_id": "investigator-0001",
                "subject_type": "agent",
                "role": "investigator",
            },
            "action": {
                "tool": {"tool_id": "siem-query", "version": "1.0.0"},
                "operation": "workspace-health",
                "target": {
                    "scope_id": "other-boundary",
                    "environment": "lab",
                    "resource_ids": ["workspace-0001"],
                },
                "risk_tier": "low",
                "requires_approval": False,
            },
            "approval_status": "not_required",
            "policy_ref": CanonicalWorkflow._policy_ref(),
        }
    )

    assert result["decision"] == "deny"
    assert result["reason_code"] == "policy-denied"


def test_missing_opa_fails_closed_and_emits_valid_evidence():
    document = CanonicalWorkflow(opa_binary="/does/not/exist/opa").run(workflow_input())

    decision = record(document, "policy_decision")
    assert decision["decision"] == "deny"
    assert decision["authorization_basis"] == "none"
    assert decision["reason_code"] == "pdp-unavailable"
    assert record(document, "execution_result")["status"] == "not_executed"
    assert record(document, "audit_event")["outcome"] == "denied"
    assert_valid(document)


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
