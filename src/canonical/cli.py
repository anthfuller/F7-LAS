"""Command-line entry point for the canonical offline workflow."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .workflow import CanonicalWorkflow, WorkflowError


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--opa-binary", default="opa")
    args = parser.parse_args()

    try:
        with args.input.open("r", encoding="utf-8") as handle:
            workflow_input = json.load(handle)
        result = CanonicalWorkflow(opa_binary=args.opa_binary).run(workflow_input)
    except (OSError, json.JSONDecodeError, WorkflowError) as exc:
        print(f"F7-LAS canonical workflow refused input: {exc}")
        return 2

    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    decision = next(record for record in result["records"] if record["record_type"] == "policy_decision")
    execution = next(record for record in result["records"] if record["record_type"] == "execution_result")
    print(f"decision={decision['decision']} execution={execution['status']} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
