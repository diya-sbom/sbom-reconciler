import hashlib
import json
import sys
from pathlib import Path


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def verify_ledger(path: str) -> dict:
    ledger_path = Path(path)

    if not ledger_path.exists():
        return {
            "result": "FAIL",
            "error": "ledger_not_found",
            "ledger_file": str(ledger_path)
        }

    lines = [
        line.strip()
        for line in ledger_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    if not lines:
        return {
            "result": "FAIL",
            "error": "ledger_empty",
            "ledger_file": str(ledger_path)
        }

    previous_line = None

    for index, line in enumerate(lines):
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            return {
                "result": "FAIL",
                "error": "invalid_json_line",
                "line_number": index + 1
            }

        if index == 0:
            if entry.get("prev_entry_hash") is not None:
                return {
                    "result": "FAIL",
                    "error": "first_entry_prev_hash_not_null"
                }
        else:
            expected_prev = sha256_text(previous_line)

            if entry.get("prev_entry_hash") != expected_prev:
                return {
                    "result": "FAIL",
                    "error": "prev_hash_mismatch",
                    "line_number": index + 1,
                    "expected_prev_entry_hash": expected_prev,
                    "actual_prev_entry_hash": entry.get("prev_entry_hash")
                }

        previous_line = line

    return {
        "result": "PASS",
        "ledger_file": str(ledger_path),
        "entries_verified": len(lines),
        "final_entry_hash": sha256_text(previous_line) if previous_line else None
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 cli/verify_ledger.py ledger/ledger.jsonl")
        sys.exit(1)

    result = verify_ledger(sys.argv[1])
    print(json.dumps(result, indent=2))

    if result["result"] != "PASS":
        sys.exit(1)


if __name__ == "__main__":
    main()
