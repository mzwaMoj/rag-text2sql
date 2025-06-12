
# Database Schema Information

## Database Details
- **Database**: SQL Server (master)
- **Server**: localhost\SQLEXPRESS
- **Schema**: dbo

## Table: customer_information
Comprehensive customer data table containing personal information, financial details, loan information, and product holdings for bank customers

### Table Structure
**Full Name**: [dbo].[customer_information]
**Records**: ~70 customers
**Primary Key**: id

### Column Definitions

**id** (int)
- Description: Unique customer identifier, 8-digit number
- Range: 10000000 to 99999999
- Examples: 10474206, 10962741, 13765547
- Rules: Auto-generated unique identifier for each customer

**full_name** (nvarchar)
- Description: Customer's complete name (first and last name)
- Examples: Rachel Benitez, Samuel Anderson, Austin Perkins
- Rules: Required field, contains customer's legal name

**email** (nvarchar)
- Description: Customer's email address for communication
- Examples: nelsoneddie@example.net, dillonjodi@example.net
- Rules: Must be valid email format, used for notifications

**phone_number** (nvarchar)
- Description: Customer's contact phone number
- Examples: +1-555-123-4567, (555) 987-6543
- Rules: Various formats accepted, primary contact method

**address** (nvarchar)
- Description: Customer's physical address (street, city, state, zip)
- Examples: 123 Main St, Anytown, ST 12345
- Rules: Complete postal address for correspondence

**account_number** (nvarchar)
- Description: Bank account number associated with the customer
- Examples: 1234567890, 9876543210
- Rules: 10-digit unique account identifier

**account_type** (nvarchar)
- Description: Type of bank account held by the customer
- Valid Values: Savings, Cheque, Business
- Examples: Savings, Cheque, Business
- Rules: Determines account features and limitations

**balance** (decimal)
- Description: Current account balance in local currency
- Range: 100.00 to 50000.00
- Examples: 8383.72, 19437.26, 45030.79
- Rules: Updated in real-time with transactions, minimum balance varies by account type

**gender** (nvarchar)
- Description: Customer's gender identification
- Valid Values: Male, Female
- Examples: Male, Female
- Rules: Used for demographic analysis and targeted marketing

**age** (int)
- Description: Customer's age in years
- Range: 18 to 75
- Examples: 61, 30, 64
- Rules: Must be 18+ to open account, affects product eligibility

**occupation** (nvarchar)
- Description: Customer's current job title or profession
- Examples: English as a second language teacher, Engineering geologist, Information systems manager
- Rules: Used for risk assessment and income verification

**income** (decimal)
- Description: Customer's annual income in local currency
- Range: 20000.00 to 150000.00
- Examples: 45000.0, 32000.0, 85000.0
- Rules: Used for loan eligibility and credit limit determination

**income_source** (nvarchar)
- Description: Primary source of customer's income
- Valid Values: Employment, Self-employment, Business, Investments, Pension, Rental, Freelance
- Examples: Employment, Self-employment, Business
- Rules: Affects income stability assessment for lending

**income_category** (nvarchar)
- Description: Income classification based on amount
- Valid Values: Low, Medium, High
- Examples: Low, Medium, High
- Rules: Determines product offerings and credit limits

**previous_loans_count** (int)
- Description: Number of previous loans taken by the customer
- Range: 0 to 5
- Examples: 0, 2, 5
- Rules: Higher count may affect future loan approval

**credit_score** (int)
- Description: Customer's credit score based on credit history
- Range: 300 to 850
- Examples: 718, 807, 511
- Rules: Primary factor in loan approval and interest rate determination

**loan_eligible** (bit)
- Description: Boolean indicating if customer is eligible for loans
- Valid Values: 0, 1
- Examples: 1, 0
- Rules: Determines access to lending products

**eligible_loan_amount** (decimal)
- Description: Maximum loan amount customer is eligible for
- Examples: 25000.0, 50000.0, 100000.0
- Rules: Sets upper limit for loan applications

**loan_amount_applied_for** (decimal)
- Description: Amount of loan currently applied for or received
- Examples: 15000.0, 30000.0, 0.0
- Rules: Cannot exceed eligible_loan_amount, 0 if no loan application

**loan_status** (nvarchar)
- Description: Current status of loan application or existing loan
- Valid Values: Pending, Approved, Active, Closed, None
- Examples: Active, Pending, Approved
- Rules: NULL if no loan application

