#!/usr/bin/env python3
"""Validate repository citation metadata against the required CFF 1.2 profile."""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import yaml


ROOT = Path(__file__).resolve().parents[1]
CITATION_PATH = ROOT / "CITATION.cff"
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")
SPDX_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.+-]*$")


class CitationError(ValueError):
    """Citation metadata violates the repository CFF profile."""


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that refuses duplicate mapping keys."""


def _construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False):
    result: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise CitationError(f"duplicate YAML mapping key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping,
)


def _nonempty_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CitationError(f"{field} must be a non-empty string")
    return value


def validate_citation(path: Path = CITATION_PATH) -> None:
    document = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    if not isinstance(document, dict):
        raise CitationError("CITATION.cff must contain a YAML mapping")
    for field in ("cff-version", "message", "title", "authors"):
        if field not in document:
            raise CitationError(f"required CFF field is missing: {field}")
    if document["cff-version"] != "1.2.0":
        raise CitationError("cff-version must be 1.2.0")
    _nonempty_string(document["message"], "message")
    _nonempty_string(document["title"], "title")

    authors = document["authors"]
    if not isinstance(authors, list) or not authors:
        raise CitationError("authors must be a non-empty array")
    for index, author in enumerate(authors):
        if not isinstance(author, dict):
            raise CitationError(f"authors[{index}] must be a mapping")
        if "name" in author:
            _nonempty_string(author["name"], f"authors[{index}].name")
        else:
            _nonempty_string(author.get("family-names"), f"authors[{index}].family-names")
            _nonempty_string(author.get("given-names"), f"authors[{index}].given-names")

    if "version" in document:
        _nonempty_string(document["version"], "version")
    if "doi" in document and not DOI_RE.fullmatch(_nonempty_string(document["doi"], "doi")):
        raise CitationError("doi is not syntactically valid")
    if "url" in document:
        parsed = urlsplit(_nonempty_string(document["url"], "url"))
        if parsed.scheme != "https" or not parsed.netloc:
            raise CitationError("url must be an absolute HTTPS URL")
    if "license" in document:
        licenses = document["license"]
        if isinstance(licenses, str):
            licenses = [licenses]
        if not isinstance(licenses, list) or not licenses:
            raise CitationError("license must be an SPDX identifier or non-empty array")
        if not all(isinstance(item, str) and SPDX_RE.fullmatch(item) for item in licenses):
            raise CitationError("license contains an invalid SPDX identifier")
    if "date-released" in document:
        released = document["date-released"]
        if not isinstance(released, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", released):
            raise CitationError("date-released must be a full YYYY-MM-DD string")
        try:
            date.fromisoformat(released)
        except ValueError as exc:
            raise CitationError("date-released is not a valid calendar date") from exc


def main() -> int:
    try:
        validate_citation()
    except (OSError, UnicodeError, yaml.YAMLError, CitationError) as exc:
        print(f"CFF validation failed: {exc}", file=sys.stderr)
        return 1
    print("CITATION.cff validation PASSED for CFF 1.2.0.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
