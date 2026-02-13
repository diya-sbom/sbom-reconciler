#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
from datetime import datetime


def sha256_of_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    p = argparse.ArgumentParser(description="BIL receipt generator")
    p.add_argument("--intent", required=True, help="e.g., pre-deploy, deploy, release")
    p.add_argument("--artifact", required=True, help="path to file to hash")
    p.add_argument("--out", required=True, help="output JSON receipt path")
    args = p.parse_args()

    artifact_hash = sha256_of_file(args.artifact)

    receipt = {
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "intent": args.intent,
        "artifact": args.artifact,
        "artifact_sha256": artifact_hash,
        "status": "RECORDED",
    }

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)
        f.write("\n")

    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
