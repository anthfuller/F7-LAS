from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-documentation.py"
SPEC = importlib.util.spec_from_file_location("validate_documentation", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_repository_documentation_is_consistent() -> None:
    MODULE.validate_repository(ROOT)


def test_local_virtual_environment_is_not_documentation(tmp_path: Path) -> None:
    ignored = tmp_path / ".venv" / "dependency" / "README.md"
    ignored.parent.mkdir(parents=True)
    ignored.write_text("```bash\necho not-repository-docs\n```\n", encoding="utf-8")
    assert MODULE.markdown_files(tmp_path) == []


def test_unresolved_relative_link_is_rejected(tmp_path: Path) -> None:
    document = tmp_path / "README.md"
    document.write_text("[missing](missing.md)\n", encoding="utf-8")
    with pytest.raises(MODULE.DocumentationError, match="unresolved relative link"):
        MODULE.validate_links(document, tmp_path)


def test_unclosed_fence_is_rejected(tmp_path: Path) -> None:
    document = tmp_path / "README.md"
    document.write_text("```bash\npython -m pytest -q\n", encoding="utf-8")
    with pytest.raises(MODULE.DocumentationError, match="unclosed Markdown fence"):
        MODULE.shell_blocks(document, tmp_path)


def test_shell_commands_in_illustrative_doc_are_rejected(tmp_path: Path) -> None:
    document = tmp_path / "illustrative.md"
    document.write_text("```bash\necho unsupported\n```\n", encoding="utf-8")
    with pytest.raises(MODULE.DocumentationError, match="outside supported"):
        MODULE.validate_command_boundaries(document, tmp_path)


def test_bare_pytest_command_is_rejected(tmp_path: Path) -> None:
    document = tmp_path / "README.md"
    document.write_text("```bash\npytest -q\n```\n", encoding="utf-8")
    with pytest.raises(MODULE.DocumentationError, match="python -m pytest"):
        MODULE.validate_command_boundaries(document, tmp_path)


def test_clean_user_gate_rejects_substituted_opa(tmp_path: Path) -> None:
    fake_opa = tmp_path / "opa"
    fake_opa.write_text("#!/bin/sh\necho 'Version: 1.20.2'\n", encoding="utf-8")
    fake_opa.chmod(0o755)
    result = subprocess.run(
        [str(ROOT / "scripts" / "run-clean-user-acceptance.sh")],
        cwd=ROOT,
        env={
            **os.environ,
            "OPA_BIN": str(fake_opa),
            "PYTHON_BIN": sys.executable,
        },
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert "OPA binary digest does not match" in result.stderr
