
# Database Schema Information

## Database Details
- **Database**: SQL Server (master)
- **Server**: localhost\SQLEXPRESS
- **Schema**: dbo

## Table: transaction_history
Comprehensive transaction history table containing all customer financial transactions including deposits, withdrawals, transfers, payments, and purchases

### Table Structure
**Full Name**: [dbo].[transaction_history]
**Records**: 5000+ transactions
**Primary Key**: transaction_id
**Foreign Keys**: customer_id
**Time Range**: Last 2 years of transaction data

### Column Definitions

**transaction_id** (bigint)
- Description: Unique transaction identifier, 12-digit number
- Range: 100000000000 to 999999999999
- Examples: 679551814302, 376513881618, 994709101726
- Rules: Auto-generated unique identifier for each transaction

**customer_id** (int)
- Description: Customer identifier linking to customer_information table
- Range: 10000000 to 99999999
- Examples: 10000001, 10000002, 10000003
- Rules: Must exist in customer_information table

**transaction_date** (datetime)
- Description: Date and time when the transaction occurred
- Examples: 2023-06-15 14:30:22, 2024-11-28 09:15:45, 2025-01-12 16:45:33
- Rules: Cannot be future date, used for transaction ordering and reporting

**transaction_type** (nvarchar)
- Description: Type of transaction performed
- Valid Values: Deposit, Withdrawal, Transfer, Payment, Purchase, Refund, Fee, Interest, Loan Payment, Salary
- Examples: Deposit, Withdrawal, Transfer
- Rules: Determines transaction processing rules and account impact

**amount** (decimal)
- Description: Transaction amount in specified currency (negative for debits, positive for credits)
- Range: -100000.00 to 100000.00
- Examples: 1500.5, -89.99, 25000.0
- Rules: Negative values represent debits (withdrawals, payments, fees), positive values represent credits (deposits, refunds, interest)

**currency** (nvarchar)
- Description: ISO 4217 currency code for the transaction
- Valid Values: ZAR, USD, EUR, GBP, JPY
- Examples: ZAR, USD, EUR
- Rules: Primarily ZAR (85%), with some international currencies for forex transactions

**description** (nvarchar)
- Description: Human-readable description of the transaction
- Examples: Groceries purchase at Woolworths, Transfer to John Smith, Salary payment from ABC Corp
- Rules: Auto-generated based on transaction type and context

**category** (nvarchar)
- Description: Transaction category for spending analysis
- Valid Values: Groceries, Gas, Restaurant, Shopping, Utilities, Healthcare, Entertainment, Travel, Education, Insurance, Banking, Investment, Salary, Bonus, Refund, Other
- Examples: Groceries, Gas, Restaurant
- Rules: Used for budgeting and spending pattern analysis

**channel** (nvarchar)
- Description: Channel through which the transaction was made
- Valid Values: ATM, Online Banking, Mobile App, Branch, POS Terminal, Wire Transfer, ACH, Check, Direct Deposit
- Examples: ATM, Online Banking, Mobile App
- Rules: Tracks customer behavior and channel preference

**status** (nvarchar)
- Description: Current status of the transaction
- Valid Values: Completed, Pending, Failed, Cancelled
- Examples: Completed, Pending, Failed
- Rules: Only Completed transactions affect account balance

**reference_number** (nvarchar)
- Description: Unique reference number for transaction tracking
- Examples: REF1234AB5678, REF9876XY1234
- Rules: Used for transaction inquiries and dispute resolution
- Pattern: REF####??####

**merchant_name** (nvarchar)
- Description: Name of merchant for purchase and payment transactions
- Examples: Woolworths, Shell Garage, Amazon
- Rules: Only populated for Purchase and Payment transaction types

**merchant_category** (nvarchar)
- Description: Category of merchant for purchase and payment transactions
- Examples: Groceries, Gas, Shopping
- Rules: Matches category field for Purchase and Payment transactions

**account_from** (nvarchar)
- Description: Source account number for the transaction
- Examples: 1234567890, 9876543210
- Rules: 10-digit account number, links to customer's account

**account_to** (nvarchar)
- Description: Destination account number for transfer transactions
- Examples: 5555666677, 1111222233
- Rules: Only populated for Transfer transaction types

**balance_after** (decimal)
- Description: Account balance after the transaction was processed
- Range: 0.00 to 100000.00
- Examples: 15420.5, 8750.25, 45000.0
- Rules: Snapshot of balance immediately after transaction completion

**location** (nvarchar)
- Description: Geographic location where the transaction occurred
- Examples: Johannesburg, South Africa, Cape Town, South Africa, London, United Kingdom
- Rules: Used for fraud detection and geographic spending analysis

