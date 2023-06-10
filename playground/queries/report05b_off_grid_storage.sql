SELECT ROUND(AVG(PowerGenerator.capacity)) as avg_capacity
FROM PowerGenerator
    INNER JOIN Household USING (email)
WHERE NOT Household.on_grid;