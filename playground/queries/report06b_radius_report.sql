WITH CenterLocation AS (
    SELECT latitude as lat,
        longitude AS lng
    FROM Location
    WHERE postal_code = '71937'
),
NearbyHouseholds AS (
    SELECT (household_type = 'house')::int AS is_house,
        (household_type = 'apartment')::int AS is_apartment,
        (household_type = 'townhome')::int AS is_townhome,
        (household_type = 'condominium')::int AS is_condo,
        (household_type = 'mobile_home')::int AS is_mobile,
        square_footage,
        thermostat_setting_heating,
        thermostat_setting_cooling,
        (NOT on_grid)::int AS off_grid,
        (
            CASE
                WHEN ARRAY_LENGTH(ARRAY_AGG(DISTINCT PowerGenerator.type), 1) = 2 THEN 'Mixed'
                WHEN ARRAY_LENGTH(ARRAY_AGG(DISTINCT PowerGenerator.type), 1) = 0 THEN NULL
                ELSE (ARRAY_AGG(DISTINCT PowerGenerator.type)) [1]
            END
        ) as pg_type,
        STRING_AGG(DISTINCT HouseholdUtilities.utilities, ',') AS utilities,
        COUNT(DISTINCT PowerGenerator.email) > 0 AS has_power_gen,
        (
            COUNT(DISTINCT PowerGenerator.email) FILTER (
                WHERE PowerGenerator.capacity > 0
            ) > 0
        )::int as has_battery,
        SUM(PowerGenerator.avg_mon_kilo_hours) AS powergen_kwh
    FROM Location L
        CROSS JOIN CenterLocation C
        INNER JOIN Household USING (postal_code)
        LEFT JOIN HouseholdUtilities USING (email)
        LEFT JOIN PowerGenerator USING (email)
    WHERE 2 * 3958 * ASIN(
            SQRT(
                POW(SIN(RADIANS(L.latitude - C.lat) / 2), 2) + COS(RADIANS(C.lat)) * COS(RADIANS(L.latitude)) * POW(
                    SIN(RADIANS(L.longitude - C.lng) / 2),
                    2
                )
            )
        ) <= 5000
    GROUP BY Household.email
)
SELECT COUNT(*) AS household_count,
    SUM(is_house) AS house_count,
    SUM(is_apartment) AS apartment_count,
    SUM(is_townhome) AS townhome_count,
    SUM(is_mobile) AS mobile_count,
    SUM(is_condo) AS condo_count,
    ROUND(AVG(square_footage)) AS avg_sq_footage,
    ROUND(AVG(thermostat_setting_heating), 1) AS avg_therm_heating,
    ROUND(AVG(thermostat_setting_cooling), 1) AS avg_therm_cooling,
    STRING_AGG(DISTINCT utilities, ',') AS utilities,
    SUM(off_grid) AS off_grid_count,
    COUNT(pg_type) AS count_with_power_gen,
    MODE() WITHIN GROUP (
        ORDER BY pg_type
    ) as most_common_power_gen,
    ROUND(AVG(powergen_kwh)) AS avg_powergen_kwh,
    SUM(has_battery) AS count_with_battery
    FROM NearbyHouseholds;