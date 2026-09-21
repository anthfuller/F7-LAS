import importlib.util
from pathlib import Path

import pytest


MODULE_PATH = Path("scripts/validate-citation.py")
SPEC = importlib.util.spec_from_file_location("validate_citation", MODULE_PATH)
assert SPEC and SPEC.loader
citation = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(citation)


def test_repository_citation_is_valid():
    citation.validate_citation()


def test_citation_rejects_year_only_release_date(tmp_path):
    path = tmp_path / "CITATION.cff"
    path.write_text(
        """cff-version: 1.2.0
message: Cite this work.
title: Test
authors:
  - family-names: Fuller
    given-names: Anthony
date-released: 2025
""",
        encoding="utf-8",
    )

    with pytest.raises(citation.CitationError, match="full YYYY-MM-DD"):
        citation.validate_citation(path)


def test_citation_rejects_duplicate_keys(tmp_path):
    path = tmp_path / "CITATION.cff"
    path.write_text(
        """cff-version: 1.2.0
message: Cite this work.
message: Conflicting message.
title: Test
authors:
  - family-names: Fuller
    given-names: Anthony
""",
        encoding="utf-8",
    )

    with pytest.raises(citation.CitationError, match="duplicate YAML mapping key"):
        citation.validate_citation(path)
