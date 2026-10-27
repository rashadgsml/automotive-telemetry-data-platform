
WITH daily_metrics AS (
    SELECT
        vehicle_id,
        DATE_TRUNC('day', reading_timestamp)::date AS reading_date,

        COUNT(*) AS total_readings,
        ROUND(AVG(speed_kmh)::numeric, 2) AS avg_speed_kmh,
        ROUND(MAX(speed_kmh)::numeric, 2) AS max_speed_kmh,
        ROUND(MAX(engine_temp_c)::numeric, 2) AS max_engine_temp_c,
        ROUND(MIN(battery_voltage_v)::numeric, 2) AS min_battery_voltage_v,
        ROUND(MIN(fuel_level_pct)::numeric, 2) AS min_fuel_level_pct,
        MIN(odometer_km) AS start_odometer_km,
        MAX(odometer_km) AS end_odometer_km

    FROM {{ ref('stg_telemetry') }}
    GROUP BY
        vehicle_id,
        DATE_TRUNC('day', reading_timestamp)::date
)

SELECT
    vehicle_id,
    reading_date,
    total_readings,
    avg_speed_kmh,
    max_speed_kmh,
    max_engine_temp_c,
    min_battery_voltage_v,
    min_fuel_level_pct,
    start_odometer_km,
    end_odometer_km,
    ROUND((end_odometer_km - start_odometer_km)::numeric, 2)
     AS distance_traveled_km
FROM daily_metrics
