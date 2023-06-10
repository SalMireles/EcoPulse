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
    COALESCE(ROUND(MIN(btu)), 0) AS min_btu_rating,
    COALESCE(ROUND(AVG(btu)), 0) AS avg_btu_rating,
    COALESCE(ROUND(MAX(btu)), 0) AS max_btu_rating
FROM AllTypes
    LEFT JOIN ApplianceBTUs USING (t)
GROUP BY t;