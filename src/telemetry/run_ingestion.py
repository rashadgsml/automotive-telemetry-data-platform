
import json
import sys
from pathlib import Path

from sqlalchemy.exc import SQLAlchemyError

from telemetry.raw_repository import save_raw_records
from telemetry.ingestion import ingest_file, load_records
from telemetry.repository import save_records
from telemetry.run_repository import (
    create_run,
    fail_run,
    finish_run,
)


def main() -> None:
    if len(sys.argv) != 2:
        print(
            "Usage: python -m telemetry.run_ingestion <file_path>"
        )
        raise SystemExit(1)

    file_path = Path(sys.argv[1])

    if not file_path.is_file():
        print(f"Ingestion failed: File not found: {file_path}")
        raise SystemExit(1)

    try:
        run_id = create_run(file_path.name)
    except SQLAlchemyError as error:
        print(f"Could not create ingestion run: {error}")
        raise SystemExit(1) from error


    try:
        raw_records = load_records(file_path)

        raw_inserted_count = save_raw_records(
            run_id=run_id,
            source_name=file_path.name,
            records=raw_records,
        )
        report = ingest_file(file_path)
        inserted_count = save_records(report["accepted"])

        finish_run(
            run_id=run_id,
            report=report,
            inserted_count=inserted_count,
        )

    except (OSError, ValueError, SQLAlchemyError) as error:
        try:
            fail_run(run_id, str(error))
        except SQLAlchemyError as tracking_error:
            print(f"Could not record ingestion failure: {tracking_error}")

        print(f"Ingestion failed for run {run_id}: {error}")
        raise SystemExit(1) from error


    summary = {
        "run_id": run_id,
        "source": report["source"],
        "status": "success",
        "total_records": report["total_records"],
        "valid_records": report["accepted_count"],
        "inserted_count": inserted_count,
        "already_present_count": (
            report["accepted_count"] - inserted_count
        ),
        "rejected_count": report["rejected_count"],
    }

    print(json.dumps(summary, indent=2))

    if report["rejected"]:
        print("\nRejected records:")
        print(json.dumps(report["rejected"], indent=2))


if __name__ == "__main__":
    main()
