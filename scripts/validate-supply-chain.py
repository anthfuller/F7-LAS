#!/usr/bin/env python3
"""Validate repository-local supply-chain and CI invariants."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
PIN_RE = re.compile(r"^([A-Za-z0-9_.-]+)==([^\s;\\]+)")
HASH_RE = re.compile(r"--hash=sha256:[0-9a-f]{64}(?:\s|$)")
ACTION_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_./-]+)?@[0-9a-f]{40}$")
DOCKER_DIGEST_RE = re.compile(r"^docker://[^@\s]+@sha256:[0-9a-f]{64}$")
VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
CFF_SCHEMA_PATH = Path("schemas/cff/cff-1.2.0.schema.json")
CFF_SCHEMA_SHA256 = "0b8d22140da702d766df318dcff3a91af2f39521298dcf36d76315fd99cc169b"


class SupplyChainError(ValueError):
    """Raised when a supply-chain invariant is not satisfied."""


def _normalized_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def _logical_requirements(text: str) -> list[str]:
    logical: list[str] = []
    pending = ""
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        continuation = line.endswith("\\")
        fragment = line[:-1].strip() if continuation else line
        pending = f"{pending} {fragment}".strip()
        if not continuation:
            logical.append(pending)
            pending = ""
    if pending:
        raise SupplyChainError("unterminated requirement continuation")
    return logical


def validate_pinned_requirements(text: str, *, require_hashes: bool) -> dict[str, str]:
    """Return normalized package pins or raise for mutable/incomplete entries."""

    pins: dict[str, str] = {}
    for entry in _logical_requirements(text):
        if entry.startswith(("-r ", "--requirement ")):
            continue
        match = PIN_RE.match(entry)
        if not match:
            raise SupplyChainError(f"requirement is not exactly pinned: {entry}")
        name, version = match.groups()
        normalized = _normalized_name(name)
        if normalized in pins:
            raise SupplyChainError(f"duplicate requirement: {normalized}")
        if require_hashes and not HASH_RE.search(entry):
            raise SupplyChainError(f"requirement has no SHA-256 hash: {normalized}")
        pins[normalized] = version
    if not pins:
        raise SupplyChainError("no pinned requirements found")
    return pins


def validate_workflow(data: dict[str, Any], raw_text: str) -> None:
    """Validate immutable actions, least privilege, and verified downloads."""

    if "pull_request_target" in raw_text:
        raise SupplyChainError("pull_request_target is not allowed")
    if "citation-file-format/cffconvert-github-action@" in raw_text:
        raise SupplyChainError("CFF Action wrapper hides a mutable tag-only container")
    if data.get("permissions") != {"contents": "read"}:
        raise SupplyChainError("workflow permissions must be exactly contents: read")
    jobs = data.get("jobs")
    if not isinstance(jobs, dict) or not jobs:
        raise SupplyChainError("workflow has no jobs")

    checkout_found = False
    python_found = False
    for job in jobs.values():
        if job.get("runs-on") == "ubuntu-latest":
            raise SupplyChainError("runner image must not use ubuntu-latest")
        steps = job.get("steps", [])
        for step in steps:
            action = step.get("uses")
            if action and not str(action).startswith("./"):
                action_ref = str(action)
                if action_ref.startswith("docker://"):
                    validate_docker_reference(action_ref)
                elif not ACTION_RE.fullmatch(action_ref):
                    raise SupplyChainError(
                        f"external action is not pinned to a full SHA: {action_ref}"
                    )
                if action_ref.startswith("actions/checkout@"):
                    checkout_found = True
                    options = step.get("with", {})
                    if options.get("fetch-depth") != 0:
                        raise SupplyChainError(
                            "checkout must fetch full history for secret scanning"
                        )
                    if options.get("persist-credentials") is not False:
                        raise SupplyChainError("checkout must disable persisted credentials")
                if action_ref.startswith("actions/setup-python@"):
                    python_found = True
                    version = str(step.get("with", {}).get("python-version", ""))
                    if not VERSION_RE.fullmatch(version):
                        raise SupplyChainError("Python must be pinned to an exact patch version")

            run = str(step.get("run", ""))
            if "curl " in run and "sha256sum -c -" not in run:
                raise SupplyChainError(
                    f"download step lacks SHA-256 verification: {step.get('name')}"
                )

            env = step.get("env", {})
            for key, value in env.items():
                if str(key).endswith("_SHA256") and not SHA256_RE.fullmatch(str(value)):
                    raise SupplyChainError(f"{key} must be a lowercase 64-character SHA-256")

    if not checkout_found:
        raise SupplyChainError("pinned actions/checkout step not found")
    if not python_found:
        raise SupplyChainError("pinned actions/setup-python step not found")
    for required_command in (
        "python scripts/validate-citation.py",
        "python scripts/validate-control-traceability.py",
    ):
        if required_command not in raw_text:
            raise SupplyChainError(f"workflow is missing required validation: {required_command}")

    push = data.get("on", {}).get("push", {})
    if push.get("tags") != ["v*"]:
        raise SupplyChainError("workflow must validate version tags matching v*")


def validate_docker_reference(reference: str) -> None:
    if not DOCKER_DIGEST_RE.fullmatch(reference):
        raise SupplyChainError(
            f"Docker action must use an exact SHA-256 image digest: {reference}"
        )


def validate_cff_schema_artifact(root: Path = ROOT) -> None:
    path = root / CFF_SCHEMA_PATH
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != CFF_SCHEMA_SHA256:
        raise SupplyChainError(
            f"official CFF schema digest mismatch: expected {CFF_SCHEMA_SHA256}, found {actual}"
        )


def validate_dependabot(data: dict[str, Any]) -> None:
    updates = data.get("updates", [])
    ecosystems = {entry.get("package-ecosystem") for entry in updates}
    if ecosystems != {"pip", "github-actions"}:
        raise SupplyChainError("Dependabot must cover exactly pip and github-actions")
    for entry in updates:
        if entry.get("directory") != "/":
            raise SupplyChainError("Dependabot updates must target the repository root")
        if entry.get("schedule", {}).get("interval") != "weekly":
            raise SupplyChainError("Dependabot updates must run weekly")


def validate_repository(root: Path = ROOT) -> None:
    validate_cff_schema_artifact(root)
    requirements = validate_pinned_requirements(
        (root / "requirements.txt").read_text(encoding="utf-8"),
        require_hashes=False,
    )
    ci_input = validate_pinned_requirements(
        (root / "requirements-ci.in").read_text(encoding="utf-8"),
        require_hashes=False,
    )
    if ci_input.get("pip-audit") is None:
        raise SupplyChainError("requirements-ci.in must pin pip-audit")

    lock = validate_pinned_requirements(
        (root / "requirements-ci.lock").read_text(encoding="utf-8"),
        require_hashes=True,
    )
    for name, version in {**requirements, **ci_input}.items():
        if lock.get(name) != version:
            raise SupplyChainError(
                f"lock mismatch for {name}: expected {version}, found {lock.get(name)}"
            )

    workflow_path = root / ".github" / "workflows" / "f7las-ci.yml"
    workflow_text = workflow_path.read_text(encoding="utf-8")
    validate_workflow(yaml.safe_load(workflow_text), workflow_text)

    dependabot_text = (root / ".github" / "dependabot.yml").read_text(encoding="utf-8")
    validate_dependabot(yaml.safe_load(dependabot_text))


def main() -> int:
    try:
        validate_repository()
    except (OSError, SupplyChainError, yaml.YAMLError) as exc:
        print(f"supply-chain validation failed: {exc}", file=sys.stderr)
        return 1
    print("Supply-chain and CI invariants validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
