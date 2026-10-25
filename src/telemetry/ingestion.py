
import csv
import json
from pathlib import Path
from typing import Any

from telemetry.validation import find_duplicates, validate_record


def load_records(file_path: str | Path) -> list[dict[str, Any]]:
    """Load telemetry records from a CSV or JSON file."""
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".csv":
        with path.open("r", newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))

    if suffix == ".json":
        with path.open("r", encoding="utf-8") as file:
            records = json.load(file)

        if not isinstance(records, list):
            raise ValueError("JSON input must contain a list of records")

        if not all(isinstance(record, dict) for record in records):
            raise ValueError("Every JSON record must be an object")

        return records

    raise ValueError(f"Unsupported file format: {suffix}")


def ingest_file(file_path: str | Path) -> dict[str, Any]:
    """Load, validate and classify telemetry records from a file."""
    records = load_records(file_path)
    duplicate_indexes = find_duplicates(records)

    accepted = []
    rejected = []

    for index, record in enumerate(records):
        errors = validate_record(record)

        if errors:
            rejected.append({
                "row": index + 1,
                "record": record,
                "errors": errors,
            })
        elif index in duplicate_indexes:
            rejected.append({
                "row": index + 1,
                "record": record,
                "errors": ["Duplicate vehicle/timestamp combination"],
            })
        else:
            accepted.append(record)

    return {
        "source": Path(file_path).name,
        "total_records": len(records),
        "accepted_count": len(accepted),
        "rejected_count": len(rejected),
        "accepted": accepted,
        "rejected": rejected,
    }
