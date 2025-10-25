WITH transactions_summary AS (
    SELECT 
        user_id, 
        transaction_type, 
        SUM(amount) AS total_sum,
        COUNT(*) as transaction_count,
		COUNT(CASE WHEN transaction_type = 'transfer' AND to_account_id is NULL THEN 1 END) as transfer_income_count,
		COUNT(CASE WHEN transaction_type = 'transfer' AND to_account_id is NOT NULL THEN 1 END) as transfer_expense_count
    FROM (
        SELECT *
        FROM transactions
        WHERE user_id = :user_id
            AND date >= :date_from
            AND date < :date_to
            AND account_id = ANY(:list_account_id)
         ) as transactions
    GROUP BY user_id, transaction_type
)

SELECT
    ts.user_id,
    MAX(CASE WHEN ts.transaction_type = 'income' THEN total_sum END) AS total_income,
    MAX(CASE WHEN ts.transaction_type = 'expense' THEN total_sum END) AS total_expense,
	MAX(CASE WHEN ts.transaction_type = 'income' THEN total_sum END) -
    MAX(CASE WHEN ts.transaction_type = 'expense' THEN total_sum END) AS net_balance,
    MAX(CASE WHEN ts.transaction_type = 'income' THEN transaction_count END) AS transaction_income_count,
    MAX(CASE WHEN ts.transaction_type = 'expense' THEN transaction_count END) AS transaction_expense_count,
	MAX(ts.transfer_income_count) AS transfer_income_count,
	MAX(ts.transfer_expense_count) AS transfer_expense_count,
	SUM(ts.transaction_count) as transaction_count
FROM
	transactions_summary as ts
GROUP BY ts.user_id