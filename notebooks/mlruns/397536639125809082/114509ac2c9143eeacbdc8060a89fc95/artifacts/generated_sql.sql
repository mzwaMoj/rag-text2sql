```sql
SELECT 
    YEAR(loan_application_date) AS year,
    loan_purpose AS transaction_type,
    SUM(loan_amount_applied_for) AS total_transaction_amount
FROM [dbo].[customer_information] WITH (NOLOCK)
WHERE loan_status IS NOT NULL AND loan_amount_applied_for IS NOT NULL
GROUP BY YEAR(loan_application_date), loan_purpose
ORDER BY year, transaction_type;
```