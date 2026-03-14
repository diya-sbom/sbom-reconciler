import subprocess
import sys


def run(cmd):
    print(f"\n>>> {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)


def verify():
    run([
        "python3", "-m", "engine.gate",
        "--artifact", "artifact.txt",
        "--attestation", "attest/attestation.json"
    ])


def export_evidence():
    run(["python3", "cli/export_evidence.py"])


def write_ledger():
    run(["python3", "cli/write_ledger.py", "evidence/gate_result.json"])


def verify_ledger():
    run(["python3", "cli/verify_ledger.py", "ledger/ledger.jsonl"])


def pipeline():
    verify()
    export_evidence()
    write_ledger()
    verify_ledger()
    print("\nPIPELINE PASS")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 cli/provenance.py verify")
        print("  python3 cli/provenance.py evidence export")
        print("  python3 cli/provenance.py ledger write")
        print("  python3 cli/provenance.py ledger verify")
        print("  python3 cli/provenance.py pipeline")
        sys.exit(1)

    if sys.argv[1] == "verify":
        verify()
    elif sys.argv[1] == "pipeline":
        pipeline()
    elif len(sys.argv) >= 3 and sys.argv[1] == "evidence" and sys.argv[2] == "export":
        export_evidence()
    elif len(sys.argv) >= 3 and sys.argv[1] == "ledger" and sys.argv[2] == "write":
        write_ledger()
    elif len(sys.argv) >= 3 and sys.argv[1] == "ledger" and sys.argv[2] == "verify":
        verify_ledger()
    else:
        print("Unknown command")
        sys.exit(1)


if __name__ == "__main__":
    main()