**loan_tenure** (int)
- Description: Loan repayment period in months
- Range: 6 to 60 months
- Examples: 12, 24, 60
- Rules: Longer tenure increases interest rate, NULL if no loan

**loan_interest_rate** (decimal)
- Description: Annual interest rate for the loan as a percentage
- Range: 3.50% to 20.00%
- Examples: 7.5, 12.25, 15.0
- Rules: NULL if no loan, calculated using risk-based pricing

**loan_purpose** (nvarchar)
- Description: Reason for taking the loan
- Valid Values: Home, Education, Vehicle, Personal, Business
- Examples: Home, Education, Vehicle
- Rules: Required for loan applications, affects interest rates

**loan_application_date** (datetime)
- Description: Date when loan application was submitted
- Examples: 2023-05-15 10:30:00, 2024-01-20 14:45:00
- Rules: NULL if no loan application, within last 2 years

**last_login** (datetime)
- Description: Last time customer accessed online banking
- Examples: 2025-06-08 09:15:00, 2025-06-07 18:30:00
- Rules: Used to track customer engagement and activity

**product_holding** (nvarchar)
- Description: JSON array of bank products held by the customer
- Examples: ["Checking Account", "Overdraft Protection", "Foreign Currency Exchange"], ["Investment Advisory Services"], ["Home Mortgages", "Insurance Products", "Savings Account"]
- Rules: Determines cross-selling opportunities and customer value

**no_product_holding** (int)
- Description: Count of products currently held by the customer
- Range: 1 to 15
- Examples: 3, 1, 9
- Rules: Higher count indicates deeper customer relationship

**entrenchment_score** (decimal)
- Description: Percentage of total available products held by customer
- Range: 0.00% to 100.00%
- Examples: 13.04, 4.35, 39.13
- Rules: Higher score indicates stronger customer relationship and retention likelihood

### Key Relationships & Rules

- **loan_eligible** is calculated from **credit_score**: loan_eligible = 1 if credit_score >= 580, else 0
- **income_category** is calculated from **income**: Low: <30K, Medium: 30K-70K, High: >70K
- **no_product_holding** is calculated from **product_holding**: COUNT of JSON array items
- **entrenchment_score** is calculated from **no_product_holding**: (no_product_holding / 23) * 100
- Constraint: loan_amount_applied_for <= eligible_loan_amount
- Constraint: loan_interest_rate calculated from credit_score, loan_tenure, loan_amount

### Common Query Patterns

**Customer Search:**
```sql
SELECT * FROM customer_information WHERE full_name LIKE '%{name}%'
```
```sql
SELECT * FROM customer_information WHERE email = '{email}'
```

**Financial Analysis:**
```sql
SELECT AVG(balance) as avg_balance, income_category FROM customer_information GROUP BY income_category
```
```sql
SELECT COUNT(*) as customer_count, credit_score FROM customer_information WHERE credit_score BETWEEN {min} AND {max}
```

**Loan Analysis:**
```sql
SELECT * FROM customer_information WHERE loan_status = 'Active'
```
```sql
SELECT AVG(loan_interest_rate) as avg_rate, loan_purpose FROM customer_information WHERE loan_status IS NOT NULL GROUP BY loan_purpose
```

**Product Analysis:**
```sql
SELECT * FROM customer_information WHERE JSON_VALUE(product_holding, '$') LIKE '%{product_name}%'
```
```sql
SELECT AVG(no_product_holding) as avg_products, income_category FROM customer_information GROUP BY income_category
```

**Demographic Analysis:**
```sql
SELECT COUNT(*) as count, gender, age FROM customer_information GROUP BY gender, age
```
```sql
SELECT AVG(income) as avg_income, occupation FROM customer_information GROUP BY occupation HAVING COUNT(*) > 1
```

### Query Tips

**Json Handling:**
- Use JSON_VALUE() or OPENJSON() to query product_holding column
- Example: JSON_VALUE(product_holding, '$[0]') gets first product
- Use LIKE '%product_name%' for simple product searches in JSON

**Date Handling:**
- Use DATEPART() for extracting year, month, day from datetime fields
- Use DATEDIFF() to calculate time differences
- Format: 'YYYY-MM-DD HH:MM:SS' for datetime comparisons

**Aggregations:**
- Common aggregations: COUNT(), AVG(), SUM(), MIN(), MAX()
- Use GROUP BY for categorical analysis
- Use HAVING for filtered aggregations

**Performance:**
- Index exists on primary key (id)
- Consider filtering by indexed columns first
- Use appropriate data types in WHERE clauses

