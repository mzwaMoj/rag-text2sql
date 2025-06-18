"""
Test script for CRS Data Setup with Windows Authentication
This script helps test the CRS data setup functionality using Windows authentication.
"""

import os
import sys
import pandas as pd
from datetime import datetime

# Add the db directory to the path so we can import our modules
sys.path.append(os.path.dirname(__file__))

try:
    from crs_data_setup import setup_database_connection, verify_data_insertion
    from sql_connector import connect_to_sql_server
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this script from the db directory")
    sys.exit(1)

def test_database_connection():
    """Test database connection with Windows authentication"""
    print("🔍 Testing database connection...")
    
    # Try different Windows connection configurations
    test_configs = [
        {
            'name': 'Windows SQL Express (default)',
            'server': 'localhost\\SQLEXPRESS',
            'database': 'master',
            'auth_type': 'windows',
            'username': None,
            'password': None
        },
        {
            'name': 'Windows SQL Express (dot notation)',
            'server': '.\\SQLEXPRESS',
            'database': 'master',
            'auth_type': 'windows',
            'username': None,
            'password': None
        },
        {
            'name': 'Local Windows SQL Server',
            'server': 'localhost',
            'database': 'master',
            'auth_type': 'windows',
            'username': None,
            'password': None
        },
        {
            'name': 'Windows SQL Server (MSSQLSERVER)',
            'server': 'localhost\\MSSQLSERVER',
            'database': 'master',
            'auth_type': 'windows',
            'username': None,
            'password': None
        }
    ]
    
    for config in test_configs:
        print(f"\n   Testing: {config['name']}")
        print(f"   Server: {config['server']}")
        
        try:
            conn, cursor = connect_to_sql_server(
                server=config['server'],
                database=config['database'],
                auth_type=config['auth_type'],
                username=config['username'],
                password=config['password']
            )
            
            if conn and cursor:
                print("   ✅ Connection successful!")
                
                # Test a simple query
                cursor.execute("SELECT @@VERSION")
                version = cursor.fetchone()[0]
                print(f"   📊 SQL Server version: {version[:50]}...")
                
                # Test schema access
                cursor.execute("SELECT name FROM sys.databases WHERE name IN ('master', 'tempdb')")
                databases = [row[0] for row in cursor.fetchall()]
                print(f"   📊 Accessible databases: {databases}")
                
                cursor.close()
                conn.close()
                
                print(f"   ✅ {config['name']} works! Use this configuration.")
                return True, config
            else:
                print("   ❌ Connection failed")
                
        except Exception as e:
            print(f"   ❌ Connection error: {e}")
    
    print("\n❌ All connection attempts failed")
    return False, None

def test_using_crs_setup():
    """Test using the CRS setup module"""
    print("🔍 Testing CRS setup module connection...")
    
    try:
        # Test with default (should be Windows auth)
        conn, cursor = setup_database_connection('default')
        
        if conn and cursor:
            print("✅ CRS setup connection successful")
            
            # Test a simple query
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()[0]
            print(f"📊 SQL Server version: {version[:50]}...")
            
            cursor.close()
            conn.close()
            return True
        else:
            print("❌ CRS setup connection failed")
            return False
            
    except Exception as e:
        print(f"❌ CRS setup connection error: {e}")
        return False

def test_excel_loading(excel_file_path):
    """Test loading Excel file"""
    print(f"📁 Testing Excel file loading: {excel_file_path}")
    
    try:
        if not os.path.exists(excel_file_path):
            print(f"❌ Excel file not found: {excel_file_path}")
            return False
        
        # Try to load the Excel file
        excel_data = pd.read_excel(excel_file_path, sheet_name=None, engine='openpyxl')
        
        print(f"✅ Excel file loaded successfully")
        print(f"📊 Found {len(excel_data)} sheets:")
        
        for sheet_name, df in excel_data.items():
            rows, cols = df.shape
            print(f"   - {sheet_name}: {rows} rows, {cols} columns")
            
            # Show column names for first few sheets
            if len(excel_data) <= 3:  # Only show details if not too many sheets
                print(f"     Columns: {list(df.columns)[:5]}{'...' if len(df.columns) > 5 else ''}")
        
        # Check for required sheets
        required_sheets = ['AccountReport', 'MessageSpec', 'CountryCode']
        missing_sheets = [sheet for sheet in required_sheets if sheet not in excel_data.keys()]
        
        if missing_sheets:
            print(f"⚠️  Warning: Missing required sheets: {missing_sheets}")
            print(f"   Available sheets: {list(excel_data.keys())}")
        else:
            print("✅ All required sheets found")
        
        return True
        
    except Exception as e:
        print(f"❌ Excel loading error: {e}")
        return False

