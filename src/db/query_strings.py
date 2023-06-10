# SQL queries with psycopg param interpolation: (%s)

validate_email_sql = """
SELECT COUNT(email) FROM Household WHERE email = (%s);
"""

validate_postal_code_sql = """
SELECT COUNT(postal_code) FROM Location WHERE postal_code = (%s);
"""

insert_household_sql = """
INSERT INTO Household
(
    email,
    postal_code,
    household_type,
    square_footage,
    thermostat_setting_heating,
    thermostat_setting_cooling,
    on_grid
) VALUES (
    (%s),
    (%s),
    (%s),
    (%s),
    (%s),
    (%s),
    (%s));
"""

insert_household_utility_sql = """
INSERT INTO HouseholdUtilities (email, utilities)
VALUES (
    (%s), 
    (%s));
"""

appliance_index_sql = """
SELECT * FROM Appliance WHERE Appliance.email = (%s);
"""

appliance_delete_sql = """
DELETE FROM Appliance WHERE email = (%s) AND appliance_number = (%s);
"""

insert_appliance_sql = """
INSERT INTO Appliance (email, appliance_number, manufacturer_name, type, model_name, btu_rating)
VALUES (
    (%s),
    (%s),
    (%s),
    (%s),
    (%s),
    (%s));
"""

insert_water_heater_sql = """
INSERT INTO WaterHeater (email, appliance_number, energy_source, current_temperature, capacity)
VALUES (
    (%s),
    (%s),
    (%s),
    (%s),
    (%s));
"""

insert_air_handler_air_conditioner_sql = """
INSERT INTO AirConditioner (email, appliance_number, EER)
VALUES (
    (%s),
    (%s),
    (%s));
"""

insert_air_handler_heater_sql = """
INSERT INTO Heater (email, appliance_number, energy_source)
VALUES (
    (%s),
    (%s),
    (%s));
"""

insert_air_handler_heat_pump_sql = """
INSERT INTO HeatPump (email, appliance_number, HSPF, SEER)
VALUES (
    (%s),
    (%s),
    (%s),
    (%s));
"""

power_generation_index_sql = """
SELECT * FROM PowerGenerator WHERE PowerGenerator.email = (%s);
"""

insert_power_generation_sql = """
INSERT INTO PowerGenerator (pg_number, email, type, avg_mon_kilo_hours, capacity)
VALUES (
    (%s),
    (%s),
    (%s),
    (%s),
    (%s));
"""

power_generation_methods_sql = """
SELECT * FROM PowerGenerator WHERE email = (%s);
"""

power_generation_methods_delete_sql = """
DELETE FROM PowerGenerator WHERE email = (%s) AND pg_number = (%s);
"""

manufacturer_names_sql = """
SELECT Manufacturer.name
FROM Manufacturer;
"""

manufacturer_index_sql = """
SELECT Manufacturer.name,
    COUNT(Appliance) AS Appliances
FROM Manufacturer
    INNER JOIN Appliance ON Manufacturer.name = Appliance.manufacturer_name
GROUP BY Manufacturer.name
ORDER BY Appliances DESC
LIMIT 25;
"""

manufacturer_detail_sql = """
SELECT COUNT(DISTINCT WaterHeater) AS count_water_heaters,
    COUNT(DISTINCT Appliance) FILTER (
        WHERE Appliance.type = 'Air Handler'
    ) AS count_air_handlers,
    COUNT(DISTINCT AirConditioner) AS count_acs,
    COUNT(DISTINCT HeatPump) AS count_heat_pumps,
    COUNT(DISTINCT Heater) AS count_heaters
FROM Appliance
    LEFT JOIN AirConditioner USING (appliance_number, email)
    LEFT JOIN WaterHeater USING (appliance_number, email)
    LEFT JOIN HeatPump USING (appliance_number, email)
    LEFT JOIN Heater USING (appliance_number, email)
WHERE Appliance.manufacturer_name = (%s);
"""

manufacturer_search_sql = """
SELECT DISTINCT Manufacturer.name AS manufacturer,
    COALESCE(Appliance.model_name, '') AS model
FROM Manufacturer
    LEFT JOIN Appliance on Manufacturer.name = Appliance.manufacturer_name
WHERE POSITION((%s) IN LOWER(Appliance.model_name)) > 0
    OR POSITION((%s) IN LOWER(Manufacturer.name)) > 0
ORDER BY 1 ASC, 2 ASC;
"""

