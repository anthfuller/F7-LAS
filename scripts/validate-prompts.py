#!/usr/bin/env python3
"""
F7-LAS Prompt Validator

Validates all prompt files under config/prompts/ to ensure they
conform to the F7-LAS Prompt Security Profile (PSP) structure.

Checks:
- BEGIN / END markers
- Required section headers
- PSP metadata fields
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PROMPT_DIR = REPO_ROOT / "config" / "prompts"

# Added, was missing during updated code

prompt_files_glob = "*.txt"

REQUIRED_SECTIONS = [
    "[ROLE]",
    "[SCOPE]",
    "[PROHIBITED ACTIONS]",
    "[ESCALATION RULES]",
    "[PROMPT SECURITY PROFILE METADATA]",
]

# Validate ALL .txt prompts (hyphens included)
prompt_files = sorted([
    *PROMPT_DIR.glob("*-agent-prompt-*.txt"),
    *PROMPT_DIR.glob("system-prompt-*.txt"),
])

REQUIRED_SECTIONS = [
    "[ROLE]",
    "[SCOPE]",
    "[PROHIBITED ACTIONS]",
    "[ESCALATION RULES]",
    "[PROMPT SECURITY PROFILE METADATA]",
]

REQUIRED_METADATA_FIELDS = [
    "PSP-Version:",
    "PSP-ID:",
    "Approved-By:",
    "Change-Ticket:",
    "Date-Approved:",
    "Risk-Tier:",
]

BEGIN_MARKER = "==== BEGIN SYSTEM PROMPT ===="
END_MARKER = "==== END SYSTEM PROMPT ===="


def validate_prompt_file(path: Path) -> list[str]:
    errors: list[str] = []

    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        errors.append(f"{path}: cannot read file ({e})")
        return errors

    # Basic markers
    if BEGIN_MARKER not in text:
        errors.append(f"{path}: missing BEGIN marker: {BEGIN_MARKER!r}")
    if END_MARKER not in text:
        errors.append(f"{path}: missing END marker: {END_MARKER!r}")
    if BEGIN_MARKER in text and END_MARKER in text:
        if text.index(BEGIN_MARKER) > text.index(END_MARKER):
            errors.append(f"{path}: BEGIN marker appears after END marker")

    # Required section headers
    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"{path}: missing required section header {section!r}")

    # PSP metadata block
    if "[PROMPT SECURITY PROFILE METADATA]" in text:
        meta_start = text.index("[PROMPT SECURITY PROFILE METADATA]")
        meta_block = text[meta_start:]

        # Stop before next section header
        for line in meta_block.splitlines()[1:]:
            if line.strip().startswith("[") and line.strip().endswith("]"):
                meta_block = meta_block.split(line, 1)[0]
                break

        for field in REQUIRED_METADATA_FIELDS:
            if field not in meta_block:
                errors.append(f"{path}: missing metadata field {field!r}")
    else:
        errors.append(
            f"{path}: missing [PROMPT SECURITY PROFILE METADATA] section entirely"
        )

    return errors


def main() -> int:
    if not PROMPT_DIR.exists():
        print(f"[ERROR] Prompt directory not found: {PROMPT_DIR}", file=sys.stderr)
        return 1

    prompt_files = sorted(PROMPT_DIR.glob(prompt_files_glob))
    if not prompt_files:
        print(f"[WARN] No prompt files matching pattern {prompt_files_glob!r} found.")
        return 0

    all_errors: list[str] = []
    for path in prompt_files:
        errors = validate_prompt_file(path)
        if errors:
            all_errors.extend(errors)

    if all_errors:
        print("F7-LAS prompt validation FAILED:\n", file=sys.stderr)
        for err in all_errors:
            print(f" - {err}", file=sys.stderr)
        return 1

    print("F7-LAS prompt validation PASSED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


