import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


EVIDENCE_DIR = Path("evidence")
LEDGER_DIR = Path("ledger")
LEDGER_FILE = LEDGER_DIR / "ledger.jsonl"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def get_last_entry_hash() -> str | None:
    if not LEDGER_FILE.exists():
        return None

    lines = LEDGER_FILE.read_text(encoding="utf-8").splitlines()
    if not lines:
        return None

    last_line = lines[-1].strip()
    if not last_line:
        return None

    return sha256_text(last_line)


def main() -> int:
    bundle_hash = read_text(EVIDENCE_DIR / "bundle.sha256")
    gate_result = read_json(EVIDENCE_DIR / "gate_result.json")

    if not bundle_hash:
        print("ERROR: evidence/bundle.sha256 not found or empty")
        return 1

    if not gate_result:
        print("ERROR: evidence/gate_result.json not found or empty")
        return 1

    artifact = gate_result.get("artifact", "UNKNOWN")
    decision = gate_result.get("result", "UNKNOWN")
    prev_hash = get_last_entry_hash()

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "artifact": artifact,
        "decision": decision,
        "bundle_sha256": bundle_hash,
        "prev_entry_hash": prev_hash
    }

    entry_text = json.dumps(entry, sort_keys=True)
    entry_hash = sha256_text(entry_text)
    entry["entry_hash"] = entry_hash

    LEDGER_DIR.mkdir(exist_ok=True)

    with LEDGER_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    print(json.dumps({
        "result": "PASS",
        "ledger_file": str(LEDGER_FILE),
        "entry": entry
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
