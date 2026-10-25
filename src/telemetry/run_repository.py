
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import update

from telemetry.database import SessionLocal
from telemetry.run_models import IngestionRun


def create_run(source_name: str) -> int:
    """Create an ingestion run and return its ID."""
    run = IngestionRun(
        source_name=source_name,
        status="running",
        started_at=datetime.now(timezone.utc),
    )

    with SessionLocal.begin() as session:
        session.add(run)
        session.flush()
        run_id = run.id

    return run_id


def finish_run(
    run_id: int,
    report: dict[str, Any],
    inserted_count: int,
) -> None:
    """Mark a run successful and save its record counts."""
    statement = (
        update(IngestionRun)
        .where(IngestionRun.id == run_id)
        .values(
            status="success",
            total_records=report["total_records"],
            valid_records=report["accepted_count"],
            inserted_count=inserted_count,
            rejected_count=report["rejected_count"],
            finished_at=datetime.now(timezone.utc),
            error_message=None,
        )
    )

    with SessionLocal.begin() as session:
        session.execute(statement)



def fail_run(run_id: int, error_message: str) -> None:
    """Mark an ingestion run as failed."""
    statement = (
        update(IngestionRun)
        .where(IngestionRun.id == run_id)
        .values(
            status="failed",
            finished_at=datetime.now(timezone.utc),
            error_message=error_message[:4000],
        )
    )

    with SessionLocal.begin() as session:
        session.execute(statement)
