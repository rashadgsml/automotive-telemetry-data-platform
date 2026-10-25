
CREATE TABLE IF NOT EXISTS telemetry (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    vehicle_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    speed_kmh DOUBLE PRECISION NOT NULL
        CHECK (speed_kmh BETWEEN 0 AND 250),
    engine_temp_c DOUBLE PRECISION NOT NULL
        CHECK (engine_temp_c BETWEEN -40 AND 200),
    battery_voltage_v DOUBLE PRECISION NOT NULL
        CHECK (battery_voltage_v BETWEEN 0 AND 20),
    fuel_level_pct DOUBLE PRECISION NOT NULL
        CHECK (fuel_level_pct BETWEEN 0 AND 100),
    odometer_km DOUBLE PRECISION NOT NULL
        CHECK (odometer_km >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT unique_vehicle_timestamp
        UNIQUE (vehicle_id, timestamp)
);

CREATE TABLE IF NOT EXISTS ingestion_runs (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_name VARCHAR(255) NOT NULL,
    status VARCHAR(20) NOT NULL
        CHECK (status IN ('running', 'success', 'failed')),
    total_records INTEGER NOT NULL DEFAULT 0,
    valid_records INTEGER NOT NULL DEFAULT 0,
    inserted_count INTEGER NOT NULL DEFAULT 0,
    rejected_count INTEGER NOT NULL DEFAULT 0,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    finished_at TIMESTAMPTZ,
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS raw_telemetry (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ingestion_run_id BIGINT NOT NULL
        REFERENCES ingestion_runs(id),
    source_name VARCHAR(255) NOT NULL,
    source_row_number INTEGER NOT NULL,
    raw_record JSONB NOT NULL,
    received_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT unique_source_row_per_run
        UNIQUE (ingestion_run_id, source_row_number)
);
