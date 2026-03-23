import json
import sys


def load_components(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    components = data.get("components", [])
    return {
        (
            c.get("name", "").strip(),
            c.get("version", "").strip(),
        )
        for c in components
    }


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 src/sbom_diff.py <baseline> <current>")
        return 2

    baseline = load_components(sys.argv[1])
    current = load_components(sys.argv[2])

    added = sorted(current - baseline)
    removed = sorted(baseline - current)

    if added or removed:
        print("SBOM DRIFT DETECTED")

        if added:
            print("\nAdded:")
            for name, version in added:
                print(f"- {name} {version}")

        if removed:
            print("\nRemoved:")
            for name, version in removed:
                print(f"- {name} {version}")

        return 1

    print("SBOM OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
