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
