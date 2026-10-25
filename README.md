# Automotive Telemetry Data Platform

A data engineering project for ingesting, validating, storing, and analyzing synthetic automotive telemetry data. The platform combines Python-based ingestion, PostgreSQL storage, SQL analytics, and a FastAPI service, with dbt being integrated for modular data transformations.

## Project Overview

Modern vehicles generate telemetry data that can support fleet monitoring, operational analytics, and data quality management. This project demonstrates how to build a data pipeline that processes vehicle sensor readings and makes the resulting data available for analysis.

The platform currently supports CSV and JSON ingestion, record validation, duplicate handling, PostgreSQL persistence, ingestion run tracking, raw data storage, automated data quality checks, and SQL-based analytics.

**Note:** All vehicle telemetry data is synthetic and generated for this project. It is not real vehicle data or proprietary automotive data.

## Architecture

```text
Synthetic Telemetry Data
          |
          v
   CSV / JSON Files
          |
          v
  Python Ingestion Pipeline
          |
          +----> Raw Data Layer
          |      (PostgreSQL JSONB)
          |
          v
  Validation & Duplicate Handling
          |
          v
   Clean Telemetry Data
          |
          v
      PostgreSQL
          |
          +----> SQL Analytics Views
          |
          +----> dbt Staging Model
          |
          v
       FastAPI
          |
          v
  Telemetry & Analytics Endpoints
```

## Technology Stack

- **Python** — ingestion logic, validation, data processing, and application development
- **PostgreSQL** — relational storage, constraints, JSONB raw records, and analytics
- **SQLAlchemy** — database access and ORM models
- **FastAPI** — API endpoints for telemetry and vehicle analytics
- **dbt Core and dbt-postgres** — initial setup completed; staging model integration in progress
- **pytest** — automated tests
- **Git** — version control

## Implemented Features

### 1. Data Ingestion

- Load telemetry records from CSV and JSON files.
- Generate reproducible synthetic telemetry for multiple vehicles.
- Process input records through a Python ingestion pipeline.
- Produce ingestion summaries with record counts and rejection details.

### 2. Data Validation and Deduplication

- Validate required fields and timestamps.
- Check sensor readings against defined ranges.
- Identify duplicate vehicle and timestamp combinations.
- Use PostgreSQL uniqueness constraints to prevent duplicate telemetry records.
- Handle invalid records and report rejection details.

### 3. PostgreSQL Data Storage

- Store validated telemetry in a structured relational table.
- Store original input records in a raw data layer using PostgreSQL JSONB.
- Track ingestion runs, including status, record counts, timestamps, and error messages.
- Support repeatable ingestion without inserting duplicate clean records.

### 4. Data Quality Checks

- Detect missing values.
- Identify sensor values outside expected ranges.
- Return structured quality-check results.
- Exit with a non-zero status when quality checks fail.

### 5. SQL Analytics

Created PostgreSQL views for daily vehicle-level analytics, including:

- Daily telemetry record counts
- Average vehicle speed
- Average engine temperature
- Maximum recorded speed
- Average fuel level and minimum fuel level
- Average battery voltage
- Latest recorded telemetry timestamp

SQL tests verify that the analytics views expose their expected columns.

### 6. FastAPI Service

The application includes endpoints for health checks, vehicle discovery, vehicle telemetry history, and vehicle analytics.

### 7. dbt Integration — In Progress

- Installed dbt Core and the PostgreSQL adapter.
- Initialized the dbt project and verified the database connection.
- Created the initial `stg_telemetry.sql` staging model.
- Configured staging models to materialize as PostgreSQL views.

The dbt model execution and verification are the next integration steps.

## Project Structure

```text
Automotive Telemetry Data Platform/
├── data/
│   ├── telemetry.csv
│   ├── telemetry.json
│   └── telemetry_invalid.csv
├── sql/
│   ├── vehicle_daily_summary.sql
│   └── transformations/
│       └── vehicle_daily_metrics.sql
├── src/
│   └── telemetry/
│       ├── api.py
│       ├── database.py
│       ├── data_quality.py
│       ├── generate_data.py
│       ├── ingestion.py
│       ├── models.py
│       ├── raw_models.py
│       ├── raw_repository.py
│       ├── repository.py
│       ├── run_ingestion.py
│       ├── run_models.py
│       ├── run_quality_checks.py
│       ├── run_repository.py
│       └── validation.py
├── telemetry_analytics/
│   ├── models/
│   │   ├── example/
│   │   └── staging/
│   │       └── stg_telemetry.sql
│   └── dbt_project.yml
├── tests/
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.13
- PostgreSQL
- A virtual environment
- Git

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd "Automotive Telemetry Data Platform"
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

Install the project's Python dependencies using the project's dependency file, if available.

### 4. Configure PostgreSQL

Create a database named `telemetry_db` and configure the database connection through the `DATABASE_URL` environment variable when needed.

The default local connection used during development is:

```text
postgresql+psycopg://localhost/telemetry_db
```

The database schema must be initialized before running the pipeline.

### 5. Generate synthetic data

```bash
PYTHONPATH=src python -m telemetry.generate_data
```

### 6. Run ingestion

```bash
PYTHONPATH=src python -m telemetry.run_ingestion data/telemetry.csv
```

### 7. Run data quality checks

```bash
PYTHONPATH=src python -m telemetry.run_quality_checks
```

### 8. Run automated tests

```bash
PYTHONPATH=src pytest -q
```

### 9. Validate the dbt connection

```bash
dbt debug --project-dir telemetry_analytics
```

Once the staging model has been successfully built, run:

```bash
dbt run --project-dir telemetry_analytics
```

## Current Development Status

The core ingestion, validation, persistence, raw record tracking, data quality checks, SQL analytics views, and FastAPI functionality have been implemented and tested during development.

The dbt project has been initialized and its PostgreSQL connection validated. Full dbt model execution and integration remain in progress.

## Planned Improvements

- Complete dbt model execution and add schema and data tests.
- Introduce a more formal raw, staging, and analytics layer.
- Add incremental processing and stronger ingestion failure recovery.
- Add orchestration with Apache Airflow.
- Introduce Docker-based environment setup.
- Expand data quality monitoring and pipeline observability.
- Build a dashboard for exploring vehicle telemetry and analytics.
- Add CI automation for tests and data transformation checks.

## Purpose

This project is designed to demonstrate practical data engineering skills, including ingestion pipeline design, data validation, relational data modeling, SQL transformations, database reliability, API development, and automated testing.

It is an evolving portfolio project, with a focus on building reliable and maintainable data processing systems.
