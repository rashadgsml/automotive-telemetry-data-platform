# Automotive Telemetry Data Platform

A Python-based data engineering project for ingesting, validating, storing, and analyzing synthetic automotive telemetry data using PostgreSQL.

## Overview

This project explores how raw vehicle telemetry data can be transformed into reliable, structured data for downstream analytics. It focuses on data ingestion, validation, database persistence, duplicate handling, and automated testing.

All vehicle telemetry data used in this project is synthetic.

## Tech Stack

- **Python** — ingestion, validation, and application logic
- **PostgreSQL** — relational data storage
- **SQLAlchemy** — database interaction and ORM
- **Pandas** — data processing, where applicable
- **FastAPI** — API endpoints for accessing telemetry data, where implemented
- **pytest** — automated testing
- **Git** — version control

## Current Features

- Ingestion of CSV and JSON data sources
- Validation of missing values, duplicate records, and invalid sensor readings
- Persistence of valid telemetry records in PostgreSQL
- Duplicate handling to avoid inserting records that already exist
- Tracking of ingestion results, including processed, inserted, duplicate, and rejected records
- Automated tests for ingestion, validation, and database operations
- Telemetry access and analytical endpoints, where implemented

## Architecture

Raw CSV / JSON Data  
↓  
Python Ingestion  
↓  
Data Validation  
↓  
PostgreSQL Storage  
↓  
Analytics and API Access

## Project Structure

```text
src/
  telemetry/
    ingestion.py
    models.py
    database.py
    repository.py
    validation.py
    generate_data.py
    run_ingestion.py
tests/
data/
```

The structure may evolve as additional data engineering capabilities are implemented.

## Getting Started

1. Clone the repository:

   ```bash
   git clone <YOUR_REPOSITORY_URL>
   cd automotive-telemetry-data-platform
   ```

2. Create and activate a Python virtual environment.

3. Install the project dependencies using the dependency file provided in the repository.

4. Configure PostgreSQL and the required database connection settings.

5. Generate synthetic data or use the included sample dataset.

6. Run the ingestion pipeline using the documented commands.

See the project configuration and source code for the current setup requirements.

## Testing

Run the automated test suite from the project root:

```bash
pytest
```

## Planned Improvements

- Containerized development environment with Docker Compose
- SQL-based analytical models and data quality tests using dbt
- Pipeline orchestration with Apache Airflow
- CI/CD and automated test execution with GitHub Actions
- Distributed processing with PySpark
- Cloud deployment and monitoring

## Project Goals

The goal is to develop practical skills in building reliable data pipelines, designing data storage systems, validating data quality, and applying production-oriented data engineering practices.