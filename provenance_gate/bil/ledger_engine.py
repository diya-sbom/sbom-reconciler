#!/usr/bin/env python3
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

LEDGER_PATH = Path("bil/ledger.jsonl")

# ---------- hashing helpers ----------

def _canon(obj: Dict[str, Any]) -> str:
    # Deterministic JSON for hashing (stable across runs)
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()

# ---------- ledger ops ----------

def get_last_entry_hash() -> str:
    if (not LEDGER_PATH.exists()) or LEDGER_PATH.stat().st_size == 0:
        return "GENESIS"

    last_line: Optional[str] = None
    with LEDGER_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                last_line = line

    if not last_line:
        return "GENESIS"

    last = json.loads(last_line)
    return str(last.get("entry_hash", "GENESIS"))

def append_entry(
    artifact: str,
    digest: str,
    builder: str,
    approver: str,
    decision: str,
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    entry: Dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "artifact": artifact,
        "digest": digest,
        "builder": builder,
        "approver": approver,
        "decision": decision,
        "previous_hash": get_last_entry_hash(),
    }

    if extra:
        # extra fields are included in the hash (so they are tamper-evident)
        for k, v in extra.items():
            if k not in entry:
                entry[k] = v

    entry_hash = sha256_hex(_canon(entry))
    entry["entry_hash"] = entry_hash

    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER_PATH.open("a", encoding="utf-8") as f:
        f.write(_canon(entry) + "\n")

    return entry

# ---------- CLI demo (optional) ----------

if __name__ == "__main__":
    # You can edit these values anytime for a quick test
    artifact_path = "artifact.txt"

    e = append_entry(
        artifact=artifact_path,
        digest=sha256_file(artifact_path),
        builder="local-mac",
        approver="local-dev",
        decision="PASS",
    )

    print("ENTRY WRITTEN")
    print(json.dumps(e, indent=2, sort_keys=True))
