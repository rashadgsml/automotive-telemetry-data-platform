
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Float, Identity, String
from sqlalchemy.orm import Mapped, mapped_column

from telemetry.database import Base


class Telemetry(Base):
    __tablename__ = "telemetry"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )
    vehicle_id: Mapped[str] = mapped_column(String(50), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    speed_kmh: Mapped[float] = mapped_column(Float, nullable=False)
    engine_temp_c: Mapped[float] = mapped_column(Float, nullable=False)
    battery_voltage_v: Mapped[float] = mapped_column(Float, nullable=False)
    fuel_level_pct: Mapped[float] = mapped_column(Float, nullable=False)
    odometer_km: Mapped[float] = mapped_column(Float, nullable=False)
