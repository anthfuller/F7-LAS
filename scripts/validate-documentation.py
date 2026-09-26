#!/usr/bin/env python3
"""Validate repository Markdown links, fences, and runnable-command boundaries."""

from __future__ import annotations

import hashlib
import re
import struct
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^\s*```([^`]*)\s*$")
SHELL_LANGUAGES = {"bash", "sh", "shell", "console", "powershell", "cmd"}
RUNNABLE_COMMAND_DOCS = {
    Path("README.md"),
    Path("docs/clean-user-acceptance.md"),
    Path("docs/supply-chain-and-ci.md"),
    Path("examples/canonical-workflow/README.md"),
    Path("schemas/contracts/README.md"),
}
IGNORED_DIRECTORIES = {".git", ".venv", "venv", "node_modules", "__pycache__"}
EXPECTED_DIAGRAMS = {
    Path("docs/images/F7-LAS-Executive-Control-Loop.png"): (
        "0e250eff8f021973608a77df78f01b276ed8c1147f25d24e493f9d96bc8b38ff",
        (1920, 1080),
    ),
    Path("docs/images/F7-LAS-Agentic-Execution-Control-Loop.png"): (
        "777f4a5de48dcc98ea0332358c0d9272ca4ca13d12889143a3e42464d4e6187d",
        (1920, 1080),
    ),
}
REQUIRED_DIAGRAM_ALT_TEXT = {
    Path("docs/images/F7-LAS-Executive-Control-Loop.png"): (
        "F7-LAS executive control loop showing six numbered runtime stages "
        "governed across all seven layers, conditional human approval, PDP and "
        "PEP gates, scoped execution, lifecycle-wide Layer 7 monitoring and "
        "governed feedback"
    ),
    Path("docs/images/F7-LAS-Agentic-Execution-Control-Loop.png"): (
        "F7-LAS technical execution control loop showing all seven "
        "responsibility layers, permit-only PDP-to-PEP routing, Layer 4 tool "
        "access inside the Layer 6 boundary, lifecycle-wide Layer 7 monitoring "
        "and evaluation, and governed feedback"
    ),
}
RETIRED_DIAGRAMS = {
    Path("config/prompts/F7-LAS-Model-v1.png"),
    Path("docs/F7-LAS-Model-v1.png"),
    Path("docs/images/F7-LAS-Model-v1A.png"),
    Path("docs/images/F7-LAS-Model-v1B.png"),
    Path("docs/images/F7-LAS_Execution_Control_Loop.png"),
    Path("docs/images/Multi-Agent-F7-LAS_Model-v1.png"),
}
REQUIRED_DIAGRAM_NOTICES = {
    "Layer numbers name responsibility domains",
    "proposal has no authority to execute",
    "synthetic in-process executor—not an OS/container sandbox",
    "The implementation does not self-modify",
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
EXPECTED_RELEASE_VERSION = "4.0.0"
CURRENT_WHITEPAPER_PATH = Path("docs/whitepaper/F7-LAS-Whitepaper-v4.1-Restored-Full-Edition.pdf")
CURRENT_WHITEPAPER_CHECKSUM_PATH = Path(
    "docs/whitepaper/F7-LAS-Whitepaper-v4.1-Restored-Full-Edition.sha256"
)
CURRENT_WHITEPAPER_SHA256 = (
    "95cf7f053f0fe021c9b0cc50f81a81afb33ba3dbdceae1cd7bbbeff407706456"
)
HISTORICAL_V4_WHITEPAPER_PATH = Path("docs/whitepaper/F7-LAS-Whitepaper-v4.0.pdf")
HISTORICAL_V4_WHITEPAPER_SHA256 = (
    "67bfbff70f60309608921a58b28ee472d7aca876146988600916af093c992fe7"
)
HISTORICAL_WHITEPAPER_PATH = Path("docs/F7-LAS-model-whitepaper_v3.0.pdf")
HISTORICAL_WHITEPAPER_SHA256 = (
    "24f6e855fc8816edb200280c8cdf26fe41e3736a2544f87906bf2b2d273989fa"
)
RETIRED_PLACEHOLDERS = {
    Path("src/agents/placeholder"),
    Path("src/core/placeholder"),
    Path("src/tools/placeholder"),
}
CURRENT_STATUS_DOCUMENTS = {
    Path("README.md"),
    Path("RELEASE_NOTES.md"),
    Path("ROADMAP.md"),
    Path("docs/README.md"),
    Path("docs/F7-LAS-QA.md"),
    Path("docs/architecture-diagrams.md"),
    Path("docs/corrections/whitepaper-v3.0-errata.md"),
    Path("docs/f7-las-implementation-guide/README.md"),
}
STALE_STATUS_PATTERNS = {
    "unpublished release candidate": re.compile(
        r"unpublished\s+release[- ]candidate", re.IGNORECASE
    ),
    "not tagged or published": re.compile(
        r"not\s+tagged\s+or\s+published", re.IGNORECASE
    ),
    "whitepaper remains v3.0": re.compile(
        r"whitepaper\s+remains\s+(?:\*\*)?v3\.0", re.IGNORECASE
    ),
    "repository release candidate 4.0.0": re.compile(
        r"repository\s+release[- ]candidate\s+(?:\*\*)?4\.0\.0",
        re.IGNORECASE,
    ),
}


class DocumentationError(ValueError):
    """Raised when documentation cannot be followed from a clean checkout."""


def markdown_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.md")
        if not IGNORED_DIRECTORIES.intersection(path.relative_to(root).parts)
    )


