
from datetime import datetime, timezone

import psycopg2
from airflow import DAG
from airflow.operators.python import PythonOperator


DB_CONFIG = {
    "host": "db",
    "port": 5432,
    "dbname": "telemetry_db",
    "user": "telemetry_user",
    "password": "local_dev_password",
}


def check_database_connection():
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM telemetry;")
            count = cur.fetchone()[0]

    print(f"Database connection successful. Telemetry records: {count}")

    if count == 0:
        raise ValueError("Telemetry table is empty.")


def check_telemetry_quality():
    query = """
        SELECT COUNT(*)
        FROM telemetry
        WHERE vehicle_id IS NULL
           OR timestamp IS NULL
           OR speed_kmh < 0
           OR speed_kmh > 250
           OR engine_temp_c < -40
           OR engine_temp_c > 200
           OR battery_voltage_v < 0
           OR battery_voltage_v > 20
           OR fuel_level_pct < 0
           OR fuel_level_pct > 100
           OR odometer_km < 0;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            invalid_count = cur.fetchone()[0]

    print(f"Invalid telemetry records: {invalid_count}")

    if invalid_count > 0:
        raise ValueError(
            f"Data-quality check failed: {invalid_count} invalid records."
        )


with DAG(
    dag_id="telemetry_quality_pipeline",
    description="Check telemetry database connectivity and data quality",
    start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
    schedule=None,
    catchup=False,
    tags=["telemetry", "data-quality"],
) as dag:

    database_check = PythonOperator(
        task_id="check_database_connection",
        python_callable=check_database_connection,
    )

    quality_check = PythonOperator(
        task_id="check_telemetry_quality",
        python_callable=check_telemetry_quality,
    )

    database_check >> quality_check
