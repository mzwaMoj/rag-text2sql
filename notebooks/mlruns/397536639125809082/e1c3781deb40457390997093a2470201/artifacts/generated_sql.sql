```sql
SELECT TOP 1
    YEAR(transaction_date) AS transaction_year,
    MONTH(transaction_date) AS transaction_month,
    SUM(amount) AS total_amount
FROM [dbo].[transaction_history] WITH (NOLOCK)
WHERE status = 'Completed'
GROUP BY YEAR(transaction_date), MONTH(transaction_date)
ORDER BY total_amount DESC;
```