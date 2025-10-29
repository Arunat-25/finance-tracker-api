WITH ranked_transactions AS (
    SELECT
        t.date,
        t.account_id,
         CASE
            WHEN t.transaction_type = 'transfer' AND t.to_account_id IS NOT NULL THEN t.balance_after+t.amount+COALESCE(t.commission, 0)
            WHEN t.transaction_type = 'transfer' AND t.to_account_id IS NULL THEN t.balance_after-t.amount
            WHEN t.transaction_type = 'income' THEN t.balance_after-t.amount
            WHEN t.transaction_type = 'expense' THEN t.balance_after+t.amount+COALESCE(t.commission, 0)
        END balance_before,
        a.currency,
        ROW_NUMBER() OVER(
            PARTITION BY t.account_id
            ORDER BY t.date
        ) as rank
    FROM transactions as t
    JOIN accounts as a
    ON t.account_id = a.id
    WHERE
        t.user_id = :user_id AND
        t.date >= :date_from AND
        t.date < :date_to AND
        t.account_id = ANY(:list_account_id)
)

SELECT *
FROM ranked_transactions
WHERE rank = 1