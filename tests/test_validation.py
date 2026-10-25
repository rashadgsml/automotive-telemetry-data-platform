
from telemetry.generate_data import generate_records
from telemetry.validation import find_duplicates, validate_record


def test_valid_record_passes():
    record = generate_records(1)[0]
    assert validate_record(record) == []


def test_missing_field_is_rejected():
    record = generate_records(1)[0]
    del record["vehicle_id"]

    errors = validate_record(record)

    assert any("Missing required field: vehicle_id" in e for e in errors)


def test_empty_sensor_value_is_rejected():
    record = generate_records(1)[0]
    record["engine_temp_c"] = ""

    errors = validate_record(record)

    assert any("engine_temp_c cannot be empty" in e for e in errors)


def test_out_of_range_speed_is_rejected():
    record = generate_records(1)[0]
    record["speed_kmh"] = 350

    errors = validate_record(record)

    assert any("speed_kmh must be between" in e for e in errors)


def test_timezone_is_required():
    record = generate_records(1)[0]
    record["timestamp"] = "2026-10-20T10:00:00"

    errors = validate_record(record)

    assert any("timestamp must include a timezone" in e for e in errors)


def test_duplicate_detection_keeps_first_occurrence():
    records = generate_records(2)
    records.append(dict(records[0]))
    
    duplicates = find_duplicates(records)

    assert duplicates == {6}
