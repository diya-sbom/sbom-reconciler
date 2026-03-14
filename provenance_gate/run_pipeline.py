import subprocess
import sys


def run(cmd):
    print(f"\n>>> {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main():
    artifact = "artifact.txt"
    attestation = "attest/attestation.json"
    ledger_file = "ledger/ledger.jsonl"

    run([
        "python3", "-m", "engine.gate",
        "--artifact", artifact,
        "--attestation", attestation
    ])

    run([
        "python3", "cli/export_evidence.py"
    ])

    run([
        "python3", "cli/write_ledger.py",
        "evidence/gate_result.json"
    ])

    run([
        "python3", "cli/verify_ledger.py",
        ledger_file
    ])

    print("\nPIPELINE PASS")


if __name__ == "__main__":
    main()
