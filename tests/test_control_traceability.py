import importlib.util
import json
from pathlib import Path

import pytest


MODULE_PATH = Path("scripts/validate-control-traceability.py")
SPEC = importlib.util.spec_from_file_location("validate_control_traceability", MODULE_PATH)
assert SPEC and SPEC.loader
traceability = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(traceability)


def copy_fixture(tmp_path: Path) -> Path:
    (tmp_path / "config").mkdir()
    (tmp_path / "docs").mkdir()
    (tmp_path / "scripts").mkdir()
    (tmp_path / "tests").mkdir()
    catalog = Path("docs/F7-LAS-Control-Catalog-v0.1.md")
    target_catalog = tmp_path / catalog
    target_catalog.write_bytes(catalog.read_bytes())
    document = json.loads(Path("config/control-traceability.json").read_text(encoding="utf-8"))
    paths = {
        reference["path"]
        for control in document["controls"]
        for reference in control["evidence"]
    }
    for relative_text in paths:
        relative = Path(relative_text)
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(relative.read_bytes())
    (tmp_path / "config" / "control-traceability.json").write_text(
        json.dumps(document, indent=2) + "\n", encoding="utf-8"
    )
    return tmp_path


def load_fixture(root: Path) -> dict:
    return json.loads((root / "config" / "control-traceability.json").read_text())


def save_fixture(root: Path, document: dict) -> None:
    (root / "config" / "control-traceability.json").write_text(
        json.dumps(document, indent=2) + "\n", encoding="utf-8"
    )


def test_complete_traceability_matches_all_51_catalog_controls():
    counts = traceability.validate_traceability()

    assert counts == {"partial": 29, "not_implemented": 16, "implemented": 6}


def test_traceability_rejects_missing_control(tmp_path):
    root = copy_fixture(tmp_path)
    document = load_fixture(root)
    document["controls"].pop()
    save_fixture(root, document)

    with pytest.raises(traceability.TraceabilityError, match="catalog order and membership"):
        traceability.validate_traceability(root)


def test_traceability_rejects_missing_evidence_target(tmp_path):
    root = copy_fixture(tmp_path)
    document = load_fixture(root)
    document["controls"][0]["evidence"][0]["path"] = "missing-evidence.txt"
    save_fixture(root, document)

    with pytest.raises(traceability.TraceabilityError, match="evidence path does not exist"):
        traceability.validate_traceability(root)


def test_traceability_rejects_unverifiable_implemented_claim(tmp_path):
    root = copy_fixture(tmp_path)
    document = load_fixture(root)
    entry = next(item for item in document["controls"] if item["status"] == "implemented")
    entry["evidence"] = [
        {
            "kind": "documentation",
            "path": "docs/F7-LAS-Control-Catalog-v0.1.md",
            "locator": entry["control_id"],
        }
    ]
    save_fixture(root, document)

    with pytest.raises(traceability.TraceabilityError, match="lacks executable evidence"):
        traceability.validate_traceability(root)
