```sql
SELECT TOP 1 full_name, id, account_number, balance
FROM [dbo].[customer_information] WITH (NOLOCK)
ORDER BY balance DESC;
```