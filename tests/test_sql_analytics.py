
from sqlalchemy import text

from telemetry.database import SessionLocal


def test_daily_summary_has_expected_columns():
    with SessionLocal() as session:
        result = session.execute(
            text("SELECT * FROM vehicle_daily_summary LIMIT 1")
        )

        columns = result.keys()

    expected_columns = {
        "vehicle_id",
        "reading_date",
        "reading_count",
        "average_speed_kmh",
        "average_engine_temp_c",
        "max_speed_kmh",
        "average_fuel_level_pct",
        "latest_reading",
    }

    assert expected_columns.issubset(set(columns))


def test_daily_metrics_has_expected_columns():
    with SessionLocal() as session:
        result = session.execute(
            text("SELECT * FROM vehicle_daily_metrics LIMIT 1")
        )

        columns = result.keys()

    expected_columns = {
        "vehicle_id",
        "reading_date",
        "reading_count",
        "average_speed_kmh",
        "average_engine_temp_c",
        "max_speed_kmh",
        "min_fuel_level_pct",
        "average_battery_voltage_v",
    }

    assert expected_columns.issubset(set(columns))
