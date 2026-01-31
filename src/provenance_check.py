import json
import sys
from pathlib import Path

TOOL = "provenance_check"
VERSION = "0.1"

def emit(payload: dict) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))

def main() -> None:
    if len(sys.argv) != 3:
        emit({
            "tool": TOOL,
            "version": VERSION,
            "result": "INCONCLUSIVE",
            "error": "usage: provenance_check.py <provenance.json> <expected_sha256>",
        })
        sys.exit(2)

    prov_path = Path(sys.argv[1])
    expected = sys.argv[2]

    if not prov_path.exists():
        emit({
            "tool": TOOL,
            "version": VERSION,
            "result": "INCONCLUSIVE",
            "error": "file_not_found",
            "file": str(prov_path),
        })
        sys.exit(2)

    doc = json.loads(prov_path.read_text())

    statement_type = doc.get("_type")
    predicate_type = doc.get("predicateType")

    subjects = doc.get("subject", [])
    if not subjects:
        emit({
            "tool": TOOL,
            "version": VERSION,
            "result": "FAIL",
            "file": str(prov_path),
            "statement_type": statement_type,
            "predicate_type": predicate_type,
            "error": "no_subject",
        })
        sys.exit(1)

    subj0 = subjects[0] or {}
    name = subj0.get("name")
    found = (subj0.get("digest") or {}).get("sha256")

    payload = {
        "tool": TOOL,
        "version": VERSION,
        "result": "PASS" if found == expected else "FAIL",
        "file": str(prov_path),
        "statement_type": statement_type,
        "predicate_type": predicate_type,
        "subject": {
            "name": name,
            "expected_sha256": expected,
            "found_sha256": found,
        },
    }

    emit(payload)
    sys.exit(0 if payload["result"] == "PASS" else 1)

if __name__ == "__main__":
    main()

