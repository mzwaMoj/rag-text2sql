"""
SQL Server Transaction History Data Setup
This script creates a transaction history table in SQL Server and populates it with synthetic data.
Uses pyodbc for SQL Server connectivity.
"""

import pandas as pd
import numpy as np
import os
import sys
import json
import pyodbc
import random
from faker import Faker
from datetime import datetime, timedelta
import re
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def connect_to_sql_server():
    """Connect to SQL Server using pyodbc with Windows authentication"""
    # Use environment variables if available, otherwise use sensible defaults
    server = os.environ.get("server_data_studio", "localhost\\SQLEXPRESS")
    database = "master"  # Use master database as default
    
    # Clean any potential comment strings from server name
    if "#" in server:
        server = server.split("#")[0].strip().strip('"').strip("'")
    
    try:
        # Build connection string for Windows authentication
        conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        print(f"Successfully connected to SQL Server database: {database} on server: {server}")
        return conn, cursor
    except Exception as e:
        print(f"Error connecting to SQL Server: {e}")
        print(f"Connection string used: DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;")
        
        # Try alternative server names if the first one fails
        alternative_servers = ["localhost", "(local)", ".\\SQLEXPRESS", "localhost\\SQLEXPRESS"]
        
        for alt_server in alternative_servers:
            if alt_server == server:  # Skip if we already tried this one
                continue
            try:
                print(f"Trying with server: {alt_server}...")
                conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={alt_server};DATABASE={database};Trusted_Connection=yes;"
                conn = pyodbc.connect(conn_str)
                cursor = conn.cursor()
                print(f"Successfully connected to SQL Server database: {database} on server: {alt_server}")
                return conn, cursor
            except Exception as e2:
                print(f"Error with server {alt_server}: {e2}")
                continue
        
        # Try with SQL Server driver if ODBC Driver 17 fails
        try:
            print("Trying with SQL Server driver...")
            conn_str = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            print(f"Successfully connected to SQL Server database: {database} on server: {server}")
            return conn, cursor
        except Exception as e3:
            print(f"Error with SQL Server driver: {e3}")
            print("Available ODBC drivers:")
            for driver in pyodbc.drivers():
                print(f"  - {driver}")
            print("\nPlease ensure:")
            print("1. SQL Server is running")
            print("2. SQL Server Browser service is running (for named instances)")
            print("3. Your Windows account has access to SQL Server")
            print("4. TCP/IP protocol is enabled in SQL Server Configuration Manager")
            sys.exit(1)

def get_existing_customer_ids(cursor):
    """Get existing customer IDs from the customer_information table"""
    try:
        cursor.execute("SELECT [id] FROM [dbo].[customer_information]")
        customer_ids = [row[0] for row in cursor.fetchall()]
        print(f"Found {len(customer_ids)} existing customers")
        return customer_ids
    except Exception as e:
        print(f"Warning: Could not fetch customer IDs from customer_information table: {e}")
        print("Using synthetic customer IDs instead")
        # Generate synthetic customer IDs if customer table doesn't exist
        return [random.randint(10000000, 99999999) for _ in range(1000)]

def generate_transaction_data(customer_ids, n=5000):
    """Generate synthetic transaction history data"""
    fake = Faker()
    data = []
    
    # Define transaction types and categories
    transaction_types = [
        "Deposit", "Withdrawal", "Transfer", "Payment", "Purchase", 
        "Refund", "Fee", "Interest", "Loan Payment", "Salary"
    ]
    
    transaction_categories = [
        "Groceries", "Gas", "Restaurant", "Shopping", "Utilities", 
        "Healthcare", "Entertainment", "Travel", "Education", "Insurance",
        "Banking", "Investment", "Salary", "Bonus", "Refund", "Other"
    ]
    
    transaction_channels = [
        "ATM", "Online Banking", "Mobile App", "Branch", "POS Terminal",
        "Wire Transfer", "ACH", "Check", "Direct Deposit"
    ]
    
    transaction_statuses = ["Completed", "Pending", "Failed", "Cancelled"]
    
    # Currency codes (primarily ZAR for South Africa with some international)
    currencies = ["ZAR", "USD", "EUR", "GBP", "JPY"]
    
    print(f"Generating {n} transaction records...")
    
    for i in range(n):
        if i % 1000 == 0:
            print(f"Generated {i} transactions...")
            
        # Select random customer
        customer_id = random.choice(customer_ids)
        
        # Generate transaction details
        transaction_id = fake.unique.random_number(digits=12)
        transaction_type = random.choice(transaction_types)
        category = random.choice(transaction_categories)
        channel = random.choice(transaction_channels)
        status = random.choice(transaction_statuses)
        currency = random.choices(currencies, weights=[85, 5, 3, 3, 4])[0]  # Weighted for ZAR
        
        # Generate transaction amount based on type
        if transaction_type in ["Salary", "Bonus"]:
            amount = round(random.uniform(15000.0, 80000.0), 2)
        elif transaction_type in ["Deposit", "Transfer"]:
            amount = round(random.uniform(100.0, 25000.0), 2)
        elif transaction_type in ["Withdrawal", "Payment", "Purchase"]:
            amount = round(random.uniform(50.0, 5000.0), 2)
        elif transaction_type == "Fee":
            amount = round(random.uniform(5.0, 200.0), 2)
        elif transaction_type == "Interest":
            amount = round(random.uniform(10.0, 1000.0), 2)
        else:
            amount = round(random.uniform(10.0, 10000.0), 2)
        
        # For withdrawals, payments, purchases, and fees, make amount negative
        if transaction_type in ["Withdrawal", "Payment", "Purchase", "Fee", "Loan Payment"]:
            amount = -abs(amount)
        
        # Generate transaction date (last 2 years)
        transaction_date = fake.date_time_between(start_date="-2y", end_date="now")
        
        # Generate merchant/payee information
        if transaction_type in ["Purchase", "Payment"]:
            merchant_name = fake.company()
            merchant_category = category
        else:
            merchant_name = None
            merchant_category = None
        
        # Generate reference numbers and descriptions
        reference_number = fake.bothify(text='REF####??####')
        
        # Generate description based on transaction type
        if transaction_type == "Purchase":
            description = f"{category} purchase at {merchant_name if merchant_name else fake.company()}"
        elif transaction_type == "Transfer":
            description = f"Transfer to {fake.name()}"
        elif transaction_type == "Salary":
            description = f"Salary payment from {fake.company()}"
        elif transaction_type == "Withdrawal":
            description = f"Cash withdrawal - {channel}"
        elif transaction_type == "Deposit":
            description = f"Deposit - {channel}"
        else:
            description = f"{transaction_type} - {category}"
        
        # Generate account numbers (from and to)
        account_from = fake.random_number(digits=10)
        account_to = fake.random_number(digits=10) if transaction_type == "Transfer" else None
        
        # Generate balance after transaction (simplified)
        balance_after = round(random.uniform(500.0, 50000.0), 2)
        
        # Generate location data
        location = fake.city() + ", " + fake.country()
        
        transaction = {
            "transaction_id": transaction_id,
            "customer_id": customer_id,
            "transaction_date": transaction_date.strftime("%Y-%m-%d %H:%M:%S"),
            "transaction_type": transaction_type,
            "amount": amount,
            "currency": currency,
            "description": description,
            "category": category,
            "channel": channel,
            "status": status,
            "reference_number": reference_number,
            "merchant_name": merchant_name,
            "merchant_category": merchant_category,
            "account_from": str(account_from),
            "account_to": str(account_to) if account_to else None,
            "balance_after": balance_after,
            "location": location,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        data.append(transaction)
    
    print(f"Successfully generated {len(data)} transaction records")
    return pd.DataFrame(data)

def create_sql_server_table(cursor, table_name="transaction_history"):
    """Create transaction history table in SQL Server if it doesn't exist"""
    try:
        # Drop table if exists to recreate it
        cursor.execute(f"""
        IF OBJECT_ID(N'dbo.{table_name}', N'U') IS NOT NULL
            DROP TABLE [dbo].[{table_name}]
        """)
        
        # Create table
        sql_create_table = f"""
        CREATE TABLE [dbo].[{table_name}] (
            [transaction_id] [bigint] NOT NULL,
            [customer_id] [int] NOT NULL,
            [transaction_date] [datetime] NOT NULL,
            [transaction_type] [nvarchar](50) NOT NULL,
            [amount] [decimal](18, 2) NOT NULL,
            [currency] [nvarchar](3) NOT NULL,
            [description] [nvarchar](500) NULL,
            [category] [nvarchar](100) NULL,
            [channel] [nvarchar](50) NULL,
            [status] [nvarchar](20) NOT NULL,
            [reference_number] [nvarchar](50) NULL,
            [merchant_name] [nvarchar](255) NULL,
            [merchant_category] [nvarchar](100) NULL,
            [account_from] [nvarchar](20) NULL,
            [account_to] [nvarchar](20) NULL,
            [balance_after] [decimal](18, 2) NULL,
            [location] [nvarchar](255) NULL,
            [created_at] [datetime] NOT NULL,
            [updated_at] [datetime] NOT NULL,
            CONSTRAINT [PK_{table_name}] PRIMARY KEY CLUSTERED ([transaction_id] ASC)
        )
        """
        cursor.execute(sql_create_table)
        cursor.commit()
        print(f"Table '{table_name}' created in SQL Server")
    except Exception as e:
        print(f"Error creating SQL Server table: {e}")
        sys.exit(1)

def insert_data_into_sql_server(conn, cursor, df, table_name="transaction_history"):
    """Insert transaction data from DataFrame into SQL Server table using pyodbc"""
    try:
        print(f"Inserting {len(df)} transaction records into SQL Server...")
        
        # Insert data row by row
        count = 0
        for index, row in df.iterrows():
            try:
                if count % 1000 == 0:
                    print(f"Inserted {count} records...")
                
                # Handle NULL values for optional fields
                merchant_name = row['merchant_name'] if pd.notna(row['merchant_name']) else None
                merchant_category = row['merchant_category'] if pd.notna(row['merchant_category']) else None
                account_to = row['account_to'] if pd.notna(row['account_to']) else None
                
                # Insert query with pyodbc parameter style (?)
                insert_query = f"""
                INSERT INTO [dbo].[{table_name}] (
                    [transaction_id], [customer_id], [transaction_date], [transaction_type], [amount], 
                    [currency], [description], [category], [channel], [status], [reference_number], 
                    [merchant_name], [merchant_category], [account_from], [account_to], [balance_after], 
                    [location], [created_at], [updated_at]
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                
                cursor.execute(insert_query, (
                    int(row['transaction_id']),
                    int(row['customer_id']),
                    row['transaction_date'],
                    row['transaction_type'],
                    float(row['amount']),
                    row['currency'],
                    row['description'],
                    row['category'],
                    row['channel'],
                    row['status'],
                    row['reference_number'],
                    merchant_name,
                    merchant_category,
                    row['account_from'],
                    account_to,
                    float(row['balance_after']),
                    row['location'],
                    row['created_at'],
                    row['updated_at']
                ))
                count += 1
                
            except Exception as e:
                print(f"Error inserting row {index} with transaction ID {row['transaction_id']}: {e}")
                print(f"Problem row data: {row}")
                continue
        
        # Final commit
        conn.commit()
        print(f"Successfully inserted {count} records into SQL Server table '{table_name}'")
    except Exception as e:
        print(f"Error inserting data into SQL Server: {e}")
        conn.rollback()
        sys.exit(1)

def verify_sql_server_data(conn, cursor, table_name="transaction_history"):
    """Verify that data was successfully inserted into SQL Server"""
    try:
        # Get count of records
        cursor.execute(f"SELECT COUNT(*) FROM [dbo].[{table_name}]")
        count = cursor.fetchone()[0]
        print(f"Verification: {count} records found in SQL Server table '{table_name}'")
        
        # Get sample data
        cursor.execute(f"SELECT TOP 1 * FROM [dbo].[{table_name}]")
        row = cursor.fetchone()
        if row:
            print(f"Sample record - Transaction ID: {row[0]}, Customer ID: {row[1]}, Type: {row[3]}, Amount: {row[4]}")
        
        # Get transaction summary
        cursor.execute(f"""
        SELECT 
            [transaction_type], 
            COUNT(*) as count, 
            SUM([amount]) as total_amount
        FROM [dbo].[{table_name}] 
        WHERE [status] = 'Completed'
        GROUP BY [transaction_type]
        ORDER BY count DESC
        """)
        
        print("\nTransaction Summary by Type:")
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]} transactions, Total: {row[2]:,.2f}")
        
        return count
    except Exception as e:
        print(f"Error verifying SQL Server data: {e}")
        return 0

def main():
    """Main function to generate transaction data and create SQL Server table"""
    # Get number of records from user
    print("Transaction History Data Generator")
    print("=================================")
    
    while True:
        try:
            num_records = input(f"Enter number of transaction records to generate (minimum 5000): ")
            num_records = int(num_records)
            if num_records < 5000:
                print("Minimum number of records is 5000. Please enter a larger number.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    # Connect to SQL Server
    conn, cursor = connect_to_sql_server()
    
    # Get existing customer IDs
    print("Fetching existing customer IDs...")
    customer_ids = get_existing_customer_ids(cursor)
    
    # Generate transaction data
    print(f"Generating {num_records} transaction records...")
    df = generate_transaction_data(customer_ids, n=num_records)
    print(f"Generated {len(df)} transaction records")
    
    # Create table in SQL Server
    create_sql_server_table(cursor)
    
    # Insert data into SQL Server
    insert_data_into_sql_server(conn, cursor, df)
    
    # Verify the data was inserted correctly
    verify_sql_server_data(conn, cursor)
    
    # Close SQL Server connection
    cursor.close()
    conn.close()
    print("\nTransaction history data generation and loading complete!")

if __name__ == "__main__":
    main()
