"""Command-line entry point for the canonical offline workflow."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .validation import load_json
from .workflow import CanonicalWorkflow, WorkflowError


def _same_file(first: Path, second: Path) -> bool:
    """Return whether two paths resolve to the same inode or destination."""

    if first.resolve() == second.resolve():
        return True
    return first.exists() and second.exists() and os.path.samefile(first, second)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--opa-binary", default="opa")
    args = parser.parse_args()

    try:
        if _same_file(args.output, args.input):
            raise WorkflowError("output must not overwrite input")
        workflow_input = load_json(args.input)
        result = CanonicalWorkflow(opa_binary=args.opa_binary).run(workflow_input)
        if _same_file(args.output, args.input):
            raise WorkflowError("output must not overwrite input")
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except (OSError, json.JSONDecodeError, TypeError, ValueError, WorkflowError) as exc:
        print(f"F7-LAS canonical workflow refused input: {exc}")
        return 2

    decision = next(record for record in result["records"] if record["record_type"] == "policy_decision")
    execution = next(record for record in result["records"] if record["record_type"] == "execution_result")
    print(f"decision={decision['decision']} execution={execution['status']} output={args.output}")
    if decision["decision"] != "permit" or execution["status"] != "succeeded":
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
