
from fastapi import FastAPI, HTTPException, Query
from datetime import datetime

from telemetry.repository import get_records_for_vehicle
from telemetry.database import engine
from telemetry.models import Telemetry
from telemetry.database import SessionLocal
from telemetry.repository import get_records_in_time_range

from sqlalchemy import text, select
from sqlalchemy import func


app = FastAPI(
    title="Automotive Telemetry Data Platform",
    description="API for querying synthetic vehicle telemetry data.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    """Check whether the API and database are available."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        )


@app.get("/vehicles")
def list_vehicles():
    """Return the unique vehicle IDs present in the database."""
    statement = select(Telemetry.vehicle_id).distinct().order_by(
        Telemetry.vehicle_id
    )

    with SessionLocal() as session:
        vehicle_ids = session.scalars(statement).all()

    return {"vehicles": vehicle_ids, "count": len(vehicle_ids)}


@app.get("/vehicles/{vehicle_id}/telemetry")
def vehicle_telemetry(
    vehicle_id: str,
    limit: int = Query(default=100, ge=1, le=1000),
):
    """Return the latest telemetry records for a vehicle."""
    records = get_records_for_vehicle(vehicle_id, limit=limit)

    if not records:
        raise HTTPException(
            status_code=404,
            detail=f"No telemetry found for vehicle '{vehicle_id}'",
        )

    return {
        "vehicle_id": vehicle_id,
        "count": len(records),
        "records": [
            {
                "timestamp": record.timestamp.isoformat(),
                "speed_kmh": record.speed_kmh,
                "engine_temp_c": record.engine_temp_c,
                "battery_voltage_v": record.battery_voltage_v,
                "fuel_level_pct": record.fuel_level_pct,
                "odometer_km": record.odometer_km,
            }
            for record in records
        ],
    }



@app.get("/analytics/vehicles")
def vehicle_analytics():
    """Return aggregated telemetry statistics for each vehicle."""
    statement = (
        select(
            Telemetry.vehicle_id,
            func.count(Telemetry.id).label("record_count"),
            func.avg(Telemetry.speed_kmh).label("average_speed_kmh"),
            func.avg(Telemetry.engine_temp_c).label(
                "average_engine_temp_c"
            ),
            func.max(Telemetry.speed_kmh).label("max_speed_kmh"),
            func.max(Telemetry.timestamp).label("latest_reading"),
        )
        .group_by(Telemetry.vehicle_id)
        .order_by(Telemetry.vehicle_id)
    )

    with SessionLocal() as session:
        results = session.execute(statement).all()

    return {
        "vehicles": [
            {
                "vehicle_id": row.vehicle_id,
                "record_count": row.record_count,
                "average_speed_kmh": round(
                    float(row.average_speed_kmh), 2
                ),
                "average_engine_temp_c": round(
                    float(row.average_engine_temp_c), 2
                ),
                "max_speed_kmh": float(row.max_speed_kmh),
                "latest_reading": row.latest_reading.isoformat(),
            }
            for row in results
        ],
        "count": len(results),
    }



@app.get("/vehicles/{vehicle_id}/telemetry/range")
def vehicle_telemetry_range(
    vehicle_id: str,
    start_time: datetime,
    end_time: datetime,
    limit: int = Query(default=100, ge=1, le=1000),
):
    """Return telemetry within a specified time range."""
    if start_time >= end_time:
        raise HTTPException(
            status_code=400,
            detail="start_time must be earlier than end_time",
        )

    records = get_records_in_time_range(
        vehicle_id=vehicle_id,
        start_time=start_time,
        end_time=end_time,
        limit=limit,
    )

    return {
        "vehicle_id": vehicle_id,
        "count": len(records),
        "records": [
            {
                "timestamp": record.timestamp.isoformat(),
                "speed_kmh": record.speed_kmh,
                "engine_temp_c": record.engine_temp_c,
                "battery_voltage_v": record.battery_voltage_v,
                "fuel_level_pct": record.fuel_level_pct,
                "odometer_km": record.odometer_km,
            }
            for record in records
        ],
    }
