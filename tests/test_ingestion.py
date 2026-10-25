
import json

from telemetry.generate_data import generate_records
from telemetry.ingestion import ingest_file, load_records


def test_load_csv(tmp_path):
    records = generate_records(1)
    path = tmp_path / "telemetry.csv"

    import csv

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    loaded = load_records(path)

    assert len(loaded) == 3
    assert loaded[0]["vehicle_id"] == "VH-1001"


def test_load_json(tmp_path):
    records = generate_records(1)
    path = tmp_path / "telemetry.json"
    path.write_text(json.dumps(records), encoding="utf-8")

    loaded = load_records(path)

    assert len(loaded) == 3


def test_unsupported_file_format(tmp_path):
    path = tmp_path / "telemetry.txt"
    path.write_text("some data", encoding="utf-8")

    try:
        load_records(path)
        assert False, "Expected ValueError"
    except ValueError as error:
        assert "Unsupported file format" in str(error)


def test_ingest_file_reports_duplicates(tmp_path):
    records = generate_records(1)
    records.append(dict(records[0]))

    path = tmp_path / "telemetry.json"
    path.write_text(json.dumps(records), encoding="utf-8")

    report = ingest_file(path)

    assert report["total_records"] == 4
    assert report["accepted_count"] == 3
    assert report["rejected_count"] == 1
    assert "Duplicate" in report["rejected"][0]["errors"][0]
