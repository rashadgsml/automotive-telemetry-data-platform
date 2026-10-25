
CREATE OR REPLACE VIEW vehicle_daily_metrics AS
SELECT
    vehicle_id,
    DATE(timestamp AT TIME ZONE 'UTC') AS reading_date,
    COUNT(*) AS reading_count,
    ROUND(AVG(speed_kmh)::numeric, 2) AS average_speed_kmh,
    ROUND(AVG(engine_temp_c)::numeric, 2) AS average_engine_temp_c,
    ROUND(MAX(speed_kmh)::numeric, 2) AS max_speed_kmh,
    ROUND(MIN(fuel_level_pct)::numeric, 2) AS min_fuel_level_pct,
    ROUND(AVG(battery_voltage_v)::numeric, 2) AS average_battery_voltage_v
FROM telemetry
GROUP BY
    vehicle_id,
    DATE(timestamp AT TIME ZONE 'UTC');