hcm_index_sql = """
SELECT Household.household_type,
    COUNT(AirConditioner) AS ac_count,
    COALESCE(ROUND(AVG(btu_rating) FILTER (WHERE eer IS NOT NULL)),0) AS ac_avg_btu,
    COALESCE(ROUND(AVG(eer), 1),0) AS ac_avg_eer,
    COUNT(Heater) AS heater_count,
    COALESCE(ROUND(AVG(btu_rating) FILTER (WHERE energy_source IS NOT
    NULL)),0) AS heater_avg_btu,
    COALESCE(MODE() WITHIN GROUP (ORDER BY energy_source), '') AS heater_top_src,
    COUNT(HeatPump) AS heatpump_count,
    COALESCE(ROUND(AVG(btu_rating) FILTER (WHERE hspf IS NOT NULL)), 0) AS heatpump_avg_btu,
    COALESCE(ROUND(AVG(hspf), 1), 0) AS heatpump_avg_hspf,
    COALESCE(ROUND(AVG(seer), 1), 0) AS heatpump_avg_seer
FROM Household
    LEFT JOIN Appliance USING (email)
    LEFT JOIN AirConditioner USING (email, appliance_number)
    LEFT JOIN Heater USING (email, appliance_number)
    LEFT JOIN HeatPump USING (email, appliance_number)
GROUP BY Household.household_type;
"""

water_heater_index_sql = """
SELECT Location.state,
    COALESCE(ROUND(AVG(WaterHeater.capacity)), 0) AS
avg_water_heater_capacity,
    COALESCE(ROUND(AVG(Appliance.btu_rating) FILTER (WHERE
WaterHeater.email IS NOT NULL)), 0) AS avg_water_heater_btu,
    COALESCE(ROUND(AVG(WaterHeater.current_temperature), 1), 0) AS
avg_water_heater_temp,
    COALESCE(COUNT(WaterHeater.current_temperature), 0) AS temps_set,
    COALESCE(COUNT(
        CASE
            WHEN WaterHeater.email IS NOT NULL AND
WaterHeater.current_temperature IS NULL THEN 1
        END
    ), 0) AS temps_not_set
FROM Location
    LEFT JOIN Household USING (postal_code)
    LEFT JOIN Appliance USING (email)
    LEFT JOIN WaterHeater USING (email, appliance_number)
GROUP BY Location.state
ORDER BY Location.state ASC;
"""

water_heater_detail_sql = """
WITH AllEnergySources AS (
SELECT *
FROM (VALUES('Electric'),
            ('Gas'),
            ('Thermosolar'),
            ('Heat Pump')
    ) AS t(energy_source)
),
HeatersInState AS (
    SELECT capacity,
        current_temperature,
        INITCAP(LOWER(energy_source)) AS energy_source
    FROM WaterHeater
        INNER JOIN Appliance USING (email, appliance_number)
        INNER JOIN Household USING (email)
        INNER JOIN Location USING (postal_code)
    WHERE state = (%s)
)
SELECT AllEnergySources.energy_source,
    COALESCE(ROUND(MIN(W.capacity)), 0) AS min_capacity,
    COALESCE(ROUND(AVG(W.capacity)), 0) AS avg_capacity,
    COALESCE(ROUND(MAX(W.capacity)), 0) AS max_capacity,
    COALESCE(ROUND(MIN(W.current_temperature), 1), 0) AS min_temp,
    COALESCE(ROUND(AVG(W.current_temperature), 1), 0) AS avg_temp,
    COALESCE(ROUND(MAX(W.current_temperature), 1), 0) AS max_temp
FROM AllEnergySources
    LEFT JOIN HeatersInState W USING (energy_source)
    GROUP BY AllEnergySources.energy_source
    ORDER BY AllEnergySources.energy_source ASC;
"""

off_grid_state_sql = """
SELECT Location.state,
    COUNT(Household) AS count_off_grid_households
FROM Household
    INNER JOIN Location USING (postal_code)
WHERE NOT Household.on_grid
GROUP BY Location.state
ORDER BY count_off_grid_households DESC
LIMIT 1;
"""

off_grid_pq_sql = """
SELECT ROUND(AVG(PowerGenerator.capacity)) as avg_capacity
FROM PowerGenerator
    INNER JOIN Household USING (email)
WHERE NOT Household.on_grid;
"""

