import json
from pathlib import Path

def check_licenses(sbom_path, policy_path):
    sbom = json.loads(Path(sbom_path).read_text(encoding="utf-8"))
    policy = json.loads(Path(policy_path).read_text(encoding="utf-8"))

    allowed = set(policy.get("allowed_licenses", []))

    violations = []

    for pkg in sbom.get("packages", []):
        lic = pkg.get("licenseConcluded") or pkg.get("licenseDeclared")

        if lic and lic not in allowed:
            violations.append({
                "package": pkg.get("name"),
                "license": lic
            })

    if violations:
        return {
            "result": "FAIL",
            "violations": violations
        }

    return {
        "result": "PASS"
    }
