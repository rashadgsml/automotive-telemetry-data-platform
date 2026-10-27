
SELECT
    vehicle_id,
    reading_date,
    COUNT(*) AS row_count
FROM {{ ref('fct_vehicle_daily_metrics') }}
GROUP BY
    vehicle_id,
    reading_date
HAVING COUNT(*) > 1
