SELECT m.name, m.season, m.edible
FROM mushrooms m
JOIN categories c ON m.category_id = c.category_id
WHERE c.name = 'Трубчатые';