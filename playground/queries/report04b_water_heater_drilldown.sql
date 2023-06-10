WITH AllEnergySources AS (
    SELECT *
    FROM (
            VALUES('Electric'),
                ('Gas'),
                ('Thermosolar'),
                ('Heat Pump')
        ) AS t(energy_source)
),
HeatersInState AS (
    SELECT capacity,
        current_temperature,
        energy_source
    FROM WaterHeater
        INNER JOIN Appliance USING (email, appliance_number)
        INNER JOIN Household USING (email)
        INNER JOIN Location USING (postal_code)
    WHERE state = 'AR'
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