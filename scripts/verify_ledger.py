import hashlib
import json
from pathlib import Path

LEDGER_PATH = Path("ledger/ledger.jsonl")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(obj: dict) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def main() -> None:
    if not LEDGER_PATH.exists():
        raise FileNotFoundError(f"Missing {LEDGER_PATH}")

    previous_hash = "GENESIS"

    with LEDGER_PATH.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            entry = json.loads(line)
            stored_hash = entry.get("entry_hash")
            stored_previous = entry.get("previous_entry_hash")

            if stored_previous != previous_hash:
                raise ValueError(
                    f"Chain break at line {idx}: expected previous_entry_hash={previous_hash}, got {stored_previous}"
                )

            entry_without_hash = dict(entry)
            entry_without_hash.pop("entry_hash", None)
            recomputed_hash = sha256_bytes(canonical_json(entry_without_hash))

            if recomputed_hash != stored_hash:
                raise ValueError(
                    f"Hash mismatch at line {idx}: expected {recomputed_hash}, got {stored_hash}"
                )

            previous_hash = stored_hash

    print("Ledger verification passed.")


if __name__ == "__main__":
    main()
