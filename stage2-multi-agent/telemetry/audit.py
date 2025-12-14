import json
from datetime import datetime

AUDIT_FILE = "telemetry/audit_log.jsonl"

def write_audit(run_id: str, stage: str, data: dict):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "run_id": run_id,
        "stage": stage,
        "data": data
    }
    with open(AUDIT_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")
