SELECT i.name, COUNT(*) AS total_purchases
FROM transaction t
LEFT JOIN items i
ON t.item_id = i.id
GROUP BY t.item_id
ORDER BY total_purchases DESC
LIMIT 3;