def check_existing_tables():
    """Check if CRS tables already exist in the database"""
    print("🔍 Checking for existing CRS tables...")
    
    try:
        conn, cursor = setup_database_connection('default')
        
        if not conn or not cursor:
            print("❌ Database connection failed")
            return False
        
        tables_to_check = [
            ("[Ref].[CRS_CountryCode]", "CountryCode"),
            ("[DATA].[CRS_GH_AccountReport]", "AccountReport"), 
            ("[DATA].[CRS_GH_MessageSpec]", "MessageSpec")
        ]
        
        existing_tables = []
        
        for table_name, friendly_name in tables_to_check:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                existing_tables.append((friendly_name, count))
                print(f"   ✅ {friendly_name}: {count:,} records")
            except Exception:
                print(f"   ❌ {friendly_name}: Table does not exist")
        
        cursor.close()
        conn.close()
        
        if existing_tables:
            print(f"📊 Found {len(existing_tables)} existing tables with data")
            return True
        else:
            print("📊 No existing CRS tables found")
            return False
            
    except Exception as e:
        print(f"❌ Error checking tables: {e}")
        return False

def create_sample_excel_file():
    """Create a sample Excel file for testing"""
    print("📝 Creating sample Excel file for testing...")
    
    try:
        # Create sample data for each sheet
        sample_country_data = pd.DataFrame({
            'CountryShortCode': ['ZA', 'US', 'GB', 'DE', 'FR'],
            'Country': ['South Africa', 'United States', 'United Kingdom', 'Germany', 'France'],
            'Country2': ['RSA', 'USA', 'UK', 'DEU', 'FRA'],
            'Country3': ['South Africa', 'America', 'Britain', 'Deutschland', 'France']
        })
        
        sample_account_data = pd.DataFrame({
            'ParentID': ['PAR001', 'PAR002', 'PAR003'],
            'DocTypeIndic2': ['OECD1', 'OECD1', 'OECD1'],
            'DocRefId3': ['DOC001', 'DOC002', 'DOC003'],
            'AccountNumber': ['ACC123456', 'ACC789012', 'ACC345678'],
            'AccNumberType': ['IBAN', 'IBAN', 'IBAN'],
            'ClosedAccount': ['false', 'false', 'true'],
            'DormantAccount': ['false', 'true', 'false'],
            'UndocumentedAccount': ['false', 'false', 'false'],
            'ResCountryCode4': ['ZA', 'US', 'GB'],
            'AcctHolderType': ['Individual', 'Individual', 'Entity'],
            'nameType': ['OECD202', 'OECD202', 'OECD201'],
            'FirstName': ['John', 'Jane', None],
            'LastName': ['Doe', 'Smith', None],
            'MiddleName': ['Michael', None, None],
            'CountryCode5': ['ZA', 'US', 'GB'],
            'Street': ['123 Main St', '456 Oak Ave', '789 High St'],
            'PostCode': ['12345', '67890', 'SW1A 1AA'],
            'City': ['Cape Town', 'New York', 'London'],
            'BirthDate': ['1985-01-15', '1990-05-20', None],
            'TIN6': ['TIN123456789', 'TIN987654321', 'TIN555666777'],
            'issuedBy7': ['ZA', 'US', 'GB'],
            'AccountBalance': ['15000.50', '25000.75', '50000.00'],
            'currCode': ['ZAR', 'USD', 'GBP'],
            'Type': ['OECD101', 'OECD102', 'OECD103'],
            'PaymentAmnt': ['1000.00', '2000.00', '3000.00'],
            'currCode8': ['ZAR', 'USD', 'GBP'],
            'Processed': [False, False, True]
        })
        
        sample_message_data = pd.DataFrame({
            'ParentID': ['MSG001', 'MSG002'],
            'version': ['1.0', '1.0'],
            'SendingCompanyIN': ['BANK001', 'BANK002'],
            'TransmittingCountry': ['ZA', 'US'],
            'ReceivingCountry': ['US', 'ZA'],
            'MessageType': ['CRS', 'CRS'],
            'MessageRefId': ['REF001', 'REF002'],
            'MessageTypeIndic': ['CRS701', 'CRS701'],
            'ReportingPeriod': ['2023', '2023'],
            'Timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')] * 2,
            'ResCountryCode': ['ZA', 'US'],
            'TIN': ['TIN123', 'TIN456'],
            'issuedBy': ['ZA', 'US'],
            'Name': ['Standard Bank', 'US Bank'],
            'CountryCode': ['ZA', 'US'],
            'AddressFree': ['Address 1', 'Address 2'],
            'DocTypeIndic': ['OECD1', 'OECD1'],
            'DocRefId': ['DOC001', 'DOC002'],
            'Processed': [False, False]
        })
        
        # Save to Excel file
        sample_file_path = os.path.join(os.path.dirname(__file__), 'sample_crs_data.xlsx')
        
        with pd.ExcelWriter(sample_file_path, engine='openpyxl') as writer:
            sample_country_data.to_excel(writer, sheet_name='CountryCode', index=False)
            sample_account_data.to_excel(writer, sheet_name='AccountReport', index=False)
            sample_message_data.to_excel(writer, sheet_name='MessageSpec', index=False)
        
        print(f"✅ Sample Excel file created: {sample_file_path}")
        print(f"   - CountryCode sheet: {len(sample_country_data)} records")
        print(f"   - AccountReport sheet: {len(sample_account_data)} records")
        print(f"   - MessageSpec sheet: {len(sample_message_data)} records")
        
        return sample_file_path
        
    except Exception as e:
        print(f"❌ Error creating sample Excel file: {e}")
        return None

