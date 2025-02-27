SELECT c.name AS category_name, COUNT(m.mushroom_id) AS mushroom_count
FROM categories c
LEFT JOIN mushrooms m ON c.category_id = m.category_id
GROUP BY c.name
ORDER BY mushroom_count DESC;