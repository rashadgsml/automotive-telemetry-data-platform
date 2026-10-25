
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from telemetry.database import SessionLocal
from telemetry.models import Telemetry


def save_records(records: list[dict[str, Any]]) -> int:
    """Save valid records, skipping existing vehicle/timestamp pairs."""
    if not records:
        return 0

    prepared_records = []

    for record in records:
        timestamp = datetime.fromisoformat(
            record["timestamp"].replace("Z", "+00:00")
        )

        if timestamp.tzinfo is None:
            raise ValueError("Timestamp must include a timezone")

        prepared_records.append({
            **record,
            "timestamp": timestamp.astimezone(timezone.utc),
        })

    statement = (
        insert(Telemetry)
        .values(prepared_records)
        .on_conflict_do_nothing(
            constraint="unique_vehicle_timestamp"
        )
        .returning(Telemetry.id)
    )

    with SessionLocal.begin() as session:
        inserted_ids = session.scalars(statement).all()

    return len(inserted_ids)


def get_records_for_vehicle(
    vehicle_id: str,
    limit: int = 100,
) -> list[Telemetry]:
    """Return the most recent telemetry records for a vehicle."""
    if not 1 <= limit <= 1000:
        raise ValueError("limit must be between 1 and 1000")

    statement = (
        select(Telemetry)
        .where(Telemetry.vehicle_id == vehicle_id)
        .order_by(Telemetry.timestamp.desc())
        .limit(limit)
    )

    with SessionLocal() as session:
        return list(session.scalars(statement).all())



def get_records_in_time_range(
    vehicle_id: str,
    start_time: datetime,
    end_time: datetime,
    limit: int = 100,
) -> list[Telemetry]:
    """Return vehicle telemetry within a time range."""
    if start_time >= end_time:
        raise ValueError("start_time must be earlier than end_time")

    if not 1 <= limit <= 1000:
        raise ValueError("limit must be between 1 and 1000")

    statement = (
        select(Telemetry)
        .where(
            Telemetry.vehicle_id == vehicle_id,
            Telemetry.timestamp >= start_time,
            Telemetry.timestamp <= end_time,
        )
        .order_by(Telemetry.timestamp.desc())
        .limit(limit)
    )

    with SessionLocal() as session:
        return list(session.scalars(statement).all())
