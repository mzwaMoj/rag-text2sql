# Transaction History Setup

This script generates synthetic transaction history data and creates a SQL Server table to store it.

## Features

- Generates realistic transaction data with various transaction types
- Links transactions to existing customer IDs from the customer_information table
- Creates comprehensive transaction history with proper data types
- Supports configurable number of records (minimum 5,000)
- Includes transaction categories, channels, and merchant information

## Usage

1. **Run the script:**
   ```bash
   python transaction_history_setup.py
   ```

2. **Enter the number of records:**
   - The script will prompt you to enter the number of transaction records to generate
   - Minimum is 5,000 records
   - Recommended: 10,000+ for realistic testing

3. **The script will:**
   - Connect to your SQL Server instance
   - Fetch existing customer IDs from the customer_information table
   - Generate synthetic transaction data
   - Create the transaction_history table (drops if exists)
   - Insert all transaction records
   - Provide verification and summary statistics

## Table Structure

The `transaction_history` table includes:

- **transaction_id** (bigint, PK): Unique transaction identifier
- **customer_id** (int): Links to customer_information table
- **transaction_date** (datetime): When the transaction occurred
- **transaction_type** (nvarchar): Deposit, Withdrawal, Transfer, Payment, etc.
- **amount** (decimal): Transaction amount (negative for debits)
- **currency** (nvarchar): Currency code (primarily ZAR)
- **description** (nvarchar): Human-readable transaction description
- **category** (nvarchar): Transaction category (Groceries, Gas, etc.)
- **channel** (nvarchar): How transaction was made (ATM, Mobile App, etc.)
- **status** (nvarchar): Completed, Pending, Failed, Cancelled
- **reference_number** (nvarchar): Transaction reference
- **merchant_name** (nvarchar): Merchant name for purchases/payments
- **merchant_category** (nvarchar): Merchant category
- **account_from** (nvarchar): Source account number
- **account_to** (nvarchar): Destination account (for transfers)
- **balance_after** (decimal): Account balance after transaction
- **location** (nvarchar): Transaction location
- **created_at** (datetime): Record creation timestamp
- **updated_at** (datetime): Record update timestamp

## Transaction Types Generated

- **Deposits**: Salary, direct deposits, transfers in
- **Withdrawals**: ATM withdrawals, cash advances
- **Transfers**: Account-to-account transfers
- **Payments**: Bill payments, loan payments
- **Purchases**: POS transactions, online purchases
- **Fees**: Banking fees, service charges
- **Interest**: Interest earnings
- **Refunds**: Purchase returns, refunds

## Prerequisites

- SQL Server instance running
- Customer information table already created (from sql_server_setup.py)
- Required Python packages: pandas, pyodbc, faker, python-dotenv

## Notes

- The script automatically fetches existing customer IDs to ensure referential integrity
- If customer_information table doesn't exist, it generates synthetic customer IDs
- Transaction amounts are realistic and vary by transaction type
- Currency is weighted toward ZAR (South African Rand) with some international currencies
- Transactions span the last 2 years for historical context

## Example Output

```
Transaction History Data Generator
=================================
Enter number of transaction records to generate (minimum 5000): 10000
Successfully connected to SQL Server database: master on server: localhost\SQLEXPRESS
Fetching existing customer IDs...
Found 1000 existing customers
Generating 10000 transaction records...
Generated 0 transactions...
Generated 1000 transactions...
...
Generated 10000 transaction records
Table 'transaction_history' created in SQL Server
Inserting 10000 transaction records into SQL Server...
Inserted 0 records...
Inserted 1000 records...
...
Successfully inserted 10000 records into SQL Server table 'transaction_history'
Verification: 10000 records found in SQL Server table 'transaction_history'

Transaction Summary by Type:
  Purchase: 2156 transactions, Total: -4,234,567.89
  Salary: 1987 transactions, Total: 78,234,567.12
  Withdrawal: 1654 transactions, Total: -3,456,789.23
  ...
```
