SELECT
    t.transaction_type,
    t.amount,
    t.user_id,
    t.account_id,
    a.currency,
    t.to_account_id
FROM transactions AS t
JOIN accounts AS a
ON t.account_id = a.id
WHERE t.user_id = :user_id
    AND date >= :date_from
    AND date < :date_to
    AND t.account_id = ANY(:list_account_id)
