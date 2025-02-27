SELECT m.name, m.description
FROM mushrooms m
JOIN (
    SELECT region_id
    FROM regions
    ORDER BY size DESC
    LIMIT 5
) AS top_regions ON m.primary_region_id = top_regions.region_id
WHERE m.edible = TRUE;