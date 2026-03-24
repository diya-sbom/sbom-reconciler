#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


def load_json(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def _identity_from_purl_or_name(purl: str, name: str) -> str:
    purl = (purl or "").strip()
    name = (name or "").strip()

    # If purl has a version suffix like "...@1.2.3", drop the version (identity only)
    if purl and "@" in purl:
        return purl.split("@", 1)[0]
    return purl or name


def normalize_packages(sbom_doc: dict) -> dict:
    """
    Returns: {identity: version_or_empty}
    Supports: CycloneDX (components), SPDX (packages)
    """
    out: dict[str, str] = {}

    # CycloneDX JSON
    comps = sbom_doc.get("components")
    if isinstance(comps, list):
        for c in comps:
            if not isinstance(c, dict):
                continue
            name = (c.get("name") or "").strip()
            version = (c.get("version") or "").strip()
            purl = (c.get("purl") or "").strip()
            ident = _identity_from_purl_or_name(purl, name)
            if ident:
                out[ident] = version
        return out

    # SPDX JSON
    pkgs = sbom_doc.get("packages")
    if isinstance(pkgs, list):
        for p in pkgs:
            if not isinstance(p, dict):
                continue
            name = (p.get("name") or "").strip()
            version = (p.get("versionInfo") or "").strip()

            # Try to extract purl from externalRefs if present
            ident = name
            ext = p.get("externalRefs") or []
            if isinstance(ext, list):
                for ref in ext:
                    if not isinstance(ref, dict):
                        continue
                    if ref.get("referenceType") == "purl":
                        loc = (ref.get("referenceLocator") or "").strip()
                        ident = _identity_from_purl_or_name(loc, name)
                        break

            if ident:
                out[ident] = version
        return out

    return out


def diff_sboms(a: dict, b: dict) -> dict:
    """
    Compare two SBOM docs.
    Output:
      {
        "added":   [identity...],
        "removed": [identity...],
        "changed": [{"package": identity, "from": "x", "to": "y"}...]
      }
    """
    A = normalize_packages(a)
    B = normalize_packages(b)

    a_keys = set(A.keys())
    b_keys = set(B.keys())

    added = sorted(b_keys - a_keys)
    removed = sorted(a_keys - b_keys)

    changed = []
    for k in sorted(a_keys & b_keys):
        if (A.get(k) or "") != (B.get(k) or ""):
            changed.append({"package": k, "from": A.get(k, ""), "to": B.get(k, "")})

    return {"added": added, "removed": removed, "changed": changed}


def main() -> None:
    ap = argparse.ArgumentParser(description="Diff two SBOM JSON files (CycloneDX or SPDX).")
    ap.add_argument("a", help="SBOM A (baseline)")
    ap.add_argument("b", help="SBOM B (new)")
    ap.add_argument("-o", "--output", help="Write JSON report to this file (also prints to stdout).")
    ap.add_argument(
        "--fail-on-change",
        action="store_true",
        help="Exit 1 if any added/removed/changed entries exist (CI mode).",
    )
    args = ap.parse_args()

    a_doc = load_json(args.a)
    b_doc = load_json(args.b)

    report = diff_sboms(a_doc, b_doc)

    # Always print
    print(json.dumps(report, indent=2))

    # Optional file output
    if args.output:
        Path(args.output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

     
    # CI exit code
    has_add_remove = bool(report["added"] or report["removed"])
    has_change = bool(report["changed"])

    if args.fail_on_change and (has_add_remove or has_change):
        print("\nVERDICT: FAIL")
        sys.exit(1)
    else:
        print("\nVERDICT: PASS")
        sys.exit(0)


if __name__ == "__main__":
    sys.exit (main())



 

