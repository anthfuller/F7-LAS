"""
F7-LAS Stage 2 – Investigator Agent (Layer 3)
Evidence-first execution.
Runs an explicit plan through the centralized MCP executor.
Persists raw evidence for downstream signal extraction.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from telemetry.audit import write_audit
from telemetry.logger import log_event
from mcp.executor import execute as mcp_execute


class InvestigatorAgent:
    def __init__(self):
        pass

    def investigate(self, plan: List[Dict[str, Any]], *, run_id: str) -> Dict[str, Any]:
        log_event("investigator_started", {"run_id": run_id, "steps": len(plan)})

        evidence: List[Dict[str, Any]] = []

        # Evidence directory
        evidence_dir = Path("runs") / run_id / "evidence"
        evidence_dir.mkdir(parents=True, exist_ok=True)

        for step in plan:
            tool = step.get("tool")
            params = step.get("params") or {}
            if not tool:
                continue

            result = mcp_execute(tool, run_id=run_id, params=params)
            evidence.append(result)

            table = result.get("table")
            if not table:
                continue

            # Normalize rows → JSON safe
            safe_rows = []
            for row in result.get("rows", []):
                if isinstance(row, (list, tuple)):
                    safe_rows.append([str(v) for v in row])
                else:
                    safe_rows.append(str(row))

            evidence_file = evidence_dir / f"{table.lower()}.json"
            with evidence_file.open("w", encoding="utf-8") as f:
                json.dump(
                    {
                        "table": table,
                        "query": result.get("query"),
                        "columns": result.get("columns", []),
                        "rows": safe_rows,
                        "rowcount": result.get("rowcount", 0),
                    },
                    f,
                    indent=2,
                    default=str,  # 🔑 FINAL GUARANTEE
                )

        write_audit(
            run_id=run_id,
            stage="investigation_complete",
            data={"evidence_items": len(evidence)},
        )

        log_event(
            "investigator_completed",
            {"run_id": run_id, "evidence_items": len(evidence)},
        )

        return {"evidence": evidence}
