```sql
SELECT 
    FORMAT(transaction_date, 'yyyy-MM') AS transaction_month,
    SUM(amount) AS total_amount
FROM [dbo].[transaction_history] WITH (NOLOCK)
WHERE status = 'Completed'
GROUP BY FORMAT(transaction_date, 'yyyy-MM')
ORDER BY total_amount DESC;
```