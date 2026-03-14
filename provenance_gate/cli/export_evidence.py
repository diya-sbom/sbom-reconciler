import hashlib
import json
from pathlib import Path


EVIDENCE_DIR = Path("evidence")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    if not EVIDENCE_DIR.exists():
        print("ERROR: evidence directory not found")
        return 1

    bundle = {
        "decision": read_json(EVIDENCE_DIR / "decision.json"),
        "modules": read_json(EVIDENCE_DIR / "modules.json"),
        "metadata": read_json(EVIDENCE_DIR / "metadata.json"),
        "policy": read_json(EVIDENCE_DIR / "policy.json"),
        "signature": read_json(EVIDENCE_DIR / "signature.json"),
        "gate_result": read_json(EVIDENCE_DIR / "gate_result.json"),
    }

    bundle_text = json.dumps(bundle, indent=2)
    bundle_hash = sha256_text(bundle_text)

    (EVIDENCE_DIR / "bundle.json").write_text(bundle_text, encoding="utf-8")
    (EVIDENCE_DIR / "bundle.sha256").write_text(bundle_hash + "\n", encoding="utf-8")

    print(json.dumps({
        "result": "PASS",
        "bundle": str(EVIDENCE_DIR / "bundle.json"),
        "bundle_sha256": bundle_hash
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
