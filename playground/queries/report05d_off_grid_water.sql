WITH Averages AS (
    SELECT AVG(capacity) FILTER (WHERE NOT on_grid) as off_grid,
    AVG(capacity) FILTER (WHERE on_grid) as on_grid
    FROM Household
        INNER JOIN WaterHeater USING (email)
)
SELECT COALESCE(ROUND(on_grid, 1), 0) as avg_on_grid_capacity,
    COALESCE(ROUND(off_grid, 1), 0) as avg_off_grid_capacity
FROM Averages;