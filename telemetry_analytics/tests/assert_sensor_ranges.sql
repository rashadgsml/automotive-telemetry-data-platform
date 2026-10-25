SELECT *
FROM {{ ref('stg_telemetry') }}
WHERE speed_kmh < 0 OR speed_kmh > 250
   OR engine_temp_c < -40 OR engine_temp_c > 200
   OR battery_voltage_v < 0 OR battery_voltage_v > 20
   OR fuel_level_pct < 0 OR fuel_level_pct > 100
   OR odometer_km < 0
