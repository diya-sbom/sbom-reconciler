import subprocess
import sys


def run(cmd):
    print(f"\n▶ running: {' '.join(cmd)}\n")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main():
    print("\n=== PROVENANCE VERIFY ===\n")

    run(["python3", "cli/verification_record.py"])
    run(["python3", "cli/write_ledger.py", "evidence/gate_result.json"])
    run(["python3", "cli/verify_ledger.py", "ledger/ledger.jsonl"])

    print("\n✔ provenance verification completed\n")


if __name__ == "__main__":
    main()

