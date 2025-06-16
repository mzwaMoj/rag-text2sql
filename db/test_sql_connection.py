"""
Test script to validate SQL Server connections across different platforms and authentication methods.
Tests the sql_connector.py module functionality.
"""

import sys
import os
import platform
import pandas as pd
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import warnings
warnings.filterwarnings("ignore")

# Add the current directory to Python path to import sql_connector
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from sql_connector import connect_to_sql_server

password = os.environ.get("password")
# =============================================================================
# CONFIGURATION SECTION - Modify these values as needed
# =============================================================================
CONFIG = {
    'windows_scenarios': [
        {
            'name': 'Windows Auth - localhost\\SQLEXPRESS',
            'server': 'localhost\\SQLEXPRESS',
            'database': 'master',
            'auth_type': 'windows'
        },
        {
            'name': 'Windows Auth - (local)',
            'server': '(local)',
            'database': 'master',
            'auth_type': 'windows'
        },
        {
            'name': 'SQL Auth - localhost,1433',
            'server': 'localhost,1433',
            'database': 'master',
            'auth_type': 'sql',
            'username': 'SA',
            'password': password  # Update this password
        }
    ],
    'macos_scenarios': [
        {
            'name': 'SQL Auth - localhost,1433 (Docker/Container)',
            'server': 'localhost,1433',
            'database': 'master',
            'auth_type': 'sql',
            'username': 'SA',
            'password': password  # Update this password
        },
        {
            'name': 'SQL Auth - localhost (default port)',
            'server': 'localhost',
            'database': 'master',
            'auth_type': 'sql',
            'username': 'SA',
            'password': password  # Update this password
        },
        {
            'name': 'SQL Auth - 127.0.0.1,1433',
            'server': '127.0.0.1,1433',
            'database': 'master',
            'auth_type': 'sql',
            'username': 'SA',
            'password': password # Update this password
        }
    ]
}
# =============================================================================

def test_connection_scenarios():
    """Test different connection scenarios based on the current platform."""
    print("=" * 80)
    print("SQL SERVER CONNECTION TESTING")
    print("=" * 80)
    print(f"Platform: {platform.system()}")
    print(f"Python Version: {platform.python_version()}")
    print()
    
    # Get test scenarios from configuration
    current_platform = platform.system().lower()
    
    if current_platform == 'windows':
        test_scenarios = CONFIG['windows_scenarios']
        print("💡 Running Windows-specific connection tests...")
    else:
        test_scenarios = CONFIG['macos_scenarios']
        print("💡 Running macOS/Linux-specific connection tests...")
    
    print(f"📋 {len(test_scenarios)} scenarios configured for testing")
    print("⚠️  Note: Update passwords in CONFIG section if needed")
    print()
    
    successful_connections = []
    
    # Test each scenario
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n[TEST {i}/{len(test_scenarios)}] {scenario['name']}")
        print("-" * 60)
        
        try:
            conn, cursor = connect_to_sql_server(
                server=scenario['server'],
                database=scenario['database'],
                auth_type=scenario['auth_type'],
                username=scenario.get('username'),
                password=scenario.get('password')
            )
            
            if conn and cursor:
                print("✓ Connection successful!")
                successful_connections.append(scenario)
                
                # Test basic query
                test_basic_query(cursor, scenario['name'])
                
                # Close connection
                cursor.close()
                conn.close()
                print("✓ Connection closed successfully")
            else:
                print("✗ Connection failed")
                
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Total scenarios tested: {len(test_scenarios)}")
    print(f"Successful connections: {len(successful_connections)}")
    
    if successful_connections:
        print("\nSuccessful connection scenarios:")
        for conn in successful_connections:
            print(f"  ✓ {conn['name']}")
    else:
        print("\n⚠️  No successful connections found!")
        print("Please check:")
        print("  1. SQL Server is running")
        print("  2. Correct server address and port")
        print("  3. Database exists")
        print("  4. Authentication credentials are correct")
        print("  5. ODBC drivers are installed")

def test_basic_query(cursor, scenario_name):
    """Test basic SQL queries to verify connection functionality."""
    try:
        # Test 1: Basic system query
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        print(f"  SQL Server Version: {version[:80]}...")
        
        # Test 2: Database query
        cursor.execute("SELECT DB_NAME() as current_database")
        db_name = cursor.fetchone()[0]
        print(f"  Current Database: {db_name}")
        
        # Test 3: Check if customer_information table exists
        cursor.execute("""
            SELECT COUNT(*) as table_exists 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'customer_information'
        """)
        table_exists = cursor.fetchone()[0]
        
        if table_exists > 0:
            print("  ✓ customer_information table found")
            test_customer_data_query(cursor)
        else:
            print("  ⚠️  customer_information table not found")
            
    except Exception as e:
        print(f"  ✗ Query test failed: {e}")

