#!/usr/bin/env python3
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOL_NAME = "provenance-gate"
SCHEMA_VERSION = "1.0"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: str) -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def normalize_digest(s: str) -> Tuple[str, str]:
    """
    Accepts:
      - "sha256:<hex>"
      - "<hex>" (defaults to sha256)
    Returns (algo, hex)
    """
    s = (s or "").strip()
    if not s:
        raise ValueError("Empty expected digest")

    if ":" in s:
        algo, hexdigest = s.split(":", 1)
        algo = algo.strip().lower()
        hexdigest = hexdigest.strip().lower()
    else:
        algo = "sha256"
        hexdigest = s.strip().lower()

    if algo not in ("sha256",):
        raise ValueError(f"Unsupported digest algorithm: {algo}")

    # basic validation
    if any(c not in "0123456789abcdef" for c in hexdigest):
        raise ValueError("Digest contains non-hex characters")
    if algo == "sha256" and len(hexdigest) != 64:
        raise ValueError("sha256 digest must be 64 hex characters")

    return algo, hexdigest


def compute_file_digest(path: str, algo: str = "sha256") -> str:
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_subject_digests(stmt: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Works for in-toto Statement-like JSON:
      { "subject": [ { "name": "...", "digest": { "sha256": "<hex>" } }, ... ] }
    Returns list of {name, algo, digest}.
    """
    subjects = stmt.get("subject")
    out: List[Dict[str, Any]] = []
    if not isinstance(subjects, list):
        return out

    for s in subjects:
        if not isinstance(s, dict):
            continue
        name = s.get("name") if isinstance(s.get("name"), str) else ""
        digest_obj = s.get("digest")
        if not isinstance(digest_obj, dict):
            continue
        for algo, hexdigest in digest_obj.items():
            if isinstance(algo, str) and isinstance(hexdigest, str):
                out.append(
                    {
                        "name": name,
                        "algo": algo.strip().lower(),
                        "digest": hexdigest.strip().lower(),
                    }
                )
    return out


def verdict(expected_algo: str, expected_hex: str, subject_digests: List[Dict[str, Any]]) -> Tuple[str, Dict[str, Any]]:
    """
    Returns (result, details)
    result ∈ PASS | FAIL | INCONCLUSIVE
    """
    if not subject_digests:
        return "INCONCLUSIVE", {
            "reason": "No subject digests found in provenance statement",
        }

    matches = [d for d in subject_digests if d["algo"] == expected_algo and d["digest"] == expected_hex]
    if matches:
        return "PASS", {
            "reason": "Expected digest matches a provenance subject digest",
            "matched_subjects": matches,
        }

    # digest present but different
    same_algo = [d for d in subject_digests if d["algo"] == expected_algo]
    return "FAIL", {
        "reason": "Expected digest does not match any provenance subject digest",
        "expected": {expected_algo: expected_hex},
        "subjects_with_same_algo": same_algo,
        "all_subjects": subject_digests,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Verify an artifact digest against a provenance statement subject digest.")
    ap.add_argument("--expected-digest", required=False, help='Expected digest, e.g. "sha256:<hex>" (defaults to sha256 if no prefix).')
    ap.add_argument("--artifact", required=False, help="Optional artifact file path. If provided, digest is computed and used as expected digest.")
    ap.add_argument("--provenance", required=True, help="Path to provenance statement JSON (in-toto / SLSA).")
    ap.add_argument("-o", "--output", help="Write evidence JSON to this file (also prints to stdout).")

    args = ap.parse_args()

    # Determine expected digest
    expected_algo: Optional[str] = None
    expected_hex: Optional[str] = None
    expected_source = None

    try:
        if args.artifact:
            expected_algo = "sha256"
            expected_hex = compute_file_digest(args.artifact, expected_algo)
            expected_source = {"artifact": args.artifact, "algo": expected_algo}
        elif args.expected_digest:
            expected_algo, expected_hex = normalize_digest(args.expected_digest)
            expected_source = {"expected_digest": args.expected_digest}
        else:
            raise ValueError("Provide either --expected-digest or --artifact")
    except Exception as e:
        evidence = {
            "schemaVersion": SCHEMA_VERSION,
            "tool": TOOL_NAME,
            "timestamp": utc_now(),
            "result": "INCONCLUSIVE",
            "error": str(e),
        }
        print(json.dumps(evidence, indent=2))
        if args.output:
            Path(args.output).write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
        sys.exit(2)

    # Load provenance
    try:
        stmt = load_json(args.provenance)
    except Exception as e:
        evidence = {
            "schemaVersion": SCHEMA_VERSION,
            "tool": TOOL_NAME,
            "timestamp": utc_now(),
            "result": "INCONCLUSIVE",
            "expected": {expected_algo: expected_hex},
            "expectedSource": expected_source,
            "error": f"Failed to load provenance: {e}",
        }
        print(json.dumps(evidence, indent=2))
        if args.output:
            Path(args.output).write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
        sys.exit(2)

    subjects = extract_subject_digests(stmt)
    result, details = verdict(expected_algo, expected_hex, subjects)

    evidence = {
        "schemaVersion": SCHEMA_VERSION,
        "tool": TOOL_NAME,
        "timestamp": utc_now(),
        "result": result,
        "expected": {expected_algo: expected_hex},
        "expectedSource": expected_source,
        "provenance": {"path": args.provenance},
        "subjects": subjects,
        "details": details,
    }

    print(json.dumps(evidence, indent=2))

    if args.output:
        Path(args.output).write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")

    if result == "PASS":
        sys.exit(0)
    elif result == "FAIL":
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()