def _link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")]
    return target.split(maxsplit=1)[0]


def validate_links(path: Path, root: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for raw_target in LINK_RE.findall(text):
        target = _link_target(raw_target)
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or target.startswith(("#", "mailto:")):
            continue
        relative = unquote(parsed.path)
        if not relative:
            continue
        resolved = (path.parent / relative).resolve()
        try:
            resolved.relative_to(root.resolve())
        except ValueError as exc:
            raise DocumentationError(
                f"{path.relative_to(root)}: link escapes repository: {target}"
            ) from exc
        if not resolved.exists():
            raise DocumentationError(
                f"{path.relative_to(root)}: unresolved relative link: {target}"
            )
        # Resolve each spelling exactly, including on case-insensitive hosts.
        exact = path.parent
        for part in Path(relative).parts:
            if part == "..":
                exact = exact.parent
            elif part != ".":
                if part not in {child.name for child in exact.iterdir()}:
                    raise DocumentationError(
                        f"{path.relative_to(root)}: case-sensitive path mismatch: {target}"
                    )
                exact /= part


def shell_blocks(path: Path, root: Path) -> list[tuple[int, str]]:
    blocks: list[tuple[int, str]] = []
    open_line: int | None = None
    language = ""
    content: list[str] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        match = FENCE_RE.match(line)
        if match:
            if open_line is None:
                open_line = number
                language = match.group(1).strip().lower()
                content = []
            else:
                if language in SHELL_LANGUAGES:
                    blocks.append((open_line, "\n".join(content)))
                open_line = None
                language = ""
                content = []
            continue
        if open_line is not None:
            content.append(line)
    if open_line is not None:
        raise DocumentationError(
            f"{path.relative_to(root)}:{open_line}: unclosed Markdown fence"
        )
    return blocks


def validate_command_boundaries(path: Path, root: Path) -> None:
    relative = path.relative_to(root)
    blocks = shell_blocks(path, root)
    if blocks and relative not in RUNNABLE_COMMAND_DOCS:
        raise DocumentationError(
            f"{relative}: shell commands appear outside supported command documentation"
        )
    for line_number, block in blocks:
        for offset, line in enumerate(block.splitlines()):
            if re.search(r"(?<!python -m )\bpytest\b", line):
                raise DocumentationError(
                    f"{relative}:{line_number + offset + 1}: use 'python -m pytest' "
                    "so the repository root is importable in a clean virtual environment"
                )


def validate_png(path: Path, expected_digest: str, expected_size: tuple[int, int]) -> None:
    try:
        content = path.read_bytes()
    except OSError as exc:
        raise DocumentationError(f"missing canonical diagram asset: {path}") from exc
    if hashlib.sha256(content).hexdigest() != expected_digest:
        raise DocumentationError(f"canonical diagram digest mismatch: {path}")
    if len(content) < 24 or content[:8] != b"\x89PNG\r\n\x1a\n":
        raise DocumentationError(f"canonical diagram is not a valid PNG: {path}")
    width, height = struct.unpack(">II", content[16:24])
    if (width, height) != expected_size:
        raise DocumentationError(
            f"canonical diagram dimensions mismatch: {path}: {(width, height)}"
        )


def validate_diagrams(root: Path) -> None:
    for relative, (digest, dimensions) in EXPECTED_DIAGRAMS.items():
        validate_png(root / relative, digest, dimensions)
    for relative in RETIRED_DIAGRAMS:
        if (root / relative).exists():
            raise DocumentationError(f"retired legacy diagram returned: {relative}")

    guide = (root / "docs" / "architecture-diagrams.md").read_text(encoding="utf-8")
    for relative, alt_text in REQUIRED_DIAGRAM_ALT_TEXT.items():
        guide_target = relative.relative_to("docs").as_posix()
        expected_reference = f"![{alt_text}]({guide_target})"
        if expected_reference not in guide:
            raise DocumentationError(
                f"architecture diagram guide is missing accessible alt text: {relative}"
            )
    normalized_guide = " ".join(guide.split())
    for notice in REQUIRED_DIAGRAM_NOTICES:
        if notice not in normalized_guide:
            raise DocumentationError(
                f"architecture diagram guide is missing required semantics: {notice}"
            )


def validate_pdf_digest(path: Path, expected_digest: str, label: str) -> None:
    try:
        content = path.read_bytes()
    except OSError as exc:
        raise DocumentationError(f"missing {label}: {path}") from exc
    if not content.startswith(b"%PDF-"):
        raise DocumentationError(f"{label} is not a PDF: {path}")
    if hashlib.sha256(content).hexdigest() != expected_digest:
        raise DocumentationError(f"{label} digest mismatch: {path}")


def validate_whitepapers(root: Path) -> None:
    current = root / CURRENT_WHITEPAPER_PATH
    validate_pdf_digest(current, CURRENT_WHITEPAPER_SHA256, "current whitepaper")
    validate_pdf_digest(
        root / HISTORICAL_WHITEPAPER_PATH,
        HISTORICAL_WHITEPAPER_SHA256,
        "historical whitepaper",
    )
    validate_pdf_digest(
        root / HISTORICAL_V4_WHITEPAPER_PATH,
        HISTORICAL_V4_WHITEPAPER_SHA256,
        "historical v4.0 whitepaper",
    )

    expected_manifest = (
        f"{CURRENT_WHITEPAPER_SHA256}  {CURRENT_WHITEPAPER_PATH.name}\n"
    )
    try:
        manifest = (root / CURRENT_WHITEPAPER_CHECKSUM_PATH).read_text(
            encoding="ascii"
        )
    except OSError as exc:
        raise DocumentationError(
            f"missing current whitepaper checksum: {CURRENT_WHITEPAPER_CHECKSUM_PATH}"
        ) from exc
    if manifest != expected_manifest:
        raise DocumentationError("current whitepaper checksum manifest mismatch")

    whitepaper_directory = current.parent
    if whitepaper_directory.exists() and any(
        path.suffix.lower() == ".docx" for path in whitepaper_directory.iterdir()
    ):
        raise DocumentationError("DOCX whitepaper artifacts must not be published here")

    required_references = {
        Path("README.md"): {
            f"(docs/whitepaper/{CURRENT_WHITEPAPER_PATH.name})",
            f"(docs/whitepaper/{CURRENT_WHITEPAPER_CHECKSUM_PATH.name})",
            "Whitepaper version **4.1**",
            "repository release **v4.0.0**",
        },
        Path("docs/README.md"): {
            f"(whitepaper/{CURRENT_WHITEPAPER_PATH.name})",
            f"(whitepaper/{CURRENT_WHITEPAPER_CHECKSUM_PATH.name})",
            "Whitepaper version **4.1 — Restored Full Edition**",
            "repository release **v4.0.0**",
        },
    }
    for relative, required in required_references.items():
        text = (root / relative).read_text(encoding="utf-8")
        missing = sorted(item for item in required if item not in text)
        if missing:
            raise DocumentationError(
                f"{relative} has drifted from the current whitepaper metadata: {missing}"
            )

    citation = (root / "CITATION.cff").read_text(encoding="utf-8")
    required_citation = {
        'title: "F7-LAS Whitepaper v4.1 — Restored Full Edition"',
        'version: "4.1"',
        'date-released: "2026-09-25"',
    }
    missing_citation = sorted(
        item for item in required_citation if item not in citation
    )
    if missing_citation:
        raise DocumentationError(
            f"CITATION.cff has drifted from Whitepaper v4.1: {missing_citation}"
        )
    if "doi:" in citation or "zenodo.22867553" in citation:
        raise DocumentationError("CITATION.cff must not assign the historical v4.0 DOI to v4.1")


def validate_no_stale_status(relative: Path, text: str) -> None:
    for label, pattern in STALE_STATUS_PATTERNS.items():
        if pattern.search(text):
            raise DocumentationError(
                f"{relative} contains stale current-status assertion: {label}"
            )


def validate_release_status(root: Path) -> None:
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if version != EXPECTED_RELEASE_VERSION:
        raise DocumentationError(
            f"VERSION must be {EXPECTED_RELEASE_VERSION}; found {version!r}"
        )
    required_version_documents = {
        Path("README.md"): "repository release **v4.0.0**",
        Path("RELEASE_NOTES.md"): "Published as the",
        Path("ROADMAP.md"): "tagged and published",
        Path("docs/F7-LAS-QA.md"): (
            "prototype published in tagged repository release v4.0.0"
        ),
        Path("docs/f7-las-implementation-guide/README.md"): (
            "bundled with repository release v4.0.0"
        ),
        Path("docs/release-process.md"): "v4.0.0",
    }
    for relative, boundary in required_version_documents.items():
        text = (root / relative).read_text(encoding="utf-8")
        if EXPECTED_RELEASE_VERSION not in text or boundary not in text:
            raise DocumentationError(
                f"{relative} does not state the {EXPECTED_RELEASE_VERSION} release boundary"
            )

    release_notes = (root / "RELEASE_NOTES.md").read_text(encoding="utf-8")
    for boundary in (
        "Whitepaper v4.0 was published separately",
        "not part of the immutable",
        "The tag retains Whitepaper v3.0 as a historical artifact",
    ):
        if boundary not in release_notes:
            raise DocumentationError(
                f"RELEASE_NOTES.md is missing whitepaper/release separation: {boundary}"
            )

    for relative in CURRENT_STATUS_DOCUMENTS:
        validate_no_stale_status(
            relative, (root / relative).read_text(encoding="utf-8")
        )

    for relative in RETIRED_PLACEHOLDERS:
        if (root / relative).exists():
            raise DocumentationError(f"retired placeholder returned: {relative}")

    readme = (root / "README.md").read_text(encoding="utf-8")
    docs_index = (root / "docs" / "README.md").read_text(encoding="utf-8")
    count_wording = "46 core Layers 1–7 controls plus five supplemental Layer S controls"
    if count_wording not in readme or count_wording not in docs_index:
        raise DocumentationError("control-catalog count wording is inconsistent")


def validate_repository(root: Path = ROOT) -> None:
    for path in markdown_files(root):
        validate_links(path, root)
        validate_command_boundaries(path, root)

    validate_diagrams(root)
    validate_whitepapers(root)
    validate_release_status(root)

    illustrative_opa = (
        root / "examples" / "layer5-policy-engines" / "opa-rego" / "README.md"
    ).read_text(encoding="utf-8")
    required_notice = "illustrative, non-canonical, and unsupported as a runnable walkthrough"
    if required_notice not in illustrative_opa:
        raise DocumentationError(
            "the non-canonical OPA example must retain its unsupported-walkthrough notice"
        )


def main() -> int:
    try:
        validate_repository()
    except (DocumentationError, OSError, UnicodeError) as exc:
        print(f"documentation validation failed: {exc}", file=sys.stderr)
        return 1
    print("F7-LAS documentation validation PASSED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
