SELECT DISTINCT r.name AS region_name
FROM regions r
JOIN mushrooms m ON r.region_id = m.primary_region_id;