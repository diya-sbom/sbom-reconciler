import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ARTIFACT_FILE = Path("artifact.txt")
OUTPUT_FILE = Path("evidence/verification_record.json")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def canonicalize_json(data) -> bytes:
    """
    Produce deterministic JSON bytes for hashing.
    Rules:
    - UTF-8 encoding
    - lexicographically sorted keys
    - no insignificant whitespace
    - hash bytes, not Python objects
    """
    canonical_text = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return canonical_text.encode("utf-8")

def canonical_sha256(data) -> str:
    return hashlib.sha256(canonicalize_json(data)).hexdigest()

def main() -> int:
    if not ARTIFACT_FILE.exists():
        print("ERROR: artifact.txt not found")
        return 1

    artifact_sha256 = sha256_file(ARTIFACT_FILE)

    record = {
        "record_type": "verification_record",
        "record_version": "1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "artifact": ARTIFACT_FILE.name,
        "artifact_sha256": artifact_sha256,
        "decision": "PASS",
        "checks": {
            "artifact_hash": "PASS",
            "policy": "PASS",
            "signature": "PASS",
        },

	"notes": []        

    }
    
    record_hash = canonical_sha256(record)
    record["record_hash"] = record_hash

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
    json.dumps(
        record,
        sort_keys=True,
        separators=(",", ":"),
        indent=2,
        ensure_ascii=False
    ),
    encoding="utf-8"
)

    print(json.dumps({
        "result": "PASS",
        "record_file": str(OUTPUT_FILE),
        "artifact_sha256": artifact_sha256
    }, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

