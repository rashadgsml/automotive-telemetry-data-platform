
from sqlalchemy import func, select

from telemetry.database import SessionLocal
from telemetry.models import Telemetry


def run_quality_checks() -> dict:
    """Run basic quality checks on clean telemetry data."""

    checks = {}

    with SessionLocal() as session:
        missing_values = session.scalar(
            select(func.count())
            .select_from(Telemetry)
            .where(
                Telemetry.vehicle_id.is_(None)
                | Telemetry.timestamp.is_(None)
                | Telemetry.speed_kmh.is_(None)
                | Telemetry.engine_temp_c.is_(None)
                | Telemetry.battery_voltage_v.is_(None)
                | Telemetry.fuel_level_pct.is_(None)
                | Telemetry.odometer_km.is_(None)
            )
        )

        invalid_sensors = session.scalar(
            select(func.count())
            .select_from(Telemetry)
            .where(
                (Telemetry.speed_kmh < 0)
                | (Telemetry.speed_kmh > 250)
                | (Telemetry.engine_temp_c < -40)
                | (Telemetry.engine_temp_c > 200)
                | (Telemetry.battery_voltage_v < 0)
                | (Telemetry.battery_voltage_v > 20)
                | (Telemetry.fuel_level_pct < 0)
                | (Telemetry.fuel_level_pct > 100)
                | (Telemetry.odometer_km < 0)
            )
        )

        total_records = session.scalar(
            select(func.count()).select_from(Telemetry)
        )

    checks["total_records"] = total_records
    checks["missing_values"] = missing_values
    checks["invalid_sensor_records"] = invalid_sensors
    checks["passed"] = missing_values == 0 and invalid_sensors == 0

    return checks