off_grid_pg_types_sql = """
WITH Temp AS (
    SELECT ARRAY_AGG(DISTINCT PowerGenerator.type) as pg_types
    FROM PowerGenerator INNER JOIN Household USING(email)
    WHERE NOT Household.on_grid
    GROUP BY PowerGenerator.email
),
HouseholdPowerGenTypes AS (
    SELECT (CASE WHEN ARRAY_LENGTH(pg_types, 1) = 2 THEN 'Mixed' ELSE
    pg_types[1] END) as pg_type
    FROM Temp 
)

SELECT
ROUND((COUNT(H) FILTER (WHERE pg_type = 'Mixed'))::decimal/NULLIF(COUNT(H),
0) * 100, 1) as percent_mixed,
ROUND((COUNT(H) FILTER (WHERE pg_type = 'Solar-Electric'))::decimal/NULLIF(COUNT(H),
0) * 100, 1) as percent_solar,
ROUND((COUNT(H) FILTER (WHERE pg_type = 'Wind'))::decimal/NULLIF(COUNT(H),
0) * 100, 1) as percent_wind
FROM HouseholdPowerGenTypes H;
"""

off_grid_averages_sql = """
WITH Averages AS (
    SELECT AVG(capacity) FILTER (WHERE NOT on_grid) as off_grid,
    AVG(capacity) FILTER (WHERE on_grid) as on_grid
    FROM Household
        INNER JOIN WaterHeater USING (email)
)
SELECT COALESCE(ROUND(on_grid, 1), 0) as avg_on_grid_capacity,
    COALESCE(ROUND(off_grid, 1), 0) as avg_off_grid_capacity
FROM Averages;
"""

off_grid_btus_sql = """
With OffGrid AS (
    SELECT email,
        appliance_number,
        btu_rating AS btu,
        type
    FROM Household
            INNER JOIN Appliance USING (email)
    WHERE NOT on_grid
),
AllTypes AS (
    SELECT * FROM (
    VALUES ('Air Handler'),('Water Heater'),('Air Conditioner'),('Heat Pump'),('Heater')
    ) AS Temp (t)
),
ApplianceBTUs AS (
    (SELECT 'Air Handler' AS t, btu FROM OffGrid WHERE type = 'Air Handler')
    UNION
    (SELECT 'Water Heater' AS t, btu FROM OffGrid WHERE type = 'Water Heater')
    UNION
    (SELECT 'Air Conditioner' AS t, btu FROM AirConditioner INNER JOIN OffGrid USING (email, appliance_number))
    UNION
    (SELECT 'Heat Pump' AS t, btu FROM HeatPump INNER JOIN OffGrid USING (email, appliance_number))
    UNION
    (SELECT 'Heater' AS t, btu FROM Heater INNER JOIN OffGrid USING (email, appliance_number))
)
SELECT t as type,
    COALESCE(ROUND(MIN(btu), 0), 0) AS min_btu_rating,
    COALESCE(ROUND(AVG(btu), 0), 0) AS avg_btu_rating,
    COALESCE(ROUND(MAX(btu), 0), 0) AS max_btu_rating
FROM AllTypes
    LEFT JOIN ApplianceBTUs USING (t)
GROUP BY t;
"""

radius_detail_sql = """
WITH CenterLocation AS (
    SELECT latitude as lat,
        longitude AS lng
    FROM Location
    WHERE postal_code = (%s)
),
NearbyHouseholds AS (
    SELECT 
        Household.email,
        'a' as joinCol,
        (household_type = 'house')::int AS is_house,
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
        ) <= (%s)
    GROUP BY Household.email
),
utilsList as (
	SELECT
	'a' as joinCol,
	STRING_AGG(DISTINCT utilities, ',') AS utilities
	FROM
	NearbyHouseholds INNER JOIN householdutilities USING (email)
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
    utilsList.utilities,
    SUM(off_grid) AS off_grid_count,
    COUNT(pg_type) AS count_with_power_gen,
    MODE() WITHIN GROUP (
        ORDER BY pg_type
    ) as most_common_power_gen,
    ROUND(AVG(powergen_kwh)) AS avg_powergen_kwh,
    SUM(has_battery) AS count_with_battery
    FROM NearbyHouseholds
    LEFT JOIN utilsList USING (joinCol)
	GROUP BY utilsList.utilities;
"""
