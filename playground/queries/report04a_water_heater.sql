SELECT Location.state,
    COALESCE(ROUND(AVG(WaterHeater.capacity)), 0) AS avg_water_heater_capacity,
    COALESCE(ROUND(AVG(Appliance.btu_rating) FILTER (WHERE WaterHeater.email IS NOT NULL)), 0) AS avg_water_heater_btu,
    COALESCE(ROUND(AVG(WaterHeater.current_temperature), 1), 0) AS avg_water_heater_temp,
    COALESCE(COUNT(WaterHeater.current_temperature), 0) AS temps_set,
    COALESCE(COUNT(
        CASE
            WHEN WaterHeater.email IS NOT NULL AND WaterHeater.current_temperature IS NULL THEN 1
        END
    ), 0) AS temps_not_set
FROM Location
    LEFT JOIN Household USING (postal_code)
    LEFT JOIN Appliance USING (email)
    LEFT JOIN WaterHeater USING (email, appliance_number)
GROUP BY Location.state
ORDER BY Location.state ASC;