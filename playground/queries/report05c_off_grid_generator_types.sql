WITH Temp AS (
    SELECT ARRAY_AGG(DISTINCT PowerGenerator.type) as pg_types
    FROM PowerGenerator INNER JOIN Household USING(email)
    WHERE NOT Household.on_grid
    GROUP BY PowerGenerator.email
),
HouseholdPowerGenTypes AS (
    SELECT (CASE WHEN ARRAY_LENGTH(pg_types, 1) = 2 THEN 'Mixed' ELSE pg_types[1] END) as pg_type
    FROM Temp
)
SELECT 
ROUND((COUNT(H) FILTER (WHERE pg_type = 'Mixed'))::decimal/NULLIF(COUNT(H), 0) * 100, 1) as percent_mixed,
ROUND((COUNT(H) FILTER (WHERE pg_type = 'Solar'))::decimal/NULLIF(COUNT(H), 0) * 100, 1) as percent_solar,
ROUND((COUNT(H) FILTER (WHERE pg_type = 'Wind'))::decimal/NULLIF(COUNT(H), 0) * 100, 1) as percent_wind
FROM HouseholdPowerGenTypes H;