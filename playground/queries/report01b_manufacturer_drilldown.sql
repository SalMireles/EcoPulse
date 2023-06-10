SELECT COUNT(DISTINCT WaterHeater) AS count_water_heaters,
    COUNT(DISTINCT Appliance) FILTER (
        WHERE Appliance.type = 'Air Handler'
    ) AS count_air_handlers,
    COUNT(DISTINCT AirConditioner) AS count_acs,
    COUNT(DISTINCT HeatPump) AS count_heat_pumps,
    COUNT(DISTINCT Heater) AS count_heaters
FROM Appliance
    INNER JOIN Manufacturer ON Appliance.manufacturer_name = Manufacturer.name
    LEFT JOIN AirConditioner, WaterHeater, HeatPump, Heater USING (appliance_number, email)
    LEFT JOIN WaterHeater USING (appliance_number, email)
    LEFT JOIN HeatPump USING (appliance_number, email)
    LEFT JOIN Heater USING (appliance_number, email);