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

# Import the improved SQL connector
from sql_connector import connect_to_sql_server
password = os.environ.get("password")
# =============================================================================
# CONFIGURATION SECTION - Update these settings as needed
# =============================================================================
CONFIG = {
    # Database connection settings
    'server': 'localhost,1433',  # Default server
    'database': 'master',        # Default database
    'auth_type': 'sql',          # 'windows' or 'sql'
    'username': 'SA',            # SQL Server username (required for SQL auth)
    'password': password,  # SQL Server password (required for SQL auth)
    
    # Alternative configurations for different environments
    'environments': {
        'local_docker': {
            'server': 'localhost,1433',
            'database': 'master',
            'auth_type': 'sql',
            'username': 'SA',
            'password': password
        },
        'local_windows': {
            'server': 'localhost\\SQLEXPRESS',
            'database': 'master',
            'auth_type': 'windows',
            'username': None,
            'password': None
        },
        'from_env': {
            'server': os.environ.get("server_data_studio", "localhost,1433"),
            'database': os.environ.get("database", "master"),
            'auth_type': os.environ.get("auth_type", "sql"),
            'username': os.environ.get("username", "SA"),
            'password': password
        }
    }
}
# =============================================================================

def get_connection_config(environment='default'):
    """
    Get connection configuration based on environment.
    
    Args:
        environment (str): Environment name ('default', 'local_docker', 'local_windows', 'from_env')
    
    Returns:
        dict: Connection configuration
    """
    if environment == 'default':
        return {
            'server': CONFIG['server'],
            'database': CONFIG['database'],
            'auth_type': CONFIG['auth_type'],
            'username': CONFIG['username'],
            'password': CONFIG['password']
        }
    elif environment in CONFIG['environments']:
        return CONFIG['environments'][environment]
    else:
        print(f"Warning: Unknown environment '{environment}', using default configuration")
        return get_connection_config('default')

def setup_database_connection(environment='default'):
    """
    Setup database connection using the improved sql_connector.
    
    Args:
        environment (str): Environment configuration to use
        
    Returns:
        tuple: (connection_object, cursor_object) or (None, None) if connection fails
    """
    config = get_connection_config(environment)
    
    print(f"🔄 Connecting to database using '{environment}' configuration...")
    print(f"   Server: {config['server']}")
    print(f"   Database: {config['database']}")
    print(f"   Auth Type: {config['auth_type']}")
    
    # Clean server name if it contains comments
    server = config['server']
    if "#" in server:
        server = server.split("#")[0].strip().strip('"').strip("'")
    
    conn, cursor = connect_to_sql_server(
        server=server,
        database=config['database'],
        auth_type=config['auth_type'],
        username=config['username'],
        password=config['password']
    )
    
    return conn, cursor

def connect_to_sql_server_legacy():
    """Legacy connection function - replaced by setup_database_connection"""
    print("⚠️  Warning: Using legacy connection method. Consider updating to use setup_database_connection()")
    return setup_database_connection('from_env')

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
        success_count = 0
        error_count = 0
        
        # Commit every N rows to avoid transaction log growth
        commit_interval = 100
        
        for index, row in df.iterrows():
            try:
                if count % 100 == 0:
                    print(f"Processing record {count}/{len(df)}...")
                
                # Handle NULL values for optional fields
                merchant_name = row['merchant_name'] if pd.notna(row['merchant_name']) else None
                merchant_category = row['merchant_category'] if pd.notna(row['merchant_category']) else None
                account_to = row['account_to'] if pd.notna(row['account_to']) else None
                
                # Convert numeric types explicitly
                transaction_id = int(row['transaction_id'])
                customer_id = int(row['customer_id'])
                amount = float(row['amount'])
                balance_after = float(row['balance_after'])
                
                # Insert query with pyodbc parameter style (?)
                insert_query = f"""
                INSERT INTO [dbo].[{table_name}] (
                    [transaction_id], [customer_id], [transaction_date], [transaction_type], [amount], 
                    [currency], [description], [category], [channel], [status], [reference_number], 
                    [merchant_name], [merchant_category], [account_from], [account_to], [balance_after], 
                    [location], [created_at], [updated_at]
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                
                # Execute with explicit parameter values
                cursor.execute(insert_query, (
                    transaction_id,
                    customer_id,
                    row['transaction_date'],
                    row['transaction_type'],
                    amount,
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
                    balance_after,
                    row['location'],
                    row['created_at'],
                    row['updated_at']
                ))
                
                success_count += 1
                
                # Commit in batches to avoid transaction log growth
                if success_count % commit_interval == 0:
                    conn.commit()
                    print(f"Committed {success_count} records so far...")
                
            except Exception as e:
                error_count += 1
                print(f"Error inserting row {index} with transaction ID {row['transaction_id']}: {e}")
                if error_count <= 5:  # Only show details for first 5 errors
                    print(f"Problem row data: {row}")
                elif error_count == 6:
                    print("Additional errors will be counted but details suppressed...")
                
            count += 1
        
        # Final commit for any remaining records
        conn.commit()
        print(f"Successfully inserted {success_count} records with {error_count} errors")
        
        if error_count > 0:
            print(f"Warning: {error_count} records failed to insert. See above for details.")
        
        return success_count
    except Exception as e:
        print(f"Error during batch insertion: {e}")
        conn.rollback()
        import traceback
        traceback.print_exc()
        return 0

def verify_sql_server_data(conn, cursor, table_name="transaction_history"):
    """Verify that data was successfully inserted into SQL Server"""
    try:
        # Check if table exists
        cursor.execute(f"""
        IF OBJECT_ID(N'dbo.{table_name}', N'U') IS NOT NULL
            SELECT 1
        ELSE
            SELECT 0
        """)
        table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            print(f"❌ Table '{table_name}' does not exist in the database.")
            return 0
        
        # Get count of records
        cursor.execute(f"SELECT COUNT(*) FROM [dbo].[{table_name}]")
        count = cursor.fetchone()[0]
        print(f"Verification: {count} records found in SQL Server table '{table_name}'")
        
        if count == 0:
            print(f"⚠️ Table exists but contains no records.")
            return 0
        
        # Get sample data
        cursor.execute(f"SELECT TOP 3 * FROM [dbo].[{table_name}]")
        rows = cursor.fetchall()
        
        print(f"\nSample records:")
        for idx, row in enumerate(rows):
            print(f"  Record {idx+1} - Transaction ID: {row[0]}, Customer ID: {row[1]}, Type: {row[3]}, Amount: {row[4]}")
        
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
        
        rows = cursor.fetchall()
        if rows:
            print("\nTransaction Summary by Type:")
            for row in rows:
                print(f"  {row[0]}: {row[1]} transactions, Total: {row[2]:,.2f}")
        else:
            print("\n⚠️ No completed transactions found in summary.")
        
        return count
    except Exception as e:
        print(f"❌ Error verifying SQL Server data: {e}")
        import traceback
        traceback.print_exc()
        return 0

def debug_insert(conn, cursor, table_name="transaction_history"):
    """Test insertion with a simple record to debug potential issues"""
    try:
        print("\n🔍 Testing insertion with a single record...")
        
        # Generate a simple test record
        test_record = {
            'transaction_id': 999999999999,
            'customer_id': 12345678,
            'transaction_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'transaction_type': 'Deposit',
            'amount': 100.00,
            'currency': 'ZAR',
            'description': 'Test deposit',
            'category': 'Testing',
            'channel': 'Debug',
            'status': 'Completed',
            'reference_number': 'DEBUG123',
            'merchant_name': None,
            'merchant_category': None,
            'account_from': '1234567890',
            'account_to': None,
            'balance_after': 1000.00,
            'location': 'Test Location',
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Insert test record
        insert_query = f"""
        INSERT INTO [dbo].[{table_name}] (
            [transaction_id], [customer_id], [transaction_date], [transaction_type], [amount], 
            [currency], [description], [category], [channel], [status], [reference_number], 
            [merchant_name], [merchant_category], [account_from], [account_to], [balance_after], 
            [location], [created_at], [updated_at]
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        cursor.execute(insert_query, (
            test_record['transaction_id'],
            test_record['customer_id'],
            test_record['transaction_date'],
            test_record['transaction_type'],
            test_record['amount'],
            test_record['currency'],
            test_record['description'],
            test_record['category'],
            test_record['channel'],
            test_record['status'],
            test_record['reference_number'],
            test_record['merchant_name'],
            test_record['merchant_category'],
            test_record['account_from'],
            test_record['account_to'],
            test_record['balance_after'],
            test_record['location'],
            test_record['created_at'],
            test_record['updated_at']
        ))
        
        # Commit transaction
        conn.commit()
        
        # Verify the test record
        cursor.execute(f"SELECT COUNT(*) FROM [dbo].[{table_name}] WHERE [transaction_id] = ?", (test_record['transaction_id'],))
        count = cursor.fetchone()[0]
        
        if count > 0:
            print("✅ Test insertion successful! Your database connection and table are working correctly.")
            return True
        else:
            print("❌ Test record not found after insertion.")
            return False
            
    except Exception as e:
        print(f"❌ Debug insertion failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function to generate transaction data and create SQL Server table"""
    print("=" * 80)
    print("TRANSACTION HISTORY DATA GENERATOR")
    print("=" * 80)
    
    # Choose environment configuration
    print("Available connection environments:")
    print("1. default - Use default configuration")
    print("2. local_docker - Docker SQL Server (localhost,1433)")
    print("3. local_windows - Windows SQL Server Express")
    print("4. from_env - Use environment variables")
    print("5. custom - Enter custom connection details")
    
    while True:
        choice = input("\nSelect environment (1-5) or press Enter for default: ").strip()
        if not choice:
            environment = 'default'
            break
        elif choice == '1':
            environment = 'default'
            break
        elif choice == '2':
            environment = 'local_docker'
            break
        elif choice == '3':
            environment = 'local_windows'
            break
        elif choice == '4':
            environment = 'from_env'
            break
        elif choice == '5':
            environment = setup_custom_config()
            break
        else:
            print("Invalid choice. Please select 1-5 or press Enter for default.")
    
    # Get number of records from user
    while True:
        try:
            num_records_input = input(f"Enter number of transaction records to generate (minimum 1000, default 5000): ").strip()
            if not num_records_input:
                num_records = 5000
                break
            num_records = int(num_records_input)
            if num_records < 1000:
                print("Minimum number of records is 1000. Please enter a larger number.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    print(f"\n📊 Configuration Summary:")
    print(f"   Environment: {environment}")
    print(f"   Records to generate: {num_records:,}")
    
    # Connect to SQL Server
    conn, cursor = setup_database_connection(environment)
    
    if not conn or not cursor:
        print("❌ Failed to connect to database. Please check your configuration.")
        return
    
    try:
        # Get existing customer IDs
        print("\n🔍 Fetching existing customer IDs...")
        customer_ids = get_existing_customer_ids(cursor)
        
        if not customer_ids or len(customer_ids) == 0:
            print("⚠️ Warning: No customer IDs found. Using synthetic customer IDs.")
            customer_ids = [random.randint(10000000, 99999999) for _ in range(100)]
        
        # Generate transaction data
        print(f"\n🔄 Generating {num_records:,} transaction records...")
        df = generate_transaction_data(customer_ids, n=num_records)
        print(f"✅ Generated {len(df):,} transaction records")
        
        # Create table in SQL Server
        print("\n🔨 Creating transaction_history table...")
        create_sql_server_table(cursor)
        
        # Debug insertion with a single record to test connection and table
        debug_success = debug_insert(conn, cursor)
        if not debug_success:
            print("\n⚠️ Debug insertion failed. This may indicate problems with your database connection or table schema.")
            print("Attempting bulk insert anyway...")
        
        # Insert data into SQL Server
        print(f"\n📥 Inserting {len(df):,} records into database...")
        inserted_count = insert_data_into_sql_server(conn, cursor, df)
        
        if inserted_count == 0:
            print("\n⚠️ No records were inserted. Please check the error messages above.")
            return
        
        # Verify the data was inserted correctly
        print("\n✅ Verifying data insertion...")
        record_count = verify_sql_server_data(conn, cursor)
        
        if record_count == 0:
            print("\n⚠️ No records found in the database after insertion.")
        elif record_count < inserted_count:
            print(f"\n⚠️ Only {record_count} records found in database out of {inserted_count} supposedly inserted.")
        
        print("\n" + "=" * 80)
        if record_count > 0:
            print("✅ TRANSACTION HISTORY DATA GENERATION COMPLETE!")
        else:
            print("⚠️ TRANSACTION HISTORY DATA GENERATION INCOMPLETE!")
        print("=" * 80)
        print(f"📊 Records generated: {len(df):,}")
        print(f"📊 Records inserted: {inserted_count:,}")
        print(f"📊 Records verified in database: {record_count:,}")
        print(f"🗃️  Table: transaction_history")
        print(f"🔗 Database: {get_connection_config(environment)['database']}")
        print(f"🖥️  Server: {get_connection_config(environment)['server']}")
        
    except Exception as e:
        print(f"\n❌ Error during data generation: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close SQL Server connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("\n🔐 Database connection closed")

def setup_custom_config():
    """Setup custom database configuration interactively"""
    print("\n📝 Custom Database Configuration:")
    
    server = input("Server address (e.g., localhost,1433): ").strip()
    database = input("Database name (default: master): ").strip() or "master"
    
    print("Authentication type:")
    print("1. SQL Server authentication")
    print("2. Windows authentication")
    
    while True:
        auth_choice = input("Select authentication (1-2): ").strip()
        if auth_choice == '1':
            auth_type = 'sql'
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            break
        elif auth_choice == '2':
            auth_type = 'windows'
            username = None
            password = None
            break
        else:
            print("Invalid choice. Please select 1 or 2.")
    
    # Create custom configuration
    custom_config = {
        'server': server,
        'database': database,
        'auth_type': auth_type,
        'username': username,
        'password': password
    }
    
    # Add to CONFIG for this session
    CONFIG['environments']['custom'] = custom_config
    
    return 'custom'

def quick_setup(environment='local_docker', num_records=5000):
    """
    Quick setup function for automated testing or scripting.
    
    Args:
        environment (str): Environment configuration to use
        num_records (int): Number of records to generate
    
    Returns:
        bool: True if successful, False otherwise
    """
    print(f"🚀 QUICK SETUP: {environment} environment, {num_records:,} records")
    
    try:
        # Connect to database
        conn, cursor = setup_database_connection(environment)
        if not conn or not cursor:
            print("❌ Failed to connect to database")
            return False
        
        # Get customer IDs
        customer_ids = get_existing_customer_ids(cursor)
        if not customer_ids or len(customer_ids) == 0:
            print("⚠️ Warning: No customer IDs found. Using synthetic customer IDs.")
            customer_ids = [random.randint(10000000, 99999999) for _ in range(100)]
        
        # Generate and insert data
        df = generate_transaction_data(customer_ids, n=num_records)
        create_sql_server_table(cursor)
        
        # Debug insertion with a single record
        debug_success = debug_insert(conn, cursor)
        if not debug_success:
            print("\n⚠️ Debug insertion failed. This may indicate problems with your database connection or table schema.")
            
        inserted_count = insert_data_into_sql_server(conn, cursor, df)
        
        if inserted_count == 0:
            print("❌ No records were inserted")
            return False
            
        record_count = verify_sql_server_data(conn, cursor)
        
        # Cleanup
        cursor.close()
        conn.close()
        
        if record_count > 0:
            print(f"✅ Quick setup complete! {record_count:,} records inserted and verified.")
            return True
        else:
            print("⚠️ Quick setup completed but no records were verified in the database.")
            return False
        
    except Exception as e:
        print(f"❌ Quick setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_connection_only(environment='default'):
    """
    Test database connection without generating data.
    
    Args:
        environment (str): Environment configuration to use
        
    Returns:
        bool: True if connection successful, False otherwise
    """
    print(f"🔍 Testing connection for '{environment}' environment...")
    
    conn, cursor = setup_database_connection(environment)
    
    if conn and cursor:
        try:
            # Test basic query
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()[0]
            print(f"✅ Connection successful!")
            print(f"   SQL Server Version: {version[:60]}...")
            
            # Test customer table access
            try:
                cursor.execute("SELECT COUNT(*) FROM customer_information")
                customer_count = cursor.fetchone()[0]
                print(f"   Customer records available: {customer_count:,}")
            except Exception:
                print("   ⚠️  customer_information table not found (will use synthetic IDs)")
            
            return True
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    else:
        print("❌ Failed to establish connection")
        return False

if __name__ == "__main__":
    # Check for command line arguments for automated usage
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'quick':
            # Quick setup with default parameters
            environment = sys.argv[2] if len(sys.argv) > 2 else 'local_docker'
            num_records = int(sys.argv[3]) if len(sys.argv) > 3 else 5000
            success = quick_setup(environment, num_records)
            sys.exit(0 if success else 1)
            
        elif command == 'test':
            # Test connection only
            environment = sys.argv[2] if len(sys.argv) > 2 else 'default'
            success = test_connection_only(environment)
            sys.exit(0 if success else 1)
            
        elif command == 'help':
            print("Transaction History Data Generator")
            print("=" * 40)
            print("Usage:")
            print("  python transaction_history_setup.py                    # Interactive mode")
            print("  python transaction_history_setup.py quick [env] [num]  # Quick setup")
            print("  python transaction_history_setup.py test [env]         # Test connection")
            print("  python transaction_history_setup.py help               # Show this help")
            print()
            print("Environments: default, local_docker, local_windows, from_env")
            print("Examples:")
            print("  python transaction_history_setup.py quick local_docker 10000")
            print("  python transaction_history_setup.py test local_windows")
            sys.exit(0)
            
        else:
            print(f"Unknown command: {command}")
            print("Use 'help' for usage information")
            sys.exit(1)
    else:
        # Interactive mode
        main()
