SELECT m.name
FROM mushrooms m
JOIN categories c ON m.category_id = c.category_id
JOIN regions r ON m.primary_region_id = r.region_id
WHERE 
    m.season = 'Весна' 
    AND c.name = 'Пластинчатые'
    AND r.size <= 6000;