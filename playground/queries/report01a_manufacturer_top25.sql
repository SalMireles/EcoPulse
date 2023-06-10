SELECT Manufacturer.name,
    COUNT(Appliance) AS Appliances
FROM Manufacturer
    INNER JOIN Appliance ON Manufacturer.name = Appliance.manufacturer_name
GROUP BY Manufacturer.name
ORDER BY Appliances DESC
LIMIT 25;