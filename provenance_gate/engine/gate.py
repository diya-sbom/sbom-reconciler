import sys
import os
import argparse
import json
import subprocess
from pathlib import Path

from modules.loader import load_modules
from sbom.license_check import check_licenses
from attest.signature_check import sha256_file_hex


def write_json(path: str, payload: dict) -> None:
    Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--attestation", required=True)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    modules = load_modules()
    context = {
        "artifact": args.artifact
    }

    module_results = []
    for module in modules:
        r = module.run(context)
        module_results.append(r)

    digest_path = Path("artifact.sha256")

    if not digest_path.exists():
        payload = {
            "result": "FAIL",
            "error": "digest_file_not_found",
            "digest_file": str(digest_path),
            "modules": module_results
        }
        Path("evidence").mkdir(exist_ok=True)
        write_json("evidence/gate_result.json", payload)
        print(json.dumps(payload, indent=2))
        return 1

    expected_digest = digest_path.read_text(encoding="utf-8").strip()
    actual_digest = sha256_file_hex(Path(args.artifact))

    if actual_digest != expected_digest:
        payload = {
            "result": "FAIL",
            "error": "signature_digest_mismatch",
            "artifact": args.artifact,
            "expected_sha256": expected_digest,
            "actual_sha256": actual_digest,
            "modules": module_results
        }
        Path("evidence").mkdir(exist_ok=True)
        write_json("evidence/gate_result.json", payload)
        print(json.dumps(payload, indent=2))
        return 1

    cmd = [
        "python3",
        "attest/attestation_check.py",
        args.artifact,
        args.attestation,
    ]

    proc = subprocess.run(cmd, capture_output=True, text=True)

    out = proc.stdout.strip()
    err = proc.stderr.strip()
    code = proc.returncode

    Path("evidence").mkdir(exist_ok=True)

    if out:
        result = json.loads(out)
        result["modules"] = module_results
        result["signature_check"] = {
            "result": "PASS",
            "verified_sha256": actual_digest,
            "check": "artifact_signature"
        }

        lic_result = check_licenses(
            "sbom/example.spdx.json",
            "policy/license_policy.json"
        )

        if lic_result["result"] == "FAIL":
            result["license_policy"] = lic_result
            result["result"] = "FAIL"
            write_json("evidence/gate_result.json", result)
            print(json.dumps(result, indent=2))
            return 1

        if lic_result["result"] == "REQUIRE_APPROVAL":
            result["license_policy"] = lic_result
            result["result"] = "REQUIRE_APPROVAL"
            write_json("evidence/gate_result.json", result)
            print(json.dumps(result, indent=2))
            return 2

        result["license_policy"] = lic_result
        result["result"] = "PASS"

        write_json("evidence/decision.json", {
            "result": result.get("result"),
            "artifact": result.get("artifact")
        })

        write_json("evidence/modules.json", {
            "modules": result.get("modules", [])
        })

        write_json("evidence/signature.json", result.get("signature_check", {}))

        write_json("evidence/policy.json", {
            "license_policy": result.get("license_policy", {})
        })

        write_json("evidence/metadata.json", {
            "sha256": result.get("sha256"),
            "predicateType": result.get("predicateType"),
            "_type": result.get("_type"),
            "builder_id": result.get("builder_id"),
            "sbom_spdx_version": result.get("sbom_spdx_version"),
            "sbom_packages": result.get("sbom_packages")
        })

        write_json("evidence/gate_result.json", result)

        if args.quiet:
            print(result.get("result", "UNKNOWN"))
        else:
            print(json.dumps(result, indent=2))
    else:
        payload = {
            "result": "FAIL",
            "error": "checker_no_output",
            "modules": module_results
        }

        if err:
            payload["stderr"] = err

        write_json("evidence/gate_result.json", payload)
        print(json.dumps(payload, indent=2))

    return code if code in (0, 1, 2) else 2


if __name__ == "__main__":
    raise SystemExit(main())
