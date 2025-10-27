SELECT
	cat.title,
	cat.category_type,
	SUM(tran.amount) AS amount,
	acc.currency
FROM categories AS cat
JOIN transactions AS tran
ON cat.id = tran.category_id
JOIN accounts as acc
ON tran.account_id = acc.id
WHERE cat.title <> 'Перевод'
	AND tran.date >= :date_from
	AND tran.date < :date_to
	AND account_id = ANY(:list_account_id)
	AND tran.user_id = :user_id
GROUP BY
	cat.category_type,
	cat.title,
	acc.currency