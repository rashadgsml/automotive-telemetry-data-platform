
from fastapi.testclient import TestClient

from telemetry.api import app
from telemetry.repository import get_records_for_vehicle
from telemetry.generate_data import generate_records
from telemetry.repository import save_records


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "database": "connected",
    }


def test_list_vehicles():
    records = generate_records(1)
    save_records(records)

    response = client.get("/vehicles")

    assert response.status_code == 200
    assert "VH-1001" in response.json()["vehicles"]


def test_get_vehicle_telemetry():
    records = generate_records(1)
    save_records(records)

    response = client.get(
        "/vehicles/VH-1001/telemetry?limit=10"
    )

    assert response.status_code == 200

    data = response.json()
    assert data["vehicle_id"] == "VH-1001"
    assert data["count"] >= 1
    assert "speed_kmh" in data["records"][0]


def test_missing_vehicle_returns_404():
    response = client.get(
        "/vehicles/UNKNOWN-999/telemetry"
    )

    assert response.status_code == 404


def test_limit_validation():
    response = client.get(
        "/vehicles/VH-1001/telemetry?limit=0"
    )

    assert response.status_code == 422