def main():
    """Main test function"""
    print("=" * 80)
    print("CRS DATA SETUP - WINDOWS AUTHENTICATION TEST")
    print("=" * 80)
    
    # Test 1: Direct database connection with Windows auth
    print("\n1. Testing direct database connections with Windows authentication...")
    db_success, working_config = test_database_connection()
    
    if working_config:
        print(f"\n✅ Working configuration found:")
        print(f"   Server: {working_config['server']}")
        print(f"   Database: {working_config['database']}")
        print(f"   Auth Type: {working_config['auth_type']}")
    
    # Test 2: CRS setup module connection
    print("\n2. Testing CRS setup module connection...")
    crs_success = test_using_crs_setup()
    
    # Test 3: Check existing tables
    print("\n3. Checking for existing CRS tables...")
    tables_exist = check_existing_tables()
    
    # Test 4: Excel file handling
    print("\n4. Testing Excel file handling...")
    
    # Ask user for Excel file or create sample
    excel_file = input("\nEnter path to your Excel file (or press Enter to create sample): ").strip()
    
    if not excel_file:
        print("Creating sample Excel file...")
        excel_file = create_sample_excel_file()
        if not excel_file:
            print("❌ Failed to create sample Excel file")
            return
    
    excel_success = test_excel_loading(excel_file)
    
    # Test summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"✅ Direct DB connection: {'PASS' if db_success else 'FAIL'}")
    print(f"✅ CRS module connection: {'PASS' if crs_success else 'FAIL'}")
    print(f"✅ Excel file loading: {'PASS' if excel_success else 'FAIL'}")
    print(f"📊 Existing CRS tables: {'Found' if tables_exist else 'Not found'}")
    
    if working_config:
        print(f"\n🔧 Recommended configuration:")
        print(f"   Server: {working_config['server']}")
        print(f"   Auth Type: Windows")
    
    if db_success and excel_success:
        print("\n🎉 All tests passed! You can now run the main CRS data setup script.")
        print(f"   Command: python crs_data_setup.py")
        if excel_file and 'sample_crs_data.xlsx' in excel_file:
            print(f"   Sample file created: {excel_file}")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        
        if not db_success:
            print("\n🔧 Database connection troubleshooting:")
            print("   1. Make sure SQL Server is running")
            print("   2. Check Windows authentication is enabled")
            print("   3. Verify your Windows user has access to SQL Server")
            print("   4. Try different server names (localhost\\SQLEXPRESS, .\\SQLEXPRESS, localhost)")

if __name__ == "__main__":
    main()
