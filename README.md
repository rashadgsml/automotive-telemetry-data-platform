# Automotive Telemetry Data Platform

A containerized data engineering project that ingests, validates, stores, and transforms synthetic vehicle telemetry data. It demonstrates data quality checks, analytical modelling, workflow orchestration, and REST API development using Python and modern data engineering tools.

**Dataset:** Synthetic vehicle telemetry data; not sourced from BMW or any other vehicle manufacturer.

## Overview

The platform ingests vehicle sensor records from CSV and JSON files, validates them, stores valid records in PostgreSQL, and exposes telemetry history and analytical results through FastAPI.

Apache Airflow orchestrates database connectivity checks, telemetry quality checks, dbt transformations, and dbt tests. The analytics layer includes staging and daily vehicle metrics models.

## Architecture

```text
          Synthetic CSV / JSON Data
                     |
                     v
          Python Ingestion & Validation
                     |
                     v
                 PostgreSQL
                  /       \
                 v         v
           FastAPI API   Apache Airflow
                            |
                            v
                     Database Checks
                            |
                            v
                      Quality Checks
                            |
                            v
                         dbt run
                            |
                            v
                        dbt test
                            |
                            v
                  Analytics Models
```

## Key Features

- **Data ingestion:** Read telemetry records from CSV and JSON files.
- **Data validation:** Check required fields, duplicate records, timestamp validity, and sensor-value ranges.
- **Reliable database writes:** Persist valid records in PostgreSQL and avoid duplicate inserts when reprocessing existing data.
- **Ingestion tracking:** Record run metadata, including record counts and rejected records.
- **Analytics modelling:** Use dbt to create staging and daily vehicle metrics models.
- **Data quality testing:** Combine application tests, dbt schema tests, and SQL-based data quality assertions.
- **Workflow orchestration:** Use Apache Airflow to orchestrate database checks, quality checks, dbt runs, and dbt tests.
- **REST API:** Expose vehicle telemetry history and analytics through FastAPI.
- **Containerization:** Run the API, PostgreSQL, and Airflow using Docker Compose.

## Technology Stack

| Area | Technologies |
|---|---|
| Programming | Python, SQL |
| Database | PostgreSQL |
| API | FastAPI |
| Analytics engineering | dbt Core, dbt-postgres |
| Orchestration | Apache Airflow |
| Testing | pytest, dbt tests |
| Infrastructure | Docker, Docker Compose |

## Getting Started

### Prerequisites

- Git
- Docker Desktop
- Python and a virtual environment for local development and testing
- dbt Core and dbt-postgres for running dbt locally

### 1. Clone the repository

```bash
git clone https://github.com/rashadgsml/automotive-telemetry-data-platform.git
cd automotive-telemetry-data-platform
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Review the local development values in `.env`. Never commit real credentials or secrets.

### 3. Start PostgreSQL and the API

From the project root:

```bash
docker compose --env-file .env up -d --build
```

### 4. Start Airflow

```bash
docker compose --env-file .env -f airflow/compose.yaml up -d --build
```

### 5. Access the services

| Service | URL |
|---|---|
| FastAPI | http://localhost:8000 |
| Interactive API documentation | http://localhost:8000/docs |
| Airflow UI | http://localhost:8080 |

Use the Airflow credentials configured for your local environment. Do not use development credentials in a publicly deployed environment.

### 6. Run application tests

Activate the project's virtual environment, then run:

```bash
pytest
```

### 7. Run dbt locally

Ensure the local dbt profile in `~/.dbt/profiles.yml` points to the correct PostgreSQL host, port, database, and credentials.

```bash
dbt debug --project-dir telemetry_analytics --profiles-dir "$HOME/.dbt"
dbt run --project-dir telemetry_analytics --profiles-dir "$HOME/.dbt"
dbt test --project-dir telemetry_analytics --profiles-dir "$HOME/.dbt"
```

The Airflow containers use their own dbt profile and database connection configuration.

## Analytics

The daily vehicle metrics model calculates measures such as:

- Total telemetry readings per vehicle and day
- Average and maximum recorded speed
- Maximum engine temperature
- Minimum battery voltage and fuel level
- Starting and ending odometer readings
- Estimated daily distance based on the difference between the maximum and minimum odometer readings

The distance metric is an estimate derived from recorded odometer values, not a separate measurement of distance travelled.


## Example API Response

Request:

```http
GET /analytics/vehicles
```

Example response (abridged):

```json
{
  "vehicles": [
    {
      "vehicle_id": "VH-1001",
      "record_count": 24,
      "average_speed_kmh": 67.93,
      "average_engine_temp_c": 89.41,
      "max_speed_kmh": 128.6
    },
    {
      "vehicle_id": "VH-1002",
      "record_count": 24,
      "average_speed_kmh": 62.85,
      "average_engine_temp_c": 89.36,
      "max_speed_kmh": 129.4
    },
    {
      "vehicle_id": "VH-1003",
      "record_count": 24,
      "average_speed_kmh": 86.93,
      "average_engine_temp_c": 89.7,
      "max_speed_kmh": 129.5
    }
  ],
  "count": 3
}
```

The API also provides individual vehicle telemetry history through `GET /vehicles/{vehicle_id}/telemetry`. Interactive endpoint documentation is available at `/docs`.

These figures are generated from synthetic telemetry data and demonstrate the API's analytical output, not real vehicle performance.


## Current Status

Implemented:

- CSV and JSON ingestion with validation
- PostgreSQL persistence and ingestion-run tracking
- Duplicate handling and rejected-record reporting
- FastAPI telemetry and analytics endpoints
- dbt staging and daily metrics models
- dbt schema tests and SQL-based assertions
- Airflow orchestration of database checks, quality checks, dbt execution, and tests
- Docker Compose configurations for the application and Airflow

## Future Improvements

- Incremental processing and late-arriving data handling
- Larger datasets and distributed processing with PySpark
- CI checks using GitHub Actions
- Additional monitoring, logging, and failure-recovery mechanisms
- Cloud deployment

## Purpose

This project demonstrates practical data engineering concepts through an end-to-end telemetry pipeline, combining ingestion, validation, SQL transformations, testing, orchestration, and API development. It is a portfolio project and a foundation for further improvements toward production-style data systems.
