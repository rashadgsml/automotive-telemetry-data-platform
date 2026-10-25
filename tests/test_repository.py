
from sqlalchemy import delete

from telemetry.database import SessionLocal
from telemetry.models import Telemetry
from telemetry.repository import get_records_for_vehicle, save_records
from telemetry.generate_data import generate_records

from datetime import datetime

def cleanup(records):
    with SessionLocal.begin() as session:
        for record in records:
            timestamp = datetime.fromisoformat(
                record["timestamp"].replace("Z", "+00:00")
            )

            session.execute(
                delete(Telemetry).where(
                    Telemetry.vehicle_id == record["vehicle_id"],
                    Telemetry.timestamp == timestamp,
                )
            )



def test_save_records_and_skip_duplicates():
    records = generate_records(1)

    # Use isolated IDs so the test cannot affect development data.
    for record in records:
        record["vehicle_id"] = f"TEST-{record['vehicle_id']}"

    cleanup(records)

    try:
        inserted = save_records(records)
        inserted_again = save_records(records)

        assert inserted == 3
        assert inserted_again == 0

        saved = get_records_for_vehicle("TEST-VH-1001")
        assert len(saved) == 1
        assert saved[0].vehicle_id == "TEST-VH-1001"
    finally:
        cleanup(records)

