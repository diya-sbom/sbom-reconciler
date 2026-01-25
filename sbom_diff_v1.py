import json
import sys
from pathlib import Path


def load_json(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def normalize_packages(sbom: dict) -> dict:
    """
    Returns: {package_identity: version}
    Supports: CycloneDX (components), SPDX (packages)
    """
    out = {}

    # CycloneDX JSON
    if isinstance(sbom, dict) and "components" in sbom and isinstance(sbom["components"], list):
        for c in sbom["components"]:
            if not isinstance(c, dict):
                continue

            name = (c.get("name") or "").strip()
            version = (c.get("version") or "").strip()
            purl = (c.get("purl") or "").strip()

            # Identity WITHOUT version (so version bumps become "changed")
            if purl and "@" in purl:
                identity = purl.split("@")[0]
            else:
                identity = name

            if identity:
                out[identity] = version

        return out

    # SPDX JSON
    if isinstance(sbom, dict) and "packages" in sbom and isinstance(sbom["packages"], list):
        for p in sbom["packages"]:
            if not isinstance(p, dict):
                continue

            name = (p.get("name") or "").strip()
            version = (p.get("versionInfo") or "").strip()
            spdxid = (p.get("SPDXID") or "").strip()
            identity = name or spdxid

            if identity:
                out[identity] = version

        return out

    raise ValueError("Unrecognized SBOM format")


def diff(a: dict, b: dict) -> dict:
    a_keys = set(a.keys())
    b_keys = set(b.keys())

    added = sorted(b_keys - a_keys)
    removed = sorted(a_keys - b_keys)

    changed = []
    for k in sorted(a_keys & b_keys):
        if (a.get(k) or "") != (b.get(k) or ""):
            changed.append({"package": k, "from": a.get(k, ""), "to": b.get(k, "")})

    return {"added": added, "removed": removed, "changed": changed}


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 sbom_diff.py <sbom_A.json> <sbom_B.json>")
        sys.exit(2)

    sbom_a = load_json(sys.argv[1])
    sbom_b = load_json(sys.argv[2])

    a = normalize_packages(sbom_a)
    b = normalize_packages(sbom_b)

    print(json.dumps(diff(a, b), indent=2))


if __name__ == "__main__":
    main()
