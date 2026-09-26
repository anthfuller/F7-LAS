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


def test_case_sensitive_relative_link_is_required(tmp_path: Path) -> None:
    (tmp_path / "Whitepaper.pdf").write_bytes(b"PDF")
    document = tmp_path / "README.md"
    document.write_text("[PDF](whitepaper.pdf)\n", encoding="utf-8")
    with pytest.raises(MODULE.DocumentationError, match="unresolved relative link|case-sensitive path mismatch"):
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


def test_substituted_canonical_diagram_is_rejected(tmp_path: Path) -> None:
    source = ROOT / "docs" / "images" / "F7-LAS-Executive-Control-Loop.png"
    substituted = tmp_path / source.name
    substituted.write_bytes(source.read_bytes() + b"substituted")
    with pytest.raises(MODULE.DocumentationError, match="diagram digest mismatch"):
        MODULE.validate_png(
            substituted,
            MODULE.EXPECTED_DIAGRAMS[
                Path("docs/images/F7-LAS-Executive-Control-Loop.png")
            ][0],
            (1920, 1080),
        )


def test_substituted_current_whitepaper_is_rejected(tmp_path: Path) -> None:
    substituted = tmp_path / MODULE.CURRENT_WHITEPAPER_PATH.name
    source = ROOT / MODULE.CURRENT_WHITEPAPER_PATH
    substituted.write_bytes(source.read_bytes() + b"substituted")
    with pytest.raises(MODULE.DocumentationError, match="whitepaper digest mismatch"):
        MODULE.validate_pdf_digest(
            substituted,
            MODULE.CURRENT_WHITEPAPER_SHA256,
            "current whitepaper",
        )


def test_whitepaper_checksum_manifest_is_exact() -> None:
    manifest = (ROOT / MODULE.CURRENT_WHITEPAPER_CHECKSUM_PATH).read_text(
        encoding="ascii"
    )
    assert manifest == (
        f"{MODULE.CURRENT_WHITEPAPER_SHA256}  "
        f"{MODULE.CURRENT_WHITEPAPER_PATH.name}\n"
    )


def test_whitepaper_repository_metadata_is_locked() -> None:
    assert MODULE.CURRENT_WHITEPAPER_PATH == Path(
        "docs/whitepaper/F7-LAS-Whitepaper-v4.1-Restored-Full-Edition.pdf"
    )
    assert MODULE.CURRENT_WHITEPAPER_SHA256 == (
        "95cf7f053f0fe021c9b0cc50f81a81afb33ba3dbdceae1cd7bbbeff407706456"
    )
    MODULE.validate_pdf_digest(
        ROOT / MODULE.HISTORICAL_V4_WHITEPAPER_PATH,
        MODULE.HISTORICAL_V4_WHITEPAPER_SHA256,
        "historical v4.0 whitepaper",
    )
    assert "doi:" not in (ROOT / "CITATION.cff").read_text(encoding="utf-8")


@pytest.mark.parametrize(
    "stale_assertion",
    [
        "Repository version 4.0.0 is an unpublished release candidate.",
        "Version 4.0.0 is not tagged or published.",
        "The whitepaper remains v3.0.",
    ],
)
def test_stale_current_status_assertions_are_rejected(
    stale_assertion: str,
) -> None:
    with pytest.raises(
        MODULE.DocumentationError, match="stale current-status assertion"
    ):
        MODULE.validate_no_stale_status(Path("README.md"), stale_assertion)


def test_docx_whitepaper_is_rejected(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    whitepaper = docs / "whitepaper"
    whitepaper.mkdir(parents=True)
    (whitepaper / MODULE.CURRENT_WHITEPAPER_PATH.name).write_bytes(
        (ROOT / MODULE.CURRENT_WHITEPAPER_PATH).read_bytes()
    )
    (docs / MODULE.HISTORICAL_WHITEPAPER_PATH.name).write_bytes(
        (ROOT / MODULE.HISTORICAL_WHITEPAPER_PATH).read_bytes()
    )
    (whitepaper / MODULE.HISTORICAL_V4_WHITEPAPER_PATH.name).write_bytes(
        (ROOT / MODULE.HISTORICAL_V4_WHITEPAPER_PATH).read_bytes()
    )
    (whitepaper / MODULE.CURRENT_WHITEPAPER_CHECKSUM_PATH.name).write_text(
        f"{MODULE.CURRENT_WHITEPAPER_SHA256}  "
        f"{MODULE.CURRENT_WHITEPAPER_PATH.name}\n",
        encoding="ascii",
    )
    (whitepaper / "F7-LAS-Whitepaper-v4.1.docx").write_bytes(b"not public")
    (tmp_path / "README.md").write_text(
        (ROOT / "README.md").read_text(encoding="utf-8"), encoding="utf-8"
    )
    (docs / "README.md").write_text(
        (ROOT / "docs" / "README.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    with pytest.raises(MODULE.DocumentationError, match="DOCX whitepaper"):
        MODULE.validate_whitepapers(tmp_path)


def test_control_loop_semantics_are_required() -> None:
    expected = {
        "returns to the PDP for reevaluation",
        "Only a PDP permit may proceed to PEP enforcement",
        "PEP authorization occurs before tool access or execution",
        "distinct terminal outcomes",
        "Agent Planning",
        "workflow compression",
        "six-stage runtime flow governed across all seven F7-LAS layers",
        "L7 Monitoring & Evaluation",
        "result validation, audit, telemetry, evidence, and assurance",
        "Layer 7 observes the complete lifecycle",
        "governed feedback produced from Layer 7 observations",
        "not an eighth layer",
    }
    assert expected <= MODULE.REQUIRED_DIAGRAM_NOTICES


def test_control_loop_accessible_alt_text_is_required() -> None:
    assert set(MODULE.REQUIRED_DIAGRAM_ALT_TEXT) == set(MODULE.EXPECTED_DIAGRAMS)
    assert all(
        "Layer 7" in alt_text
        for alt_text in MODULE.REQUIRED_DIAGRAM_ALT_TEXT.values()
    )


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
