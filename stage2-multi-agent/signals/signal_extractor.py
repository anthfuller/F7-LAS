# signals/signal_extractor.py

from __future__ import annotations

import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any


def extract_domain_signals(run_dir: Path, domain_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert raw evidence into domain-level metrics.
    No interpretation. No thresholds. Counts only.
    """

    domains_out = []
    time_start = None
    time_end = None

    for domain, cfg in domain_config["domains"].items():
        domain_metrics = {}
        tables_used = []
        signals_present = False

        for table_cfg in cfg["tables"]:
            table_name = table_cfg["name"]
            evidence_file = run_dir / "evidence" / f"{table_name.lower()}.json"

            if not evidence_file.exists():
                continue

            tables_used.append(table_name)

            with evidence_file.open(encoding="utf-8") as f:
                evidence = json.load(f)

            rows = evidence.get("rows", [])
            columns = evidence.get("columns", [])

            # Track time window
            if "TimeGenerated" in columns:
                idx = columns.index("TimeGenerated")
                times = [row[idx] for row in rows if row[idx]]
                parsed = [datetime.fromisoformat(t.replace("Z", "")) for t in times]
                if parsed:
                    time_start = min(parsed) if not time_start else min(time_start, min(parsed))
                    time_end = max(parsed) if not time_end else max(time_end, max(parsed))

            for metric in table_cfg.get("metrics", []):
                metric_id = metric["id"]
                count = 0

                for row in rows:
                    match = True

                    if "where" in metric:
                        field = metric["where"]["field"]
                        op = metric["where"]["op"]
                        value = metric["where"].get("value")
                        values = metric["where"].get("values")

                        if field not in columns:
                            match = False
                        else:
                            cell = row[columns.index(field)]
                            if op == "==" and cell != value:
                                match = False
                            elif op == "!=" and cell == value:
                                match = False
                            elif op == "in" and cell not in values:
                                match = False

                    if match:
                        count += 1

                domain_metrics[metric_id] = count
                if count > 0:
                    signals_present = True

        domains_out.append({
            "domain": domain,
            "signals_present": signals_present,
            "tables": tables_used,
            "metrics": domain_metrics,
        })

    return {
        "domains": domains_out,
        "time_window": {
            "start": time_start.isoformat() if time_start else None,
            "end": time_end.isoformat() if time_end else None,
        },
    }


def extract_signals(*, investigation: Dict[str, Any], run_id: str) -> Dict[str, Any]:
    """
    Orchestrator-facing entry point.
    Loads domain configuration and extracts domain signals.
    """

    run_dir = Path("runs") / run_id

    domain_cfg_path = Path(__file__).parent / "domain_signals.yaml"
    with domain_cfg_path.open(encoding="utf-8") as f:
        domain_config = yaml.safe_load(f)

    return extract_domain_signals(
        run_dir=run_dir,
        domain_config=domain_config,
    )
