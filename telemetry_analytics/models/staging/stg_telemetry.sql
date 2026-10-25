SELECT
    id AS telemetry_id,
    vehicle_id,
    timestamp AS reading_timestamp,
    speed_kmh,
    engine_temp_c,
    battery_voltage_v,
    fuel_level_pct,
    odometer_km,
    created_at
FROM public.telemetry