import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

LEDGER_PATH = Path("ledger/ledger.jsonl")
VERIFICATION_RECORD_PATH = Path("verification_record.json")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json(obj: dict) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def get_previous_entry_hash() -> str:
    if not LEDGER_PATH.exists() or LEDGER_PATH.stat().st_size == 0:
        return "GENESIS"

    last_line = ""
    with LEDGER_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                last_line = line.strip()

    if not last_line:
        return "GENESIS"

    last_entry = json.loads(last_line)
    return last_entry["entry_hash"]


def main() -> None:
    if not VERIFICATION_RECORD_PATH.exists():
        raise FileNotFoundError(f"Missing {VERIFICATION_RECORD_PATH}")

    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    LEDGER_PATH.touch(exist_ok=True)

    verification_record_sha256 = sha256_file(VERIFICATION_RECORD_PATH)
    previous_entry_hash = get_previous_entry_hash()

    entry = {
        "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "repo": os.getenv("GITHUB_REPOSITORY", "unknown"),
        "commit_sha": os.getenv("GITHUB_SHA", "unknown"),
        "run_id": os.getenv("GITHUB_RUN_ID", "unknown"),
        "verification_record_sha256": verification_record_sha256,
        "previous_entry_hash": previous_entry_hash,
    }

    entry_hash = sha256_bytes(canonical_json(entry))
    entry["entry_hash"] = entry_hash

    with LEDGER_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")

    print(f"Appended ledger entry: {entry_hash}")


if __name__ == "__main__":
    main()
