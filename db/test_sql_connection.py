"""
Simple test script to query the customer_information table and display sample data
"""

import pyodbc
import pandas as pd

def connect_to_sql_server():
    """Connect to SQL Server using pyodbc with Windows authentication"""
    server = "localhost\\SQLEXPRESS"
    database = "master"
    
    try:
        conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        print(f"Error connecting to SQL Server: {e}")
        return None

def test_query():
    """Test query to display sample customer data"""
    conn = connect_to_sql_server()
    if not conn:
        return
    
    try:
        # Query for sample data
        query = """
        SELECT TOP 10 
            id,
            full_name,
            email,
            account_type,
            balance,
            age,
            occupation,
            income_category,
            credit_score,
            loan_status,
            product_holding
        FROM customer_information
        ORDER BY id
        """
        
        # Execute query and display results
        df = pd.read_sql(query, conn)
        print("Sample Customer Data from SQL Server:")
        print("=" * 80)
        print(df.to_string(index=False))
        
        # Get total count
        count_query = "SELECT COUNT(*) as total_records FROM customer_information"
        count_df = pd.read_sql(count_query, conn)
        print(f"\nTotal records in table: {count_df.iloc[0]['total_records']}")
        
        # Show column info
        columns_query = """
        SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = 'customer_information'
        ORDER BY ORDINAL_POSITION
        """
        columns_df = pd.read_sql(columns_query, conn)
        print("\nTable Schema:")
        print("=" * 50)
        print(columns_df.to_string(index=False))
        
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    test_query()