**created_at** (datetime)
- Description: Timestamp when the transaction record was created in the system
- Examples: 2025-06-09 10:30:22, 2025-06-09 11:15:45
- Rules: System audit field, automatically populated

**updated_at** (datetime)
- Description: Timestamp when the transaction record was last updated
- Examples: 2025-06-09 10:30:22, 2025-06-09 11:15:45
- Rules: System audit field, automatically updated on changes

### Key Relationships & Rules

- **customer_id** references **customer_information.id**: Each transaction belongs to one customer, customers can have many transactions
- **merchant_name** depends on **transaction_type**: merchant_name is only populated when transaction_type is 'Purchase' or 'Payment'
- **account_to** depends on **transaction_type**: account_to is only populated when transaction_type is 'Transfer'
- **Amount Sign Convention**: Negative amounts for debits (Withdrawal, Payment, Purchase, Fee, Loan Payment), positive for credits (Deposit, Salary, Interest, Refund)
- **Status Constraint**: balance_after only reflects completed transactions, not pending/failed ones

### Common Query Patterns

**Customer Transactions:**
```sql
SELECT * FROM [dbo].[transaction_history] WHERE customer_id = ? ORDER BY transaction_date DESC
```
```sql
SELECT transaction_type, SUM(amount) as total FROM [dbo].[transaction_history] WHERE customer_id = ? AND status = 'Completed' GROUP BY transaction_type
```

**Date Range Queries:**
```sql
SELECT * FROM [dbo].[transaction_history] WHERE transaction_date BETWEEN ? AND ? ORDER BY transaction_date DESC
```
```sql
SELECT customer_id, COUNT(*) as transaction_count, SUM(amount) as total_amount FROM [dbo].[transaction_history] WHERE transaction_date >= DATEADD(month, -1, GETDATE()) GROUP BY customer_id
```

**Transaction Analysis:**
```sql
SELECT transaction_type, category, AVG(amount) as avg_amount, COUNT(*) as count FROM [dbo].[transaction_history] WHERE status = 'Completed' GROUP BY transaction_type, category
```
```sql
SELECT channel, COUNT(*) as usage_count FROM [dbo].[transaction_history] WHERE status = 'Completed' GROUP BY channel ORDER BY usage_count DESC
```

**Spending Patterns:**
```sql
SELECT category, SUM(ABS(amount)) as total_spent FROM [dbo].[transaction_history] WHERE amount < 0 AND status = 'Completed' GROUP BY category ORDER BY total_spent DESC
```
```sql
SELECT DATEPART(month, transaction_date) as month, SUM(amount) as net_flow FROM [dbo].[transaction_history] WHERE status = 'Completed' GROUP BY DATEPART(month, transaction_date)
```

**Merchant Analysis:**
```sql
SELECT merchant_name, COUNT(*) as transaction_count, SUM(ABS(amount)) as total_spent FROM [dbo].[transaction_history] WHERE merchant_name IS NOT NULL AND status = 'Completed' GROUP BY merchant_name ORDER BY total_spent DESC
```
```sql
SELECT merchant_category, AVG(ABS(amount)) as avg_transaction FROM [dbo].[transaction_history] WHERE merchant_category IS NOT NULL AND status = 'Completed' GROUP BY merchant_category
```

**Balance Tracking:**
```sql
SELECT transaction_date, balance_after FROM [dbo].[transaction_history] WHERE customer_id = ? ORDER BY transaction_date DESC
```
```sql
SELECT customer_id, MAX(balance_after) as peak_balance, MIN(balance_after) as lowest_balance FROM [dbo].[transaction_history] WHERE balance_after IS NOT NULL GROUP BY customer_id
```

### Query Tips

**Performance Tips:**
- Always use indexes on customer_id and transaction_date for better performance
- Filter by status = 'Completed' when calculating balances or totals
- Use date range filters to limit large result sets
- Consider using EXISTS instead of IN when joining with customer table

**Data Interpretation:**
- Negative amounts represent money leaving the account (debits)
- Positive amounts represent money entering the account (credits)
- Only 'Completed' transactions should be used for balance calculations
- merchant_name and merchant_category are only populated for Purchase/Payment types
- account_to is only populated for Transfer transactions

**Common Patterns:**
- Use SUM(amount) for net flow analysis (positive = net inflow, negative = net outflow)
- Use SUM(ABS(amount)) WHERE amount < 0 for total spending analysis
- Use SUM(amount) WHERE amount > 0 for total deposits/income analysis
- Group by DATEPART functions for time-based analysis (day, month, year)

**Aggregation Tips:**
- Use COUNT(*) for transaction frequency analysis
- Use AVG(ABS(amount)) for average transaction size by category
- Use MAX(transaction_date) to find most recent transaction per customer
- Use ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY transaction_date DESC) for latest N transactions per customer

