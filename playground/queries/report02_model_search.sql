SELECT Manufacturer.name as manufacturer,
    COALESCE(Appliance.model_name, '') AS model
FROM Manufacturer
    LEFT JOIN Appliance on Manufacturer.name = Appliance.manufacturer_name
WHERE POSITION('an' IN LOWER(Appliance.model_name)) > 0
    OR POSITION('an' IN LOWER(Manufacturer.name)) > 0
ORDER BY Manufacturer.name ASC,
    Appliance.model_name ASC;