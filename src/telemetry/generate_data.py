
import csv
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

random.seed(42)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

VEHICLES = ["VH-1001", "VH-1002", "VH-1003"]


def generate_records(records_per_vehicle: int = 24) -> list[dict]:
    """Generate reproducible synthetic vehicle telemetry."""
    records = []
    start = datetime(2026, 10, 20, tzinfo=timezone.utc)

    for vehicle_index, vehicle_id in enumerate(VEHICLES):
        for reading_index in range(records_per_vehicle):
            timestamp = start + timedelta(
                hours=reading_index,
                minutes=vehicle_index,
            )

            records.append(
                {
                    "vehicle_id": vehicle_id,
                    "timestamp": timestamp.isoformat().replace("+00:00", "Z"),
                    "speed_kmh": round(random.uniform(0, 130), 1),
                    "engine_temp_c": round(random.uniform(75, 105), 1),
                    "battery_voltage_v": round(random.uniform(11.8, 14.5), 2),
                    "fuel_level_pct": round(random.uniform(5, 100), 1),
                    "odometer_km": round(
                        25000 + vehicle_index * 500
                        + reading_index * random.uniform(0.1, 5),
                        1,
                    ),
                }
            )

    return records


def write_csv(records: list[dict], path: Path) -> None:
    if not records:
        return

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)


def write_json(records: list[dict], path: Path) -> None:
    with path.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=2)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    records = generate_records()

    write_csv(records, DATA_DIR / "telemetry.csv")
    write_json(records, DATA_DIR / "telemetry.json")

    invalid_records = [dict(record) for record in records[:4]]

    # One valid record
    invalid_records[0]["engine_temp_c"] = 90.0

    # Issue 1: Impossible speed
    invalid_records[1]["speed_kmh"] = 350

    # Issue 2: Duplicate vehicle and timestamp
    invalid_records[2] = dict(invalid_records[0])

    # Issue 3: Missing vehicle identifier
    invalid_records[3]["vehicle_id"] = ""

    write_csv(invalid_records, DATA_DIR / "telemetry_invalid.csv")

    print(f"Generated {len(records)} valid synthetic records.")
    print(f"Generated {len(invalid_records)} test records with data-quality issues.")
    print(f"Output directory: {DATA_DIR}")


if __name__ == "__main__":
    main()
