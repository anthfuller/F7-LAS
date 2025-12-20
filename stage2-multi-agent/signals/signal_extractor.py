# signals/signal_extractor.py
from __future__ import annotations

import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List


def _safe_parse_time(value: Any) -> Optional[datetime]:
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        # handle both "2025-12-17T03:02:13.356Z" and "2025-12-17 03:02:13.356"
        s = value.strip().replace("Z", "")
        try:
            return datetime.fromisoformat(s)
        except Exception:
            return None
    return None


def _iter_row_lists(rows: Any) -> List[List[Any]]:
    """
    Yield only list/tuple rows. Ignore strings/objects (legacy evidence).
    """
    out: List[List[Any]] = []
    if not rows:
        return out
    for r in rows:
        if isinstance(r, (list, tuple)):
            out.append(list(r))
        # else: ignore (prevents the 'e' / char-indexing failure)
    return out


def extract_domain_signals(run_dir: Path, domain_config: Dict[str, Any]) -> Dict[str, Any]:
    domains_out = []
    time_start: Optional[datetime] = None
    time_end: Optional[datetime] = None

    for domain, cfg in domain_config.get("domains", {}).items():
        domain_metrics: Dict[str, int] = {}
        tables_used = []
        signals_present = False

        for table_cfg in cfg.get("tables", []):
            table_name = table_cfg["name"]
            evidence_file = run_dir / "evidence" / f"{table_name.lower()}.json"
            if not evidence_file.exists():
                continue

            tables_used.append(table_name)

            with evidence_file.open(encoding="utf-8") as f:
                evidence = json.load(f)

            columns = evidence.get("columns", []) or []
            rows_raw = evidence.get("rows", []) or []
            rows = _iter_row_lists(rows_raw)

            # --- Track time window safely ---
            if "TimeGenerated" in columns:
                idx = columns.index("TimeGenerated")
                for row in rows:
                    if idx >= len(row):
                        continue
                    ts = _safe_parse_time(row[idx])
                    if not ts:
                        continue
                    time_start = ts if not time_start else min(time_start, ts)
                    time_end = ts if not time_end else max(time_end, ts)

            # --- Metrics ---
            for metric in table_cfg.get("metrics", []):
                metric_id = metric["id"]
                count = 0

                for row in rows:
                    match = True
                    if "where" in metric:
                        field = metric["where"]["field"]
                        op = metric["where"]["op"]
                        value = metric["where"].get("value")
                        values = metric["where"].get("values") or []

                        if field not in columns:
                            match = False
                        else:
                            ci = columns.index(field)
                            if ci >= len(row):
                                match = False
                            else:
                                cell = row[ci]
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

        domains_out.append(
            {
                "domain": domain,
                "signals_present": signals_present,
                "tables": tables_used,
                "metrics": domain_metrics,
            }
        )

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
        domain_config = yaml.safe_load(f)

    return extract_domain_signals(run_dir=run_dir, domain_config=domain_config)
