# SQL Server Customer Data Setup

This directory contains scripts to create and populate a customer information table in SQL Server with synthetic data, without using SQLite.

## Files

1. **sql_server_setup.py** - Main script using pyodbc
2. **sql_server_setup_pymssql.py** - Alternative script using pymssql
3. **generate_sql_data.py** - Updated original script (now works without SQLite)

## Prerequisites

1. **SQL Server** - Ensure you have SQL Server running (localhost or Azure Data Studio)
2. **Python packages** - Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment Variable** - Set the SQL Server password:
   ```bash
   # Windows (PowerShell)
   $env:PASSWORD = "YourSQLServerPassword"
   
   # Or create a .env file with:
   PASSWORD=YourSQLServerPassword
   ```

## Configuration

Update the connection settings in the scripts if needed:
- **Server**: localhost (default)
- **Database**: master (default)
- **Username**: SA (default)
- **Password**: Retrieved from `PASSWORD` environment variable

## Usage

### Option 1: Using pyodbc (Recommended)
```bash
python sql_server_setup.py
```

### Option 2: Using pymssql
```bash
python sql_server_setup_pymssql.py
```

### Option 3: Using updated original script
```bash
python generate_sql_data.py
```

## What the Scripts Do

1. **Connect** to SQL Server using either pyodbc or pymssql
2. **Generate** synthetic customer data (70 records by default) including:
   - Personal information (name, email, phone, address)
   - Financial data (income, credit score, loan information)
   - Account details (balance, account type, product holdings)
   - Loan eligibility and applications
   - Product entrenchment scores

3. **Create table** `customer_information` with proper SQL Server schema
4. **Insert data** into the table with proper type conversions
5. **Verify** the data was inserted successfully

## Table Schema

The `customer_information` table includes:
- `id` (int, PRIMARY KEY)
- `full_name` (nvarchar(255))
- `email` (nvarchar(255))
- `phone_number` (nvarchar(50))
- `address` (nvarchar(max))
- `account_number` (nvarchar(20))
- `account_type` (nvarchar(50))
- `balance` (decimal(18,2))
- `gender` (nvarchar(10))
- `age` (int)
- `occupation` (nvarchar(255))
- `income` (decimal(18,2))
- `income_source` (nvarchar(100))
- `income_category` (nvarchar(50))
- `previous_loans_count` (int)
- `credit_score` (int)
- `loan_eligible` (bit)
- `eligible_loan_amount` (decimal(18,2))
- `loan_amount_applied_for` (decimal(18,2))
- `loan_status` (nvarchar(50))
- `loan_tenure` (int)
- `loan_interest_rate` (decimal(5,2))
- `loan_purpose` (nvarchar(100))
- `loan_application_date` (datetime)
- `last_login` (datetime)
- `product_holding` (nvarchar(max)) - JSON string
- `no_product_holding` (int)
- `entrenchment_score` (decimal(5,2))

## Troubleshooting

1. **Connection Issues**: 
   - Ensure SQL Server is running
   - Verify credentials and server address
   - Check if the required ODBC driver is installed for pyodbc

2. **Import Errors**: 
   - Install missing packages: `pip install pyodbc` or `pip install pymssql`
   - For pyodbc on Windows, you might need "ODBC Driver 17 for SQL Server"

3. **Permission Issues**: 
   - Ensure the SA user has necessary permissions
   - Try connecting to a different database if master is restricted

## Customization

- Change the number of records by modifying the `n` parameter in `generate_customer_data(n=70)`
- Modify connection settings in `connect_to_sql_server()` function
- Update table schema in `create_sql_server_table()` function
- Customize data generation logic in `generate_customer_data()` function
