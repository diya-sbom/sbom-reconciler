import subprocess
import sys


def run(cmd):
    result = subprocess.run(cmd)
    return result.returncode


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 cli/diya.py verify")
        print("  python3 cli/diya.py record")
        print("  python3 cli/diya.py ledger-verify")
        return 1

    command = sys.argv[1]

    if command == "verify":
        return run(["python3", "cli/provenance_verify.py"])
    elif command == "record":
        return run(["python3", "cli/verification_record.py"])
    elif command == "ledger-verify":
        return run(["python3", "cli/verify_ledger.py", "ledger/ledger.jsonl"])
    else:
        print(f"Unknown command: {command}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
