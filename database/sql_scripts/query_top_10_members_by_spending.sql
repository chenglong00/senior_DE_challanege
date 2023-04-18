SELECT m.name, SUM(t.price * t.quantity) AS total_spent
FROM transactions t
LEFT JOIN members m
ON t.member_id = m.id
GROUP BY m.id
ORDER BY total_spent DESC
LIMIT 10;