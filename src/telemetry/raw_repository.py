
from typing import Any

from sqlalchemy.dialects.postgresql import insert

from telemetry.database import SessionLocal
from telemetry.raw_models import RawTelemetry


def save_raw_records(
    run_id: int,
    source_name: str,
    records: list[dict[str, Any]],
) -> int:
    """Store original input records for a specific ingestion run."""
    if not records:
        return 0

    rows = [
        {
            "ingestion_run_id": run_id,
            "source_name": source_name,
            "source_row_number": row_number,
            "raw_record": record,
        }
        for row_number, record in enumerate(records, start=1)
    ]

    statement = (
        insert(RawTelemetry)
        .values(rows)
        .on_conflict_do_nothing(
            constraint="unique_source_row_per_run"
        )
        .returning(RawTelemetry.id)
    )

    with SessionLocal.begin() as session:
        inserted_ids = session.scalars(statement).all()

    return len(inserted_ids)
