from __future__ import annotations

import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


def _parse_time(v: Any) -> Optional[datetime]:
    if v is None:
        return None
    if isinstance(v, datetime):
        return v
    if not isinstance(v, str):
        return None
    s = v.strip()
    if not s:
        return None
    # Common Sentinel shapes: "2025-12-18T01:22:00Z" or "...+00:00"
    s = s.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None


def extract_domain_signals(run_dir: Path, domain_config: Dict[str, Any]) -> Dict[str, Any]:
    domains_out = []
    time_start: Optional[datetime] = None
    time_end: Optional[datetime] = None

    for domain, cfg in (domain_config.get("domains") or {}).items():
        domain_metrics: Dict[str, int] = {}
        tables_used = []
        signals_present = False

        for table_cfg in cfg.get("tables", []):
            table_name = table_cfg.get("name")
            if not table_name:
                continue

            evidence_file = run_dir / "evidence" / f"{table_name.lower()}.json"
            if not evidence_file.exists():
                continue

            tables_used.append(table_name)

            with evidence_file.open(encoding="utf-8") as f:
                evidence = json.load(f) or {}

            rows = evidence.get("rows", [])
            columns = evidence.get("columns", [])

            # Guard: rows must be list of lists
            if not isinstance(rows, list):
                rows = []
            rows = [r for r in rows if isinstance(r, list)]

            # Track time window (best-effort)
            if isinstance(columns, list) and "TimeGenerated" in columns:
                idx = columns.index("TimeGenerated")
                for r in rows:
                    if idx >= len(r):
                        continue
                    dt = _parse_time(r[idx])
                    if not dt:
                        continue
                    time_start = dt if time_start is None else min(time_start, dt)
                    time_end = dt if time_end is None else max(time_end, dt)

            # Metrics
            for metric in table_cfg.get("metrics", []):
                metric_id = metric.get("id")
                if not metric_id:
                    continue

                count = 0
                where = metric.get("where")

                for r in rows:
                    match = True
                    if where:
                        field = where.get("field")
                        op = where.get("op")
                        value = where.get("value")
                        values = where.get("values")

                        if not field or field not in columns:
                            match = False
                        else:
                            cell = r[columns.index(field)]
                            # Compare as strings for stability
                            cell_s = "" if cell is None else str(cell)

                            if op == "==" and cell_s != str(value):
                                match = False
                            elif op == "!=" and cell_s == str(value):
                                match = False
                            elif op == "in" and cell_s not in set(str(x) for x in (values or [])):
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
    run_dir = Path("runs") / run_id

    domain_cfg_path = Path(__file__).parent / "domain_signals.yaml"
    with domain_cfg_path.open(encoding="utf-8") as f:
        domain_config = yaml.safe_load(f) or {}

    return extract_domain_signals(run_dir=run_dir, domain_config=domain_config)
