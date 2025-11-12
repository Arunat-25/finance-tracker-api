SELECT
    a.currency as account_currency,
	SUM(amount) as category_total_sum,
	c.title
FROM transactions AS t
JOIN categories AS c
ON t.category_id = c.id
JOIN accounts AS a
ON t.account_id = a.id
WHERE
	t.user_id = :user_id
	AND t.account_id = ANY(:list_account_id)
	AND t.transaction_type = :transaction_type
	AND date >= :date_from
	AND date < :date_to
GROUP BY
    a.currency,
	c.title