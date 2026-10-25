
from datetime import datetime
from typing import Any


REQUIRED_FIELDS = {
    "vehicle_id",
    "timestamp",
    "speed_kmh",
    "engine_temp_c",
    "battery_voltage_v",
    "fuel_level_pct",
    "odometer_km",
}

NUMERIC_RANGES = {
    "speed_kmh": (0, 250),
    "engine_temp_c": (-40, 200),
    "battery_voltage_v": (0, 20),
    "fuel_level_pct": (0, 100),
    "odometer_km": (0, float("inf")),
}


def validate_record(record: dict[str, Any]) -> list[str]:
    """Return validation errors. An empty list means the record is valid."""
    errors = []

    missing_fields = REQUIRED_FIELDS - record.keys()
    for field in sorted(missing_fields):
        errors.append(f"Missing required field: {field}")

    for field in sorted(REQUIRED_FIELDS & record.keys()):
        value = record[field]

        if value is None or value == "":
            errors.append(f"{field} cannot be empty")

    if errors:
        # Avoid type and parsing errors when required data is missing.
        return errors

    vehicle_id = record["vehicle_id"]
    if not isinstance(vehicle_id, str) or not vehicle_id.strip():
        errors.append("vehicle_id must be a non-empty string")

    try:
        timestamp = datetime.fromisoformat(
            record["timestamp"].replace("Z", "+00:00")
        )
        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            errors.append("timestamp must include a timezone")
    except (ValueError, AttributeError):
        errors.append("timestamp must be a valid ISO 8601 datetime")

    for field, (minimum, maximum) in NUMERIC_RANGES.items():
        value = record[field]

        # bool is a subclass of int in Python, but is not a valid reading.
        if isinstance(value, bool):
            errors.append(f"{field} must be numeric, not boolean")
            continue

        try:
            numeric_value = float(value)
        except (ValueError, TypeError):
            errors.append(f"{field} must be numeric")
            continue

        if not minimum <= numeric_value <= maximum:
            errors.append(
                f"{field} must be between {minimum} and {maximum}"
            )

    return errors


def find_duplicates(
    records: list[dict[str, Any]],
) -> set[int]:
    """Return indexes of repeated vehicle/timestamp pairs after first occurrence."""
    seen = set()
    duplicate_indexes = set()

    for index, record in enumerate(records):
        key = (record.get("vehicle_id"), record.get("timestamp"))

        if key in seen:
            duplicate_indexes.add(index)
        else:
            seen.add(key)

    return duplicate_indexes
