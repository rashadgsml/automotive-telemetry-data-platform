
from sqlalchemy import select

from telemetry.database import SessionLocal
from telemetry.run_models import IngestionRun
from telemetry.run_repository import create_run, fail_run


def test_failed_run_is_recorded():
    run_id = create_run("test_failure.csv")

    try:
        fail_run(run_id, "Simulated ingestion failure")

        with SessionLocal() as session:
            run = session.scalar(
                select(IngestionRun).where(
                    IngestionRun.id == run_id
                )
            )

            assert run is not None
            assert run.status == "failed"
            assert run.error_message == "Simulated ingestion failure"
            assert run.finished_at is not None
    finally:
        with SessionLocal.begin() as session:
            session.query(IngestionRun).filter_by(
                id=run_id
            ).delete()
