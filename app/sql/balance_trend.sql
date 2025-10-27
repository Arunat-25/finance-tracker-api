SELECT
	t.transaction_type,
	t.amount,
    t.date,
	t.account_id,
	t.to_account_id,
	t.commission,
	a.id,
	a.balance,
	a.currency
FROM transactions as t
JOIN accounts as a
ON t.account_id = a.id
WHERE
	t.user_id = :user_id AND
	t.account_id = ANY(:list_account_id) AND
	t.date > :date_from AND
	t.date <= :date_to AND
	a.is_deleted = false
ORDER BY
	t.date DESC

