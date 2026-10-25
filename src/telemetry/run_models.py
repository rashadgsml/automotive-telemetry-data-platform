
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    Integer,
    String,
    Text,
    Identity,
)
from sqlalchemy.orm import Mapped, mapped_column

from telemetry.database import Base


class IngestionRun(Base):
    __tablename__ = "ingestion_runs"

    __table_args__ = (
        CheckConstraint(
            "status IN ('running', 'success', 'failed')",
            name="check_ingestion_run_status",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )
    source_name: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False
    )
    total_records: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    valid_records: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    inserted_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    rejected_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    error_message: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )
