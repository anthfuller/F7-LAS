"""One deterministic, offline, fail-closed F7-LAS Layers 1-7 path."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from .contracts import (
    calculate_action_digest,
    calculate_output_digest,
    calculate_record_digest,
    digest_payload,
)
from .opa import OfflineOPA


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_POLICY_PATH = REPO_ROOT / "config" / "policies" / "canonical-workflow.rego"
POLICY_DOCUMENT_PATH = REPO_ROOT / "config" / "policies" / "policy-constraints-default.json"
EXPECTED_MISSION = "Evaluate synthetic lab workspace health."
EXPECTED_REQUESTER = {
    "subject_id": "operator-0001",
    "subject_type": "human",
    "role": "soc-analyst",
}
EXPECTED_ACTOR = {
    "subject_id": "investigator-0001",
    "subject_type": "agent",
    "role": "investigator",
}


class WorkflowError(ValueError):
    """Input cannot enter the canonical workflow."""


def _timestamp(started_at: datetime, offset_seconds: int) -> str:
    return (started_at + timedelta(seconds=offset_seconds)).strftime("%Y-%m-%dT%H:%M:%SZ")


def _reference(record: dict[str, Any]) -> dict[str, str]:
    return {
        "record_id": record["record_id"],
        "record_digest": record["record_digest"],
    }


def _action_reference(record: dict[str, Any]) -> dict[str, str]:
    return {**_reference(record), "action_digest": record["action_digest"]}


class CanonicalWorkflow:
    """Execute a single synthetic read-only action and emit canonical evidence."""

    def __init__(self, opa_binary: str = "opa", policy_path: Path = DEFAULT_POLICY_PATH) -> None:
        self.opa = OfflineOPA(opa_binary, policy_path)

    @staticmethod
    def _validate_input(workflow_input: dict[str, Any]) -> datetime:
        required = {"workflow_id", "started_at", "mission", "requester", "actor", "scope"}
        if set(workflow_input) != required:
            raise WorkflowError("workflow input fields do not match the canonical interface")
        if workflow_input["workflow_id"] != "workflow-0001":
            raise WorkflowError("Milestone 3 accepts only workflow-0001")
        if workflow_input["mission"] != EXPECTED_MISSION:
            raise WorkflowError("mission is outside the canonical offline path")
        if workflow_input["requester"] != EXPECTED_REQUESTER:
            raise WorkflowError("requester is outside the canonical offline path")
        if workflow_input["actor"] != EXPECTED_ACTOR:
            raise WorkflowError("actor is outside the canonical offline path")
        scope = workflow_input["scope"]
        if scope != {
            "scope_id": "lab-boundary-0001",
            "environment": "lab",
            "resource_ids": ["workspace-0001"],
        }:
            raise WorkflowError("scope is outside the canonical lab boundary")
        try:
            started_at = datetime.strptime(workflow_input["started_at"], "%Y-%m-%dT%H:%M:%SZ")
        except (TypeError, ValueError) as exc:
            raise WorkflowError("started_at must be whole-second RFC 3339 UTC") from exc
        return started_at.replace(tzinfo=timezone.utc)

    @staticmethod
    def _policy_ref() -> dict[str, str]:
        with POLICY_DOCUMENT_PATH.open("r", encoding="utf-8") as handle:
            document = json.load(handle)
        return {
            "policy_id": document["policy_id"],
            "version": document["version"],
            "policy_digest": digest_payload("policy", document),
        }

    @staticmethod
    def _finalize(
        record: dict[str, Any],
        previous: dict[str, Any] | None,
    ) -> dict[str, Any]:
        record["previous_record_digest"] = None if previous is None else previous["record_digest"]
        record["record_digest"] = calculate_record_digest(record)
        return record

    @staticmethod
    def _execute(action: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
        if decision["decision"] != "permit":
            return {"status": "not_executed", "output": {"reason_code": decision["reason_code"]}}
        if (
            action["tool"] != {"tool_id": "siem-query", "version": "1.0.0"}
            or action["operation"] != "workspace-health"
            or action["target"]["environment"] != "lab"
        ):
            return {"status": "not_executed", "output": {"reason_code": "executor-scope-mismatch"}}
        return {
            "status": "succeeded",
            "output": {
                "environment": "lab",
                "resource_id": "workspace-0001",
                "status": "healthy",
                "synthetic": True,
            },
        }

    def run(self, workflow_input: dict[str, Any]) -> dict[str, Any]:
        started_at = self._validate_input(workflow_input)
        workflow_id = workflow_input["workflow_id"]
        scope = workflow_input["scope"]
        records: list[dict[str, Any]] = []

        def header(record_type: str, sequence: int) -> dict[str, Any]:
            return {
                "schema_version": "1.0.0",
                "record_type": record_type,
                "record_id": f"{record_type.replace('_', '-')}-0001",
                "workflow_id": workflow_id,
                "sequence": sequence,
                "occurred_at": _timestamp(started_at, sequence - 1),
            }

        request = self._finalize(
            {
                **header("request", 1),
                "mission": workflow_input["mission"],
                "requester": workflow_input["requester"],
                "scope": scope,
                "constraints": {
                    "max_steps": 1,
                    "max_actions": 1,
                    "max_duration_seconds": 30,
                    "dry_run": False,
                },
            },
            None,
        )
        records.append(request)

        evidence_value = {"workspace_id": "workspace-0001", "source": "synthetic-inventory"}
        context = self._finalize(
            {
                **header("context", 2),
                "request_ref": _reference(request),
                "actor": workflow_input["actor"],
                "target": scope,
                "evidence": [
                    {
                        "evidence_id": "evidence-0001",
                        "source_id": "synthetic-inventory",
                        "content_digest": digest_payload("evidence", evidence_value),
                        "retrieved_at": _timestamp(started_at, 1),
                        "trust_basis_points": 10000,
                    }
                ],
            },
            request,
        )
        records.append(context)

        plan = self._finalize(
            {
                **header("plan", 3),
                "request_ref": _reference(request),
                "context_ref": _reference(context),
                "planner_id": "deterministic-planner",
                "limits": {"max_steps": 1, "max_actions": 1, "max_duration_seconds": 30},
                "steps": [
                    {
                        "step_id": "step-0001",
                        "order": 1,
                        "summary": "Read synthetic workspace health.",
                    }
                ],
            },
            context,
        )
        records.append(plan)

        action = {
            **header("proposed_action", 4),
            "request_ref": _reference(request),
            "context_ref": _reference(context),
            "plan_ref": _reference(plan),
            "step_id": "step-0001",
            "actor_id": workflow_input["actor"]["subject_id"],
            "tool": {"tool_id": "siem-query", "version": "1.0.0"},
            "operation": "workspace-health",
            "arguments": {"workspace_id": "workspace-0001"},
            "target": scope,
            "risk_tier": "low",
            "requires_approval": False,
        }
        action["action_digest"] = calculate_action_digest(action)
        action = self._finalize(action, plan)
        records.append(action)

        policy_ref = self._policy_ref()
        approval = self._finalize(
            {
                **header("approval", 5),
                "request_ref": _reference(request),
                "action_ref": _action_reference(action),
                "status": "not_required",
                "authority": {
                    "subject_id": "canonical-workflow",
                    "subject_type": "service",
                    "role": "policy-enforcement-point",
                },
                "reason_code": "low-risk-read-only",
                "policy_ref": policy_ref,
                "issued_at": _timestamp(started_at, 4),
                "expires_at": None,
                "approved_scope": None,
            },
            action,
        )
        records.append(approval)

        opa_result = self.opa.evaluate(
            {
                "request": {
                    "dry_run": request["constraints"]["dry_run"],
                    "scope": request["scope"],
                },
                "actor": context["actor"],
                "action": {
                    "tool": action["tool"],
                    "operation": action["operation"],
                    "target": action["target"],
                    "risk_tier": action["risk_tier"],
                    "requires_approval": action["requires_approval"],
                },
                "approval_status": approval["status"],
                "policy_ref": policy_ref,
            }
        )
        decision_value = opa_result["decision"]
        decision = self._finalize(
            {
                **header("policy_decision", 6),
                "request_ref": _reference(request),
                "action_ref": _action_reference(action),
                "approval_ref": _reference(approval),
                "pdp_id": "opa-cli",
                "decision": decision_value,
                "authorization_basis": "not_required" if decision_value == "permit" else "none",
                "reason_code": opa_result["reason_code"],
                "policy_ref": policy_ref,
                "obligations": sorted(opa_result["obligations"]),
            },
            approval,
        )
        records.append(decision)

        execution = self._execute(action, decision)
        execution_status = execution["status"]
        was_executed = execution_status == "succeeded"
        result = self._finalize(
            {
                **header("execution_result", 7),
                "request_ref": _reference(request),
                "action_ref": _action_reference(action),
                "decision_ref": _reference(decision),
                "execution_environment": {
                    "sandbox_id": "offline-runtime",
                    "profile_id": "synthetic-no-network",
                    "profile_digest": digest_payload(
                        "sandbox-profile",
                        {"network": False, "registered_tools": ["siem-query:workspace-health"]},
                    ),
                },
                "status": execution_status,
                "started_at": _timestamp(started_at, 6) if was_executed else None,
                "completed_at": _timestamp(started_at, 6) if was_executed else None,
                "output": execution["output"],
                "output_digest": calculate_output_digest(execution["output"]),
                "error_code": None,
                "side_effects": [],
            },
            decision,
        )
        records.append(result)

        if was_executed:
            outcome = "success"
        elif decision["decision"] == "deny":
            outcome = "denied"
        else:
            outcome = "not_executed"
        audit = self._finalize(
            {
                **header("audit_event", 8),
                "request_ref": _reference(request),
                "event_type": "workflow-completed",
                "subject": workflow_input["actor"],
                "object_ref": _reference(action),
                "outcome": outcome,
                "source_records": [
                    {
                        "record_type": record["record_type"],
                        **_reference(record),
                    }
                    for record in records
                ],
                "details": {
                    "execution_status": execution_status,
                    "policy_reason_code": decision["reason_code"],
                    "synthetic": True,
                },
            },
            result,
        )
        records.append(audit)
        return {"contract_set_version": "1.0.0", "records": records}
