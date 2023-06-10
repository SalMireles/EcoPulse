SELECT Location.state,
    COUNT(Household) AS count_off_grid_households
FROM Household
    INNER JOIN Location USING (postal_code)
WHERE NOT Household.on_grid
GROUP BY Location.state
ORDER BY count_off_grid_households DESC
LIMIT 1;