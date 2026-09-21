#!/usr/bin/env python3
"""Validate complete F7-LAS control-to-evidence traceability."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "docs" / "F7-LAS-Control-Catalog-v0.1.md"
TRACEABILITY_PATH = ROOT / "config" / "control-traceability.json"
CONTROL_RE = re.compile(r"^###\s+(F7-(L[1-7]|LS)-\d{2})\s+[–-]\s+(.+?)\s*$", re.MULTILINE)
STATUSES = {"implemented", "partial", "not_implemented"}
EVIDENCE_KINDS = {
    "configuration",
    "documentation",
    "implementation",
    "release",
    "schema",
    "test",
    "workflow",
}
EXECUTABLE_EVIDENCE = {
    "configuration",
    "implementation",
    "schema",
    "test",
    "workflow",
}


class TraceabilityError(ValueError):
    """Traceability data does not match the catalog or repository."""


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise TraceabilityError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=_reject_duplicate_keys)


def catalog_controls(root: Path = ROOT) -> list[dict[str, str]]:
    text = (root / CATALOG_PATH.relative_to(ROOT)).read_text(encoding="utf-8")
    return [
        {"control_id": control_id, "domain": domain, "title": title}
        for control_id, domain, title in CONTROL_RE.findall(text)
    ]


def validate_traceability(root: Path = ROOT) -> dict[str, int]:
    traceability = _load_json(root / TRACEABILITY_PATH.relative_to(ROOT))
    if set(traceability) != {
        "schema_version",
        "catalog",
        "scope",
        "summary",
        "controls",
    }:
        raise TraceabilityError("traceability top-level fields do not match the contract")
    if traceability["schema_version"] != "1.0.0":
        raise TraceabilityError("schema_version must be 1.0.0")
    if traceability["catalog"] != {
        "path": "docs/F7-LAS-Control-Catalog-v0.1.md",
        "version": "0.1",
    }:
        raise TraceabilityError("catalog reference does not identify v0.1")
    if not isinstance(traceability["scope"], str) or len(traceability["scope"]) < 20:
        raise TraceabilityError("scope must state the assessment boundary")

    catalog = catalog_controls(root)
    if len(catalog) != 51:
        raise TraceabilityError(f"catalog must contain 51 controls; found {len(catalog)}")
    catalog_ids = [entry["control_id"] for entry in catalog]
    if len(catalog_ids) != len(set(catalog_ids)):
        raise TraceabilityError("catalog control identifiers are not unique")

    controls = traceability["controls"]
    if not isinstance(controls, list):
        raise TraceabilityError("controls must be an array")
    trace_ids = [entry.get("control_id") for entry in controls if isinstance(entry, dict)]
    if trace_ids != catalog_ids:
        missing = sorted(set(catalog_ids) - set(trace_ids))
        extra = sorted(set(trace_ids) - set(catalog_ids))
        raise TraceabilityError(
            f"traceability must match catalog order and membership; missing={missing} extra={extra}"
        )

    for expected, entry in zip(catalog, controls):
        if set(entry) != {
            "control_id",
            "domain",
            "title",
            "status",
            "limitations",
            "evidence",
        }:
            raise TraceabilityError(
                f"{expected['control_id']}: fields do not match the traceability contract"
            )
        for field in ("control_id", "domain", "title"):
            if entry[field] != expected[field]:
                raise TraceabilityError(
                    f"{expected['control_id']}: {field} does not match the catalog"
                )
        if entry["status"] not in STATUSES:
            raise TraceabilityError(f"{expected['control_id']}: invalid status")
        if not isinstance(entry["limitations"], str) or len(entry["limitations"]) < 20:
            raise TraceabilityError(f"{expected['control_id']}: limitations are incomplete")
        evidence = entry["evidence"]
        if not isinstance(evidence, list) or not evidence:
            raise TraceabilityError(f"{expected['control_id']}: evidence is required")
        kinds: set[str] = set()
        for reference in evidence:
            if set(reference) != {"kind", "path", "locator"}:
                raise TraceabilityError(
                    f"{expected['control_id']}: evidence fields do not match the contract"
                )
            kind = reference["kind"]
            if kind not in EVIDENCE_KINDS:
                raise TraceabilityError(f"{expected['control_id']}: invalid evidence kind")
            kinds.add(kind)
            relative = Path(reference["path"])
            if relative.is_absolute() or ".." in relative.parts:
                raise TraceabilityError(f"{expected['control_id']}: unsafe evidence path")
            path = root / relative
            if not path.is_file():
                raise TraceabilityError(
                    f"{expected['control_id']}: evidence path does not exist: {relative}"
                )
            locator = reference["locator"]
            if not isinstance(locator, str) or not locator:
                raise TraceabilityError(f"{expected['control_id']}: evidence locator is required")
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError as exc:
                raise TraceabilityError(
                    f"{expected['control_id']}: evidence path is not UTF-8 text: {relative}"
                ) from exc
            if locator not in content:
                raise TraceabilityError(
                    f"{expected['control_id']}: evidence locator not found in {relative}: {locator}"
                )
        if entry["status"] in {"implemented", "partial"} and not (
            kinds & EXECUTABLE_EVIDENCE
        ):
            raise TraceabilityError(
                f"{expected['control_id']}: {entry['status']} status lacks executable evidence"
            )

    counts = Counter(entry["status"] for entry in controls)
    expected_summary = {
        "total": 51,
        "core_layers_1_7": 46,
        "supplemental_layer_s": 5,
        "implemented": counts["implemented"],
        "partial": counts["partial"],
        "not_implemented": counts["not_implemented"],
    }
    if traceability["summary"] != expected_summary:
        raise TraceabilityError(
            f"summary does not match controls: expected {expected_summary}"
        )
    return dict(counts)


def main() -> int:
    try:
        counts = validate_traceability()
    except (OSError, json.JSONDecodeError, TypeError, TraceabilityError) as exc:
        print(f"control traceability validation failed: {exc}", file=sys.stderr)
        return 1
    print(
        "F7-LAS control traceability PASSED: "
        f"implemented={counts.get('implemented', 0)} "
        f"partial={counts.get('partial', 0)} "
        f"not_implemented={counts.get('not_implemented', 0)} total=51."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
