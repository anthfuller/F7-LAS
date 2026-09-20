import copy
import importlib.util
import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from src.canonical import cli
from src.canonical.contracts import calculate_action_digest
from src.canonical.opa import OfflineOPA
from src.canonical.workflow import CanonicalWorkflow, WorkflowError


MODULE_PATH = Path("scripts/validate-contracts.py")
SPEC = importlib.util.spec_from_file_location("validate_contracts_behavioral", MODULE_PATH)
assert SPEC and SPEC.loader
contracts = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(contracts)

SCENARIO_PATH = Path("tests/behavioral_scenarios.json")
INPUT_PATH = Path("examples/canonical-workflow/request.json")
SCHEMA_PATH = Path("schemas/contracts/f7las-records-v1.schema.json")
OPA_BINARY = os.environ.get("OPA_BIN") or shutil.which("opa")

REQUIRED_CATEGORIES = {
    "denied",
    "expired",
    "malformed",
    "obligation",
    "permitted",
    "recovery",
    "tampered",
    "unauthorized",
    "unavailable",
}


def reject_duplicate_keys(pairs):
    document = {}
    for key, value in pairs:
        if key in document:
            raise ValueError(f"duplicate JSON key: {key}")
        document[key] = value
    return document


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=reject_duplicate_keys)


SCENARIO_SET = load_json(SCENARIO_PATH)
SCENARIOS = SCENARIO_SET["scenarios"]


def workflow_input():
    return load_json(INPUT_PATH)


def validator():
    return Draft202012Validator(
        load_json(SCHEMA_PATH),
        format_checker=FormatChecker(),
    )


def record(document, record_type):
    return next(item for item in document["records"] if item["record_type"] == record_type)


def observe_document(document):
    assert contracts.validate_record_set(document, validator()) == []
    decision = record(document, "policy_decision")
    result = record(document, "execution_result")
    audit = record(document, "audit_event")
    return {
        "admission": "accepted",
        "decision": decision["decision"],
        "decision_reason": decision["reason_code"],
        "execution": result["status"],
        "execution_reason": result["output"].get("reason_code"),
        "audit": audit["outcome"],
        "side_effects": result["side_effects"],
    }


def run_permitted(_monkeypatch, _tmp_path):
    return [observe_document(CanonicalWorkflow(opa_binary=OPA_BINARY).run(workflow_input()))]


def run_policy_denied(_monkeypatch, _tmp_path):
    workflow = CanonicalWorkflow(opa_binary=OPA_BINARY)
    real_evaluate = workflow.opa.evaluate

    def evaluate_unauthorized_arguments(value):
        policy_input = copy.deepcopy(value)
        policy_input["action"]["arguments"]["workspace_id"] = "workspace-other"
        return real_evaluate(policy_input)

    workflow.opa.evaluate = evaluate_unauthorized_arguments
    return [observe_document(workflow.run(workflow_input()))]


def run_refused_cli(monkeypatch, tmp_path, value, refusal_reason):
    input_path = tmp_path / f"{refusal_reason}.json"
    output_path = tmp_path / f"{refusal_reason}-records.json"
    input_path.write_text(json.dumps(value), encoding="utf-8")
    monkeypatch.setattr(
        "sys.argv",
        [
            "f7las-canonical",
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--opa-binary",
            "/does/not/matter",
        ],
    )
    exit_code = cli.main()
    records_emitted = 0
    if output_path.exists():
        records_emitted = len(load_json(output_path).get("records", []))
    return {
        "admission": "refused",
        "refusal_reason": refusal_reason,
        "cli_exit": exit_code,
        "records_emitted": records_emitted,
    }


def run_malformed_input(monkeypatch, tmp_path):
    value = workflow_input()
    value["unexpected"] = True
    with pytest.raises(WorkflowError, match="interface"):
        CanonicalWorkflow(opa_binary="/does/not/matter").run(value)
    return [run_refused_cli(monkeypatch, tmp_path, value, "malformed-input")]


def run_unauthorized_actor(monkeypatch, tmp_path):
    value = workflow_input()
    value["actor"]["subject_id"] = "unregistered-agent"
    with pytest.raises(WorkflowError, match="actor is outside"):
        CanonicalWorkflow(opa_binary="/does/not/matter").run(value)
    return [run_refused_cli(monkeypatch, tmp_path, value, "unauthorized-identity")]


def run_pdp_unavailable(_monkeypatch, _tmp_path):
    document = CanonicalWorkflow(opa_binary="/does/not/exist/opa").run(workflow_input())
    return [observe_document(document)]