def test_customer_data_query(cursor):
    """Test querying customer data if the table exists."""
    try:
        # Get sample data from customer_information table
        query = """
        SELECT TOP 3 
            id,
            full_name,
            email,
            account_type,
            balance
        FROM customer_information
        ORDER BY id
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        if rows:
            print("  ✓ Sample customer data retrieved:")
            for row in rows:
                print(f"    ID: {row[0]}, Name: {row[1]}, Email: {row[2]}")
        else:
            print("  ⚠️  customer_information table is empty")
            
        # Get total count
        cursor.execute("SELECT COUNT(*) FROM customer_information")
        total_count = cursor.fetchone()[0]
        print(f"  Total customer records: {total_count}")
        
    except Exception as e:
        print(f"  ✗ Customer data query failed: {e}")

def test_connection_with_pandas():
    """Test connection using pandas for data analysis workflows."""
    print("\n" + "=" * 80)
    print("PANDAS INTEGRATION TEST")
    print("=" * 80)
    
    # Try to establish a connection using configuration
    current_platform = platform.system().lower()
    
    if current_platform == 'windows':
        scenarios = CONFIG['windows_scenarios']
    else:
        scenarios = CONFIG['macos_scenarios']
    
    # Try first scenario from config
    if scenarios:
        scenario = scenarios[0]
        print(f"🔄 Testing pandas integration with: {scenario['name']}")
        
        conn, cursor = connect_to_sql_server(
            server=scenario['server'],
            database=scenario['database'],
            auth_type=scenario['auth_type'],
            username=scenario.get('username'),
            password=scenario.get('password')
        )
    else:
        print("❌ No scenarios configured for testing")
        conn, cursor = None, None
    
    if conn:
        try:
            # Test pandas integration
            import pyodbc
            
            # Create a new connection for pandas (pyodbc connection object)
            pandas_conn = conn
            
            # Test simple query with pandas
            df = pd.read_sql("SELECT @@VERSION as sql_version", pandas_conn)
            print("✓ Pandas integration successful!")
            print(f"  Query result: {df.iloc[0]['sql_version'][:50]}...")
            
            # Test customer data query if table exists
            try:
                df_count = pd.read_sql("""
                    SELECT COUNT(*) as table_count 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_NAME = 'customer_information'
                """, pandas_conn)
                
                if df_count.iloc[0]['table_count'] > 0:
                    df_customers = pd.read_sql("""
                        SELECT TOP 5 id, full_name, account_type, balance 
                        FROM customer_information 
                        ORDER BY id
                    """, pandas_conn)
                    print("✓ Customer data retrieved with pandas:")
                    print(df_customers.to_string(index=False))
                else:
                    print("  ⚠️  customer_information table not found")
                    
            except Exception as e:
                print(f"  ⚠️  Customer table query failed: {e}")
                
        except Exception as e:
            print(f"✗ Pandas integration failed: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("✗ Cannot test pandas integration - no database connection available")

def update_test_credentials(username='SA', password='YourStrongPassword123'):
    """
    Helper function to quickly update test credentials without editing the CONFIG directly.
    
    Args:
        username (str): SQL Server username
        password (str): SQL Server password
    """
    # Update all SQL auth scenarios
    for scenario in CONFIG['windows_scenarios']:
        if scenario['auth_type'] == 'sql':
            scenario['username'] = username
            scenario['password'] = password
    
    for scenario in CONFIG['macos_scenarios']:
        if scenario['auth_type'] == 'sql':
            scenario['username'] = username
            scenario['password'] = password
    
    print(f"✓ Updated SQL authentication credentials (username: {username})")

def print_available_drivers():
    """Print available ODBC drivers for SQL Server."""
    print("\n" + "=" * 80)
    print("AVAILABLE ODBC DRIVERS")
    print("=" * 80)
    try:
        import pyodbc
        all_drivers = pyodbc.drivers()
        sql_drivers = [d for d in all_drivers if 'SQL Server' in d.upper()]
        
        if sql_drivers:
            print("SQL Server ODBC drivers found:")
            for i, driver in enumerate(sql_drivers, 1):
                print(f"  {i}. {driver}")
        else:
            print("❌ No SQL Server ODBC drivers found!")
            print("Consider installing Microsoft ODBC Driver for SQL Server")
        
        print(f"\nTotal drivers available: {len(all_drivers)}")
        
    except Exception as e:
        print(f"Error checking drivers: {e}")

def quick_test(server='localhost,1433', database='master', username='SA', password='YourStrongPassword123'):
    """
    Quick connection test function for rapid testing.
    
    Args:
        server (str): Server address
        database (str): Database name
        username (str): Username for SQL auth
        password (str): Password for SQL auth
    """
    print(f"\n🚀 QUICK CONNECTION TEST")
    print(f"Server: {server}")
    print(f"Database: {database}")
    print(f"Username: {username}")
    print("-" * 40)
    
    conn, cursor = connect_to_sql_server(
        server=server,
        database=database,
        auth_type='sql',
        username=username,
        password=password
    )
    
    if conn and cursor:
        try:
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()[0]
            print(f"✅ SUCCESS! Connected to: {version[:60]}...")
            return True
        except Exception as e:
            print(f"❌ Query failed: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("❌ CONNECTION FAILED")
    
    return False

if __name__ == "__main__":
    # Print available drivers first
    print_available_drivers()
    
    # Update credentials if needed (uncomment and modify as needed)
    # update_test_credentials(username='SA', password='myaccess')
    
    # Quick test option (uncomment to use)
    # if quick_test(server='localhost,1433', username='SA', password='myaccess'):
    #     print("✅ Quick test passed! Proceeding with full test suite...")
    # else:
    #     print("❌ Quick test failed. Check your connection settings.")
    
    # Run full test suite
    test_connection_scenarios()
    test_connection_with_pandas()
    
    print("\n" + "=" * 80)
    print("TESTING COMPLETED")
    print("=" * 80)
    print("💡 Tips:")
    print("  - Uncomment and modify update_test_credentials() to change passwords")
    print("  - Use quick_test() function for rapid connection testing")
    print("  - Update CONFIG section for custom connection scenarios")
