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
        "23449ac61fc65089d96956d5900916f69ee637960d83a46ff847093e3da59159",
        (1672, 941),
    ),
    Path("docs/images/F7-LAS-Agentic-Execution-Control-Loop.png"): (
        "9f4400b86796f1f047e51f595f416be5c2c398801a146778833a821277cdd8d6",
        (1672, 941),
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
    normalized_guide = " ".join(guide.split())
    for notice in REQUIRED_DIAGRAM_NOTICES:
        if notice not in normalized_guide:
            raise DocumentationError(
                f"architecture diagram guide is missing required semantics: {notice}"
            )


def validate_repository(root: Path = ROOT) -> None:
    for path in markdown_files(root):
        validate_links(path, root)
        validate_command_boundaries(path, root)

    validate_diagrams(root)

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
