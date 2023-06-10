SELECT Household.household_type,
    COUNT(AirConditioner) AS ac_count,
    COALESCE(ROUND(AVG(btu_rating) FILTER (WHERE eer IS NOT NULL)),0) AS ac_avg_btu,
    COALESCE(ROUND(AVG(eer), 1),0) AS ac_avg_eer,

    COUNT(Heater) AS heater_count,
    COALESCE(ROUND(AVG(btu_rating) FILTER (WHERE energy_source IS NOT NULL)),0) AS heater_avg_btu,
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