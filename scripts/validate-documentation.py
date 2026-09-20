#!/usr/bin/env python3
"""Validate repository Markdown links, fences, and runnable-command boundaries."""

from __future__ import annotations

import re
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


def validate_repository(root: Path = ROOT) -> None:
    for path in markdown_files(root):
        validate_links(path, root)
        validate_command_boundaries(path, root)

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