def run_pdp_timeout(monkeypatch, _tmp_path):
    def timeout(*_args, **_kwargs):
        raise subprocess.TimeoutExpired(cmd="opa", timeout=5)

    monkeypatch.setattr("src.canonical.opa.subprocess.run", timeout)
    return [observe_document(CanonicalWorkflow(opa_binary="opa").run(workflow_input()))]


def run_pdp_malformed_response(monkeypatch, _tmp_path):
    completed = subprocess.CompletedProcess(args=["opa"], returncode=0, stdout="{}", stderr="")
    monkeypatch.setattr("src.canonical.opa.subprocess.run", lambda *_args, **_kwargs: completed)
    return [observe_document(CanonicalWorkflow(opa_binary="opa").run(workflow_input()))]


def run_tampered_action(monkeypatch, _tmp_path):
    original_execute = CanonicalWorkflow._execute

    def tampered_execute(request, action, approval, decision, execution_started_at):
        tampered = copy.deepcopy(action)
        tampered["arguments"]["workspace_id"] = "workspace-other"
        tampered["action_digest"] = calculate_action_digest(tampered)
        return original_execute(request, tampered, approval, decision, execution_started_at)

    monkeypatch.setattr(CanonicalWorkflow, "_execute", staticmethod(tampered_execute))
    return [observe_document(CanonicalWorkflow(opa_binary=OPA_BINARY).run(workflow_input()))]


def run_missing_obligation(_monkeypatch, _tmp_path):
    workflow = CanonicalWorkflow(opa_binary="/does/not/matter")
    workflow.opa.evaluate = lambda _value: {
        "decision": "permit",
        "reason_code": "mocked-permit",
        "obligations": ["audit-required"],
    }
    return [observe_document(workflow.run(workflow_input()))]


def run_expired_approval(monkeypatch, _tmp_path):
    original_execute = CanonicalWorkflow._execute

    def expired_execute(request, action, approval, decision, _execution_started_at):
        return original_execute(request, action, approval, decision, approval["expires_at"])

    monkeypatch.setattr(CanonicalWorkflow, "_execute", staticmethod(expired_execute))
    return [observe_document(CanonicalWorkflow(opa_binary=OPA_BINARY).run(workflow_input()))]


def run_recovery_after_pdp_unavailable(_monkeypatch, _tmp_path):
    workflow = CanonicalWorkflow(opa_binary=OPA_BINARY)
    real_evaluate = workflow.opa.evaluate
    attempts = 0

    def transient_evaluate(value):
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            return OfflineOPA._deny("pdp-unavailable")
        return real_evaluate(value)

    workflow.opa.evaluate = transient_evaluate
    first = workflow.run(workflow_input())
    second = workflow.run(workflow_input())
    return [observe_document(first), observe_document(second)]


DRIVERS = {
    "expired_approval": run_expired_approval,
    "malformed_input": run_malformed_input,
    "missing_obligation": run_missing_obligation,
    "pdp_malformed_response": run_pdp_malformed_response,
    "pdp_timeout": run_pdp_timeout,
    "pdp_unavailable": run_pdp_unavailable,
    "permitted": run_permitted,
    "policy_denied": run_policy_denied,
    "recovery_after_pdp_unavailable": run_recovery_after_pdp_unavailable,
    "tampered_action": run_tampered_action,
    "unauthorized_actor": run_unauthorized_actor,
}

REAL_OPA_DRIVERS = {
    "expired_approval",
    "permitted",
    "policy_denied",
    "recovery_after_pdp_unavailable",
    "tampered_action",
}


def test_behavioral_manifest_is_complete_and_well_formed():
    assert set(SCENARIO_SET) == {"scenario_set_version", "scenarios"}
    assert SCENARIO_SET["scenario_set_version"] == "1.0.0"
    assert isinstance(SCENARIOS, list) and SCENARIOS
    assert {scenario["category"] for scenario in SCENARIOS} == REQUIRED_CATEGORIES
    assert {scenario["driver"] for scenario in SCENARIOS} == set(DRIVERS)
    ids = [scenario["id"] for scenario in SCENARIOS]
    assert len(ids) == len(set(ids))
    for scenario in SCENARIOS:
        assert set(scenario) == {"id", "category", "title", "driver", "expected_attempts"}
        assert scenario["id"].startswith("BHV-")
        assert scenario["title"].strip()
        assert isinstance(scenario["expected_attempts"], list) and scenario["expected_attempts"]


@pytest.mark.parametrize("scenario", SCENARIOS, ids=lambda value: value["id"])
def test_behavioral_scenario(scenario, monkeypatch, tmp_path):
    if scenario["driver"] in REAL_OPA_DRIVERS and OPA_BINARY is None:
        pytest.skip("OPA CLI is not installed")

    actual_attempts = DRIVERS[scenario["driver"]](monkeypatch, tmp_path)

    assert actual_attempts == scenario["expected_attempts"]
