# Automotive Telemetry Data Platform

A containerized data engineering project that ingests, validates, stores, and transforms synthetic vehicle telemetry data. Built to explore reliable data pipelines, data quality checks, analytics modelling, and orchestration using Python and modern data engineering tools.

## Overview

The platform processes vehicle sensor records, validates incoming data, stores telemetry in PostgreSQL, and exposes vehicle history and analytics through a FastAPI service. It also includes an Apache Airflow pipeline for database and data quality checks, alongside dbt models and tests for analytical transformations.

The dataset is synthetic and is not sourced from any vehicle manufacturer.

## Architecture

```text
Synthetic CSV / JSON Data
          |
          v
Python Ingestion & Validation
          |
          v
      PostgreSQL
          |
          +--------------------+
          |                    |
          v                    v
     FastAPI API          Apache Airflow
                               |
                               v
                     Database & Quality Checks

PostgreSQL --> dbt Models --> Data Quality Tests
```

## Key Features

- **Data ingestion:** Read telemetry records from CSV and JSON files.
- **Data validation:** Detect missing fields, duplicate records, invalid sensor values, and invalid timestamps.
- **Reliable database writes:** Store valid records in PostgreSQL and avoid duplicate inserts when processing the same dataset again.
- **Ingestion tracking:** Record ingestion-run metadata, including record counts and rejected records.
- **Analytics modelling:** Use dbt to create staging models and test data constraints.
- **Automated checks:** Use pytest for application tests and Airflow to orchestrate database connectivity and telemetry quality checks.
- **REST API:** Expose vehicle telemetry history and analytical endpoints through FastAPI.
- **Containerization:** Run the API, PostgreSQL, and Airflow services using Docker Compose.

## Technology Stack

- Python
- SQL and PostgreSQL
- Apache Airflow
- dbt Core and dbt-postgres
- FastAPI
- Docker and Docker Compose
- pytest

## Getting Started

### Prerequisites

- Docker Desktop
- Git
- Python 3.13+ for local development

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd "Automotive Telemetry Data Platform"
```

### 2. Configure environment variables

Create your local `.env` file using the example:

```bash
cp .env.example .env
```

Review the values in `.env` before starting the services. Use local development credentials only, and do not commit `.env` to Git.

### 3. Start the application and database

From the project root:

```bash
docker compose --env-file .env up -d --build
```

### 4. Start Airflow

From the project root, in a separate terminal:

```bash
docker compose --env-file .env -f airflow/compose.yaml up -d --build
```

Airflow's web interface is available at:

`http://localhost:8080`

The API is available at:

`http://localhost:8000`

Interactive API documentation:

`http://localhost:8000/docs`

### 5. Run the tests

Run the project's automated tests using the configured Python environment:

```bash
pytest
```

### 6. Run dbt

With the telemetry database running and the local dbt profile configured:

```bash
dbt debug --project-dir telemetry_analytics
dbt run --project-dir telemetry_analytics
dbt test --project-dir telemetry_analytics
```

The dbt profile must point to the correct PostgreSQL host, port, database, and credentials for your execution environment.

## Data Quality and Analytics

The project includes checks for required fields, sensor-value ranges, duplicate records, and timestamp validity. dbt adds tests for model uniqueness, non-null fields, and sensor constraints.

The staging model provides a cleaned and consistently named representation of telemetry data for downstream analytics. SQL views support daily vehicle summaries and metrics.

## Current Status

Implemented:
- Python ingestion and validation
- PostgreSQL persistence and ingestion-run tracking
- FastAPI endpoints for telemetry and analytics
- Docker Compose setup for the API and database
- Airflow database and telemetry quality checks
- dbt staging model and data quality tests

Next improvements:
- Integrate dbt execution into the Airflow DAG
- Add intermediate and analytics-ready dbt models
- Introduce incremental processing for larger datasets
- Add pipeline logging, failure handling, and monitoring
- Add CI checks through GitHub Actions

## Purpose

This project demonstrates practical work with data ingestion, SQL transformations, validation, testing, orchestration, and containerized services. It is designed as a foundation for further development toward production-style data engineering pipelines.
