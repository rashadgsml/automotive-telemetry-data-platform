
import json

from telemetry.data_quality import run_quality_checks


def main() -> None:
    results = run_quality_checks()
    print(json.dumps(results, indent=2))

    if not results["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
