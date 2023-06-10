-- Pick random ZIPs to calculate haversine distance between
WITH CodePairs AS (
    SELECT DISTINCT L1.postal_code AS code1,
        L2.postal_code AS code2
    FROM (
            SELECT Location.postal_code
            FROM LOCATION
            ORDER BY RANDOM()
            LIMIT 20
        ) as L1
        CROSS JOIN (
            SELECT Location.postal_code 
            FROM LOCATION
            ORDER BY RANDOM()
            LIMIT 20
        ) AS L2
)
SELECT CodePairs.code1,
    CodePairs.code2,
    L1.latitude as lat1,
    L1.longitude as lng1,
    L2.latitude as lat2,
    L2.longitude as lng2,
    haversine(
        L1.latitude,
        L1.longitude,
        L2.latitude,
        L2.longitude
    ) as distance_miles
FROM CodePairs
    INNER JOIN Location AS L1 ON CodePairs.code1 = L1.postal_code
    INNER JOIN Location AS L2 ON CodePairs.code2 = L2.postal_code;