```sql
SELECT TOP 10 
    full_name, 
    account_number, 
    balance
FROM [dbo].[customer_information] WITH (NOLOCK)
ORDER BY balance DESC;
```