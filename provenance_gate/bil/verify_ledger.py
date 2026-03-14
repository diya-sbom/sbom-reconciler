import json, hashlib, sys, os

LEDGER = "bil/ledger.jsonl"
GENESIS = "0" * 64

def sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def canon(o) -> str:
    return json.dumps(o, sort_keys=True, separators=(",", ":"))

def main():
    if not os.path.exists(LEDGER):
        print("FAIL: missing ledger file")
        return 1

    prev = GENESIS
    n = 0

    with open(LEDGER, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            n += 1
            entry = json.loads(line)

            # must have required fields
            if "previous_hash" not in entry or "entry_hash" not in entry:
                print(f"FAIL: entry {n} missing previous_hash/entry_hash")
                return 1

            if entry["previous_hash"] != prev:
                print(f"FAIL: entry {n} previous_hash mismatch")
                return 1

            # recompute hash of entry WITHOUT entry_hash
            entry_copy = dict(entry)
            expected_hash = entry_copy.pop("entry_hash")
            computed = sha256(canon(entry_copy))

            if computed != expected_hash:
                print(f"FAIL: entry {n} entry_hash mismatch")
                return 1

            prev = expected_hash

    print(f"PASS: verified {n} entries")
    return 0

if __name__ == "__main__":
    sys.exit(main())
