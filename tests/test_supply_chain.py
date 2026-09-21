from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-supply-chain.py"
SPEC = importlib.util.spec_from_file_location("validate_supply_chain", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_repository_supply_chain_invariants() -> None:
    MODULE.validate_repository(ROOT)


def test_workflow_requires_release_tag_validation() -> None:
    path = ROOT / ".github" / "workflows" / "f7las-ci.yml"
    text = path.read_text(encoding="utf-8")
    workflow = yaml.safe_load(text)
    workflow["on"]["push"].pop("tags")

    with pytest.raises(MODULE.SupplyChainError, match="version tags"):
        MODULE.validate_workflow(workflow, text)


def test_workflow_requires_release_readiness_validators() -> None:
    path = ROOT / ".github" / "workflows" / "f7las-ci.yml"
    text = path.read_text(encoding="utf-8")
    workflow = yaml.safe_load(text)
    modified = text.replace("python scripts/validate-citation.py", "echo skipped-citation")

    with pytest.raises(MODULE.SupplyChainError, match="validate-citation"):
        MODULE.validate_workflow(workflow, modified)


def test_tag_only_docker_action_is_rejected() -> None:
    with pytest.raises(MODULE.SupplyChainError, match="exact SHA-256 image digest"):
        MODULE.validate_docker_reference("docker://citationcff/cffconvert:2.0.0")


def test_malformed_docker_digest_is_rejected() -> None:
    with pytest.raises(MODULE.SupplyChainError, match="exact SHA-256 image digest"):
        MODULE.validate_docker_reference("docker://citationcff/cffconvert@sha256:1234")


def test_exact_docker_digest_is_accepted() -> None:
    MODULE.validate_docker_reference(
        "docker://citationcff/cffconvert@sha256:"
        "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
    )


def test_cff_action_wrapper_is_rejected() -> None:
    workflow = {"permissions": {"contents": "read"}, "jobs": {"validate": {}}}
    with pytest.raises(MODULE.SupplyChainError, match="mutable tag-only container"):
        MODULE.validate_workflow(
            workflow,
            "uses: citation-file-format/cffconvert-github-action@"
            "4cf11baa70a673bfdf9dad0acc7ee33b3f4b6084",
        )


def test_modified_cff_schema_artifact_is_rejected(tmp_path) -> None:
    target = tmp_path / MODULE.CFF_SCHEMA_PATH
    target.parent.mkdir(parents=True)
    target.write_bytes((ROOT / MODULE.CFF_SCHEMA_PATH).read_bytes() + b"\n")

    with pytest.raises(MODULE.SupplyChainError, match="schema digest mismatch"):
        MODULE.validate_cff_schema_artifact(tmp_path)


def test_unpinned_requirement_is_rejected() -> None:
    with pytest.raises(MODULE.SupplyChainError, match="not exactly pinned"):
        MODULE.validate_pinned_requirements("requests>=2.34", require_hashes=False)


def test_unhashed_lock_entry_is_rejected() -> None:
    with pytest.raises(MODULE.SupplyChainError, match="no SHA-256 hash"):
        MODULE.validate_pinned_requirements("requests==2.34.2", require_hashes=True)


def test_mutable_action_reference_is_rejected() -> None:
    workflow = yaml.safe_load(
        """
permissions:
  contents: read
jobs:
  validate:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v7
"""
    )
    with pytest.raises(MODULE.SupplyChainError, match="not pinned to a full SHA"):
        MODULE.validate_workflow(workflow, yaml.safe_dump(workflow))


def test_checkout_credentials_must_not_persist() -> None:
    workflow = yaml.safe_load(
        """
permissions:
  contents: read
jobs:
  validate:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
        with:
          fetch-depth: 0
          persist-credentials: true
"""
    )
    with pytest.raises(MODULE.SupplyChainError, match="disable persisted credentials"):
        MODULE.validate_workflow(workflow, yaml.safe_dump(workflow))


def test_unverified_download_is_rejected() -> None:
    workflow = yaml.safe_load(
        """
permissions:
  contents: read
jobs:
  validate:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
        with:
          fetch-depth: 0
          persist-credentials: false
      - uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97
        with:
          python-version: 3.12.14
      - name: Unsafe download
        run: curl -fsSLo tool https://example.invalid/tool
"""
    )
    with pytest.raises(MODULE.SupplyChainError, match="lacks SHA-256 verification"):
        MODULE.validate_workflow(workflow, yaml.safe_dump(workflow))


def test_write_capable_workflow_permissions_are_rejected() -> None:
    workflow = {"permissions": {"contents": "write"}, "jobs": {"validate": {}}}
    with pytest.raises(MODULE.SupplyChainError, match="exactly contents: read"):
        MODULE.validate_workflow(workflow, yaml.safe_dump(workflow))


def test_malformed_tool_digest_is_rejected() -> None:
    workflow = yaml.safe_load(
        """
permissions:
  contents: read
jobs:
  validate:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
        with:
          fetch-depth: 0
          persist-credentials: false
      - uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97
        with:
          python-version: 3.12.14
      - name: Invalid digest
        env:
          TOOL_SHA256: not-a-digest
        run: echo no-download
"""
    )
    with pytest.raises(MODULE.SupplyChainError, match="lowercase 64-character SHA-256"):
        MODULE.validate_workflow(workflow, yaml.safe_dump(workflow))
