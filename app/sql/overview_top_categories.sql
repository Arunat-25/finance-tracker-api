WITH cat_with_total AS
	(SELECT
		cat_tran.user_id,
		cat_tran.title,
		cat_tran.category_type,
		SUM(cat_tran.amount) AS total
	FROM
		(SELECT
			cat.*,
			tran.id,
			tran.amount,
			tran.date,
			account_id
		FROM categories AS cat
		INNER JOIN transactions AS tran
		ON cat.id = tran.category_id
		WHERE cat.title <> 'Перевод'
		    AND tran.date >= :date_from
		    AND tran.date < :date_to
		    AND account_id = ANY(:list_account_id)
		    AND tran.user_id = :user_id
		) AS cat_tran
		-- сделать так, чтобы категорию перевод нельзя было удалить.
	GROUP BY
		cat_tran.user_id,
		cat_tran.category_type,
		cat_tran.title),

	ranked_cwt AS (
	SELECT
		*,
		ROW_NUMBER() OVER(
			PARTITION BY
				cwt.user_id,
				cwt.category_type
			ORDER BY
				cwt.total DESC
		) as rank
	FROM cat_with_total AS cwt
	)

SELECT
    user_id,
    title,
    category_type,
    total
FROM ranked_cwt
WHERE rank = 1