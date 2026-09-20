import copy
import importlib.util
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


MODULE_PATH = Path("scripts/validate-contracts.py")
SPEC = importlib.util.spec_from_file_location("validate_contracts", MODULE_PATH)
assert SPEC and SPEC.loader
contracts = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(contracts)

SCHEMA_PATH = Path("schemas/contracts/f7las-records-v1.schema.json")
FIXTURE_PATH = Path("schemas/contracts/examples/approved-dry-run.json")


def fixture():
    return contracts.load_json(FIXTURE_PATH)


def validator():
    return Draft202012Validator(
        contracts.load_json(SCHEMA_PATH),
        format_checker=FormatChecker(),
    )


def record(document, record_type):
    return next(item for item in document["records"] if item["record_type"] == record_type)


def cross_errors(document):
    return contracts.validate_record_set(document, validator())


def test_canonical_contract_example_is_valid():
    assert contracts.validate_all() == []


def test_schema_rejects_approved_record_without_expiry():
    document = fixture()
    approval = record(document, "approval")
    approval["expires_at"] = None
    assert list(validator().iter_errors(approval))


def test_schema_rejects_deny_with_approval_basis():
    document = fixture()
    decision = record(document, "policy_decision")
    decision["decision"] = "deny"
    assert list(validator().iter_errors(decision))


def test_schema_rejects_not_executed_with_start_time():
    document = fixture()
    result = record(document, "execution_result")
    result["started_at"] = "2026-01-15T12:00:06Z"
    assert list(validator().iter_errors(result))


def test_schema_rejects_failed_result_without_error_and_timestamps():
    document = fixture()
    result = record(document, "execution_result")
    result["status"] = "failed"
    assert list(validator().iter_errors(result))


def test_load_json_rejects_duplicate_keys(tmp_path):
    path = tmp_path / "duplicate.json"
    path.write_text('{"record_id":"first","record_id":"second"}', encoding="utf-8")
    try:
        contracts.load_json(path)
    except ValueError as exc:
        assert "duplicate JSON object key: record_id" in str(exc)
    else:
        raise AssertionError("duplicate JSON key was accepted")


def test_cross_validator_enforces_cardinality():
    document = fixture()
    document["records"].insert(2, copy.deepcopy(record(document, "context")))
    assert any("exactly one context" in error for error in cross_errors(document))


def test_cross_validator_rejects_reference_digest_mismatch():
    document = fixture()
    record(document, "plan")["context_ref"]["record_digest"] = "sha256:" + "f" * 64
    assert any(
        "plan.context_ref.record_digest does not match context" in error
        for error in cross_errors(document)
    )


def test_cross_validator_rejects_scope_mismatch():
    document = fixture()
    record(document, "proposed_action")["target"]["scope_id"] = "other-boundary"
    assert any("target must exactly equal request scope" in error for error in cross_errors(document))


def test_cross_validator_rejects_policy_mismatch():
    document = fixture()
    record(document, "policy_decision")["policy_ref"]["version"] = "v2.0"
    assert any("policy_ref must exactly equal" in error for error in cross_errors(document))


def test_cross_validator_rejects_unregistered_policy_digest():
    document = fixture()
    bad_digest = "sha256:" + "f" * 64
    record(document, "approval")["policy_ref"]["policy_digest"] = bad_digest
    record(document, "policy_decision")["policy_ref"]["policy_digest"] = bad_digest
    assert any("does not match the repository policy" in error for error in cross_errors(document))


def test_cross_validator_rejects_expired_approval():
    document = fixture()
    record(document, "approval")["expires_at"] = "2026-01-15T12:00:04Z"
    assert any("after approval expiry" in error for error in cross_errors(document))


def test_cross_validator_rejects_execution_after_approval_expiry():
    document = fixture()
    record(document, "request")["constraints"]["dry_run"] = False
    record(document, "approval")["expires_at"] = "2026-01-15T12:00:05Z"
    result = record(document, "execution_result")
    result["status"] = "succeeded"
    result["started_at"] = "2026-01-15T12:00:06Z"
    result["completed_at"] = "2026-01-15T12:00:06Z"
    assert any("starts after approval expiry" in error for error in cross_errors(document))


def test_cross_validator_rejects_timestamp_reordering():
    document = fixture()
    record(document, "policy_decision")["occurred_at"] = "2026-01-15T11:59:59Z"
    assert any("monotonically nondecreasing" in error for error in cross_errors(document))


def test_cross_validator_rejects_action_digest_substitution():
    document = fixture()
    record(document, "proposed_action")["arguments"]["workspace_id"] = "workspace-other"
    assert any("action_digest must be" in error for error in cross_errors(document))


def test_cross_validator_rejects_execution_after_deny():
    document = fixture()
    request = record(document, "request")
    request["constraints"]["dry_run"] = False
    decision = record(document, "policy_decision")
    decision["decision"] = "deny"
    decision["authorization_basis"] = "none"
    result = record(document, "execution_result")
    result["status"] = "succeeded"
    result["started_at"] = "2026-01-15T12:00:05Z"
    result["completed_at"] = "2026-01-15T12:00:06Z"
    assert any("must be not_executed after deny" in error for error in cross_errors(document))


def test_cross_validator_rejects_not_required_when_approval_is_required():
    document = fixture()
    approval = record(document, "approval")
    approval["status"] = "not_required"
    approval["expires_at"] = None
    approval["approved_scope"] = None
    record(document, "policy_decision")["authorization_basis"] = "not_required"
    assert any("cannot be not_required" in error for error in cross_errors(document))


def test_cross_validator_rejects_execution_after_referral():
    document = fixture()
    record(document, "request")["constraints"]["dry_run"] = False
    decision = record(document, "policy_decision")
    decision["decision"] = "refer_to_human"
    decision["authorization_basis"] = "none"
    result = record(document, "execution_result")
    result["status"] = "succeeded"
    result["started_at"] = "2026-01-15T12:00:05Z"
    result["completed_at"] = "2026-01-15T12:00:06Z"
    assert any("must be not_executed after deny or referral" in error for error in cross_errors(document))


def test_cross_validator_rejects_duplicate_plan_step_ids():
    document = fixture()
    plan = record(document, "plan")
    duplicate = copy.deepcopy(plan["steps"][0])
    duplicate["order"] = 2
    plan["steps"].append(duplicate)
    assert any("plan step_id values must be unique" in error for error in cross_errors(document))
