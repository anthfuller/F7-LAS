#!/usr/bin/env python3
"""Validate F7-LAS canonical records and their cross-record relationships."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

import rfc8785
from jsonschema import Draft202012Validator, FormatChecker


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "schemas" / "contracts" / "f7las-records-v1.schema.json"
EXAMPLES_DIR = REPO_ROOT / "schemas" / "contracts" / "examples"
POLICY_DIR = REPO_ROOT / "config" / "policies"

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

FORBIDDEN_KEYS = {
    "api_key",
    "chain_of_thought",
    "password",
    "private_reasoning",
    "reasoning_trace",
    "secret",
    "token",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


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


def load_policy_registry() -> dict[str, dict[str, Any]]:
    registry: dict[str, dict[str, Any]] = {}
    for path in sorted(POLICY_DIR.glob("*.json")):
        if path.name == "policy-schema.json":
            continue
        policy = load_json(path)
        registry[policy["policy_id"]] = {
            "version": policy["version"],
            "policy_digest": digest_payload("policy", policy),
        }
    return registry


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def iter_keys(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for key, nested in value.items():
            yield key
            yield from iter_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from iter_keys(nested)


def validate_reference(
    reference: dict[str, str],
    expected: dict[str, Any],
    label: str,
    errors: list[str],
) -> None:
    if reference["record_id"] != expected["record_id"]:
        errors.append(f"{label}.record_id does not match {expected['record_type']}")
    if reference["record_digest"] != expected["record_digest"]:
        errors.append(f"{label}.record_digest does not match {expected['record_type']}")


def validate_record_set(
    document: dict[str, Any],
    validator: Draft202012Validator,
) -> list[str]:
    errors: list[str] = []
    records = document.get("records")
    if document.get("contract_set_version") != "1.0.0":
        errors.append("contract_set_version must be 1.0.0")
    if not isinstance(records, list):
        return errors + ["records must be an array"]

    for index, record in enumerate(records):
        for error in validator.iter_errors(record):
            location = ".".join(str(part) for part in error.absolute_path) or "<record>"
            errors.append(f"record[{index}] {location}: {error.message}")

    if errors:
        return errors

    counts = Counter(record["record_type"] for record in records)
    for record_type in ("request", "context", "plan"):
        if counts[record_type] != 1:
            errors.append(f"workflow must contain exactly one {record_type} record")
    if counts["proposed_action"] < 1:
        errors.append("workflow must contain at least one proposed_action record")
    if errors:
        return errors

    ids = [record["record_id"] for record in records]
    if len(ids) != len(set(ids)):
        errors.append("record_id values must be unique")

    workflow_ids = {record["workflow_id"] for record in records}
    if len(workflow_ids) != 1:
        errors.append("all records must share one workflow_id")

    sequences = [record["sequence"] for record in records]
    if sequences != list(range(1, len(records) + 1)):
        errors.append("sequence values must be contiguous, ordered, and start at 1")

    timestamps = [parse_timestamp(record["occurred_at"]) for record in records]
    if timestamps != sorted(timestamps):
        errors.append("occurred_at values must be monotonically nondecreasing")

    by_id = {record["record_id"]: record for record in records}
    index_by_id = {record["record_id"]: index for index, record in enumerate(records)}

    for index, record in enumerate(records):
        for key in (
            "request_ref",
            "context_ref",
            "plan_ref",
            "action_ref",
            "approval_ref",
            "decision_ref",
            "object_ref",
        ):
            reference = record.get(key)
            if reference is None:
                continue
            referenced_id = reference["record_id"]
            if referenced_id not in by_id:
                errors.append(f"{record['record_id']}.{key} references an unknown record")
            elif index_by_id[referenced_id] >= index:
                errors.append(f"{record['record_id']}.{key} must reference an earlier record")

    previous_digest: str | None = None
    for record in records:
        if record["previous_record_digest"] != previous_digest:
            errors.append(f"{record['record_id']}.previous_record_digest breaks the record chain")
        expected_digest = calculate_record_digest(record)
        if record["record_digest"] != expected_digest:
            errors.append(f"{record['record_id']}.record_digest must be {expected_digest}")
        previous_digest = record["record_digest"]

    forbidden = sorted({key for record in records for key in iter_keys(record)} & FORBIDDEN_KEYS)
    if forbidden:
        errors.append(f"forbidden sensitive/private-reasoning keys present: {forbidden}")

    request = next(record for record in records if record["record_type"] == "request")
    context = next(record for record in records if record["record_type"] == "context")
    plan = next(record for record in records if record["record_type"] == "plan")
    actions = [record for record in records if record["record_type"] == "proposed_action"]
    approvals = [record for record in records if record["record_type"] == "approval"]
    decisions = [record for record in records if record["record_type"] == "policy_decision"]
    results = [record for record in records if record["record_type"] == "execution_result"]
    audits = [record for record in records if record["record_type"] == "audit_event"]
    policy_registry = load_policy_registry()

    validate_reference(context["request_ref"], request, "context.request_ref", errors)
    validate_reference(plan["request_ref"], request, "plan.request_ref", errors)
    validate_reference(plan["context_ref"], context, "plan.context_ref", errors)

    if context["target"] != request["scope"]:
        errors.append("context target must exactly equal request scope")
    for evidence in context["evidence"]:
        if parse_timestamp(evidence["retrieved_at"]) > parse_timestamp(context["occurred_at"]):
            errors.append(f"{evidence['evidence_id']} is retrieved after the context record")

    request_limits = request["constraints"]
    for field in ("max_steps", "max_actions", "max_duration_seconds"):
        if plan["limits"][field] > request_limits[field]:
            errors.append(f"plan.limits.{field} exceeds the request constraint")
    if len(plan["steps"]) > plan["limits"]["max_steps"]:
        errors.append("plan contains more steps than max_steps")
    step_orders = [step["order"] for step in plan["steps"]]
    if step_orders != list(range(1, len(plan["steps"]) + 1)):
        errors.append("plan step order must be contiguous and start at 1")
    step_ids = {step["step_id"] for step in plan["steps"]}

    if len(actions) > min(request_limits["max_actions"], plan["limits"]["max_actions"]):
        errors.append("proposed-action count exceeds the request or plan limit")

    def records_for_action(collection: list[dict[str, Any]], action_id: str) -> list[dict[str, Any]]:
        return [record for record in collection if record["action_ref"]["record_id"] == action_id]

    for action in actions:
        validate_reference(action["request_ref"], request, f"{action['record_id']}.request_ref", errors)
        validate_reference(action["context_ref"], context, f"{action['record_id']}.context_ref", errors)
        validate_reference(action["plan_ref"], plan, f"{action['record_id']}.plan_ref", errors)
        if action["step_id"] not in step_ids:
            errors.append(f"{action['record_id']}.step_id is not present in the plan")
        if action["actor_id"] != context["actor"]["subject_id"]:
            errors.append(f"{action['record_id']}.actor_id does not match the context actor")
        if action["target"] != request["scope"]:
            errors.append(f"{action['record_id']}.target must exactly equal request scope")
        expected_action_digest = calculate_action_digest(action)
        if action["action_digest"] != expected_action_digest:
            errors.append(f"{action['record_id']}.action_digest must be {expected_action_digest}")

        action_approvals = records_for_action(approvals, action["record_id"])
        action_decisions = records_for_action(decisions, action["record_id"])
        action_results = records_for_action(results, action["record_id"])
        for label, related in (
            ("approval", action_approvals),
            ("policy_decision", action_decisions),
            ("execution_result", action_results),
        ):
            if len(related) != 1:
                errors.append(f"{action['record_id']} must have exactly one {label} record")
        if not all(len(related) == 1 for related in (action_approvals, action_decisions, action_results)):
            continue

        approval, decision, result = action_approvals[0], action_decisions[0], action_results[0]
        validate_reference(approval["request_ref"], request, f"{approval['record_id']}.request_ref", errors)
        validate_reference(decision["request_ref"], request, f"{decision['record_id']}.request_ref", errors)
        validate_reference(result["request_ref"], request, f"{result['record_id']}.request_ref", errors)

        for record in (approval, decision, result):
            action_ref = record["action_ref"]
            validate_reference(action_ref, action, f"{record['record_id']}.action_ref", errors)
            if action_ref["action_digest"] != action["action_digest"]:
                errors.append(f"{record['record_id']}.action_ref.action_digest does not match the action")

        validate_reference(decision["approval_ref"], approval, f"{decision['record_id']}.approval_ref", errors)
        validate_reference(result["decision_ref"], decision, f"{result['record_id']}.decision_ref", errors)

        if approval["policy_ref"] != decision["policy_ref"]:
            errors.append(f"{decision['record_id']}.policy_ref must exactly equal the approval policy_ref")
        policy_ref = approval["policy_ref"]
        registered_policy = policy_registry.get(policy_ref["policy_id"])
        if registered_policy is None:
            errors.append(f"{approval['record_id']}.policy_ref references an unknown policy")
        elif (
            policy_ref["version"] != registered_policy["version"]
            or policy_ref["policy_digest"] != registered_policy["policy_digest"]
        ):
            errors.append(f"{approval['record_id']}.policy_ref does not match the repository policy")
        if approval["issued_at"] != approval["occurred_at"]:
            errors.append(f"{approval['record_id']}.issued_at must equal occurred_at")

        approval_time = parse_timestamp(approval["issued_at"])
        decision_time = parse_timestamp(decision["occurred_at"])
        if decision_time < approval_time:
            errors.append(f"{decision['record_id']} occurs before its approval disposition")

        if approval["status"] == "approved":
            if approval["approved_scope"] != action["target"]:
                errors.append(f"{approval['record_id']}.approved_scope must exactly equal action target")
            if decision_time > parse_timestamp(approval["expires_at"]):
                errors.append(f"{decision['record_id']} occurs after approval expiry")
        if action["requires_approval"] and approval["status"] != "approved":
            errors.append(f"{action['record_id']} requires an approved approval record")
        if approval["status"] == "not_required" and action["requires_approval"]:
            errors.append(f"{approval['record_id']} cannot be not_required for this action")

        if decision["decision"] == "permit":
            valid_basis = (
                approval["status"] == "approved"
                or (approval["status"] == "not_required" and not action["requires_approval"])
            )
            if not valid_basis or decision["authorization_basis"] != approval["status"]:
                errors.append(f"{decision['record_id']} permit lacks a valid approval basis")
        elif result["status"] != "not_executed":
            errors.append(f"{result['record_id']} must be not_executed after deny or referral")

        if request_limits["dry_run"] and result["status"] != "not_executed":
            errors.append(f"{result['record_id']} must be not_executed for a dry-run request")
        if result["status"] == "succeeded" and decision["decision"] != "permit":
            errors.append(f"{result['record_id']} succeeded without a permit decision")
        if result["output_digest"] != calculate_output_digest(result["output"]):
            errors.append(f"{result['record_id']}.output_digest does not match output")
        if decision["obligations"] != sorted(decision["obligations"]):
            errors.append(f"{decision['record_id']}.obligations must be sorted")

        if result["started_at"] is not None:
            start = parse_timestamp(result["started_at"])
            complete = parse_timestamp(result["completed_at"])
            if start < decision_time:
                errors.append(f"{result['record_id']} starts before the policy decision")
            if complete < start:
                errors.append(f"{result['record_id']} completes before it starts")
            if parse_timestamp(result["occurred_at"]) < complete:
                errors.append(f"{result['record_id']} is recorded before completion")

    for related in approvals + decisions + results:
        if related["action_ref"]["record_id"] not in {action["record_id"] for action in actions}:
            errors.append(f"{related['record_id']} references an unknown proposed action")

    outcome_for_status = {
        "succeeded": "success",
        "failed": "failure",
        "not_executed": "not_executed",
    }
    for audit in audits:
        validate_reference(audit["request_ref"], request, f"{audit['record_id']}.request_ref", errors)
        object_id = audit["object_ref"]["record_id"]
        if object_id not in by_id:
            errors.append(f"{audit['record_id']}.object_ref references an unknown record")
            continue
        validate_reference(audit["object_ref"], by_id[object_id], f"{audit['record_id']}.object_ref", errors)
        source_ids: set[str] = set()
        source_sequences: list[int] = []
        for source in audit["source_records"]:
            source_id = source["record_id"]
            source_ids.add(source_id)
            if source_id not in by_id:
                errors.append(f"{audit['record_id']} references unknown source record {source_id}")
                continue
            expected = by_id[source_id]
            source_sequences.append(expected["sequence"])
            if source["record_type"] != expected["record_type"] or source["record_digest"] != expected["record_digest"]:
                errors.append(f"{audit['record_id']} source record {source_id} does not match")
            if index_by_id[source_id] >= index_by_id[audit["record_id"]]:
                errors.append(f"{audit['record_id']} source record {source_id} is not earlier")
        if source_sequences != sorted(source_sequences):
            errors.append(f"{audit['record_id']}.source_records must follow workflow sequence")
        sourced_results = [result for result in results if result["record_id"] in source_ids]
        if len(sourced_results) == 1:
            result = sourced_results[0]
            expected_outcome = outcome_for_status[result["status"]]
            related_decision = by_id[result["decision_ref"]["record_id"]]
            if result["status"] == "not_executed" and related_decision["decision"] == "deny":
                expected_outcome = "denied"
            if audit["outcome"] != expected_outcome:
                errors.append(f"{audit['record_id']}.outcome is inconsistent with its execution result")

    scopes = [request["scope"], context["target"]]
    scopes.extend(action["target"] for action in actions)
    scopes.extend(
        approval["approved_scope"]
        for approval in approvals
        if approval["approved_scope"] is not None
    )
    for scope in scopes:
        if scope["resource_ids"] != sorted(scope["resource_ids"]):
            errors.append(f"{scope['scope_id']}.resource_ids must be sorted")

    return errors


def validate_all() -> list[str]:
    schema = load_json(SCHEMA_PATH)
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # pragma: no cover
        return [f"invalid schema: {exc}"]

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    paths = sorted(EXAMPLES_DIR.glob("*.json"))
    if not paths:
        return [f"no contract examples found in {EXAMPLES_DIR}"]

    errors: list[str] = []
    for path in paths:
        try:
            document = load_json(path)
            errors.extend(
                f"{path.relative_to(REPO_ROOT)}: {error}"
                for error in validate_record_set(document, validator)
            )
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError, rfc8785.CanonicalizationError) as exc:
            errors.append(f"{path.relative_to(REPO_ROOT)}: {exc}")
    return errors


def main() -> int:
    errors = validate_all()
    if errors:
        print("F7-LAS contract validation FAILED:", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1
    print("F7-LAS contract validation PASSED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
