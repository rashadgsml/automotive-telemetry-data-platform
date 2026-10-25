
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Identity,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from telemetry.database import Base


class RawTelemetry(Base):
    __tablename__ = "raw_telemetry"

    __table_args__ = (
        UniqueConstraint(
            "ingestion_run_id",
            "source_row_number",
            name="unique_source_row_per_run",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )
    ingestion_run_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("ingestion_runs.id"),
        nullable=False,
    )
    source_name: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    source_row_number: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    raw_record: Mapped[dict] = mapped_column(
        JSONB, nullable=False
    )
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
