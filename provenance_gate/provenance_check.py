#!/usr/bin/env python3
import sys
import json
import hashlib
import os
from datetime import datetime

PASS = 0
FAIL = 1
INCONCLUSIVE = 2

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def valid_sha256(value):
    if not value:
        return False
    value = value.lower().replace("sha256:", "")
    return len(value) == 64 and all(c in "0123456789abcdef" for c in value)

def valid_timestamp(ts):
    try:
        datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return True
    except Exception:
        return False

def output(result, **kwargs):
    payload = {
        "tool": "provenance_check",
        "version": "0.3",
        "result": result
    }
    payload.update(kwargs)
    print(json.dumps(payload))

def main():
    if len(sys.argv) != 4:
        output("INCONCLUSIVE", error="usage: provenance_check.py <artifact_file> <provenance_json> <expected_sha256>")
        return INCONCLUSIVE

    artifact_file = sys.argv[1]
    provenance_file = sys.argv[2]
    expected = sys.argv[3].lower().replace("sha256:", "")

    if not os.path.exists(artifact_file):
        output("INCONCLUSIVE", error="artifact_not_found")
        return INCONCLUSIVE

    if not os.path.exists(provenance_file):
        output("INCONCLUSIVE", error="provenance_not_found")
        return INCONCLUSIVE

    if not valid_sha256(expected):
        output("INCONCLUSIVE", error="invalid_expected_sha256")
        return INCONCLUSIVE

    with open(provenance_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    found = data.get("found_sha256", "").lower().replace("sha256:", "")
    commit = data.get("commit")
    builder = data.get("builder")
    timestamp = data.get("timestamp")

    if not valid_sha256(found):
        output("INCONCLUSIVE", error="invalid_or_missing_found_sha256")
        return INCONCLUSIVE

    actual_hash = sha256_file(artifact_file)

    if actual_hash != found:
        output("FAIL", reason="artifact_hash_mismatch", computed=actual_hash, declared=found)
        return FAIL

    if found != expected:
        output("FAIL", reason="expected_hash_mismatch", expected=expected, declared=found)
        return FAIL

    if not commit or not builder or not valid_timestamp(timestamp):
        output("INCONCLUSIVE", error="missing_metadata_fields")
        return INCONCLUSIVE

    output("PASS", sha256=found)
    return PASS

if __name__ == "__main__":
    sys.exit(main())
