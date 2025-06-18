"""
CRS Data Setup Script
This script creates CRS tables in SQL Server and populates them with data from Excel sheets.
Uses pyodbc for SQL Server connectivity and pandas for Excel data handling.
"""

import os
import sys
import warnings
import traceback
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Load environment variables
load_dotenv(find_dotenv())

# Import the improved SQL connector
from sql_connector import connect_to_sql_server

# =============================================================================
# CONFIGURATION SECTION - Update these settings as needed
# =============================================================================
CONFIG = {
    # Database connection settings - Default to Windows authentication for local development
    'server': 'localhost\\SQLEXPRESS',  # Default Windows SQL Server Express
    'database': 'master',        # Default database
    'auth_type': 'windows',      # 'windows' or 'sql' - Windows auth is default for local SQL Express
    'username': None,            # Not needed for Windows auth
    'password': None,            # Not needed for Windows auth
    
    # Alternative configurations for different environments
    'environments': {
        'local_docker': {
            'server': 'localhost,1433',
            'database': 'master',
            'auth_type': 'sql',
            'username': 'SA',
            'password': os.environ.get("password")
        },
        'local_windows': {
            'server': 'localhost\\SQLEXPRESS',
            'database': 'master',
            'auth_type': 'windows',
            'username': None,
            'password': None
        },
        'local_windows_named': {
            'server': '.\\SQLEXPRESS',  # Alternative server name format
            'database': 'master',
            'auth_type': 'windows',
            'username': None,
            'password': None
        },
        'from_env': {
            'server': os.environ.get("server_data_studio", "localhost\\SQLEXPRESS"),
            'database': os.environ.get("database", "master"),
            'auth_type': os.environ.get("auth_type", "windows"),  # Default to windows auth
            'username': os.environ.get("username"),
            'password': os.environ.get("password")
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

def create_schemas_if_not_exist(cursor):
    """Create the Ref and DATA schemas if they don't exist"""
    try:
        print("🔍 Checking and creating schemas...")
        
        # Create Ref schema
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'Ref')
        BEGIN
            EXEC('CREATE SCHEMA [Ref]')
            PRINT 'Created Ref schema'
        END
        ELSE
            PRINT 'Ref schema already exists'
        """)
        
        # Create DATA schema
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'DATA')
        BEGIN
            EXEC('CREATE SCHEMA [DATA]')
            PRINT 'Created DATA schema'
        END
        ELSE
            PRINT 'DATA schema already exists'
        """)
        
        cursor.commit()
        print("✅ Schemas checked/created successfully")
        
    except Exception as e:
        print(f"❌ Error creating schemas: {e}")
        raise

def create_crs_tables(cursor):
    """Create all CRS tables in SQL Server"""
    try:
        print("🔨 Creating CRS tables...")
        
        # Drop tables if they exist (for clean setup)
        tables_to_drop = [
            "[Ref].[CRS_CountryCode]",
            "[DATA].[CRS_GH_AccountReport]", 
            "[DATA].[CRS_GH_MessageSpec]"
        ]
        
        for table in tables_to_drop:
            cursor.execute(f"""
            IF OBJECT_ID(N'{table}', N'U') IS NOT NULL
                DROP TABLE {table}
            """)
        
        # Create CRS_CountryCode table
        cursor.execute("""
        CREATE TABLE [Ref].[CRS_CountryCode](
            [CountryShortCode] [nvarchar](2) NULL,
            [Country] [nvarchar](50) NULL,
            [Country2] [nvarchar](50) NULL,
            [Country3] [nvarchar](50) NULL
        )
        """)
        print("✅ Created table: [Ref].[CRS_CountryCode]")
        
        # Create CRS_GH_AccountReport table  
        cursor.execute("""
        CREATE TABLE [DATA].[CRS_GH_AccountReport](
            [ParentID] [varchar](255) NULL,
            [DocTypeIndic2] [varchar](255) NULL,
            [DocRefId3] [varchar](255) NULL,
            [AccountNumber] [varchar](255) NULL,
            [AccNumberType] [varchar](255) NULL,
            [ClosedAccount] [varchar](255) NULL,
            [DormantAccount] [varchar](255) NULL,
            [UndocumentedAccount] [varchar](255) NULL,
            [ResCountryCode4] [varchar](255) NULL,
            [AcctHolderType] [varchar](255) NULL,
            [nameType] [varchar](255) NULL,
            [FirstName] [varchar](255) NULL,
            [LastName] [varchar](255) NULL,
            [MiddleName] [varchar](255) NULL,
            [CountryCode5] [varchar](255) NULL,
            [Street] [varchar](255) NULL,
            [PostCode] [varchar](255) NULL,
            [City] [varchar](255) NULL,
            [BirthDate] [varchar](255) NULL,
            [TIN6] [varchar](255) NULL,
            [issuedBy7] [varchar](255) NULL,
            [AccountBalance] [varchar](255) NULL,
            [currCode] [varchar](255) NULL,
            [Type] [varchar](255) NULL,
            [PaymentAmnt] [varchar](255) NULL,
            [currCode8] [varchar](255) NULL,
            [Processed] [bit] NULL
        )
        """)
        print("✅ Created table: [DATA].[CRS_GH_AccountReport]")
        
        # Create CRS_GH_MessageSpec table
        cursor.execute("""
        CREATE TABLE [DATA].[CRS_GH_MessageSpec](
            [ParentID] [varchar](255) NULL,
            [version] [varchar](255) NULL,
            [SendingCompanyIN] [varchar](255) NULL,
            [TransmittingCountry] [varchar](255) NULL,
            [ReceivingCountry] [varchar](255) NULL,
            [MessageType] [varchar](255) NULL,
            [MessageRefId] [varchar](255) NULL,
            [MessageTypeIndic] [varchar](255) NULL,
            [ReportingPeriod] [varchar](255) NULL,
            [Timestamp] [varchar](255) NULL,
            [ResCountryCode] [varchar](255) NULL,
            [TIN] [varchar](255) NULL,
            [issuedBy] [varchar](255) NULL,
            [Name] [varchar](255) NULL,
            [CountryCode] [varchar](255) NULL,
            [AddressFree] [varchar](255) NULL,
            [DocTypeIndic] [varchar](255) NULL,
            [DocRefId] [varchar](255) NULL,
            [Processed] [bit] NULL
        )
        """)
        print("✅ Created table: [DATA].[CRS_GH_MessageSpec]")
        
        cursor.commit()
        print("✅ All CRS tables created successfully")
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        traceback.print_exc()
        raise

def load_excel_file(file_path):
    """Load Excel file and return dictionary of DataFrames for each sheet"""
    try:
        print(f"📁 Loading Excel file: {file_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Excel file not found: {file_path}")
        
        # Read all sheets from Excel file
        excel_data = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
        
        print(f"📊 Found {len(excel_data)} sheets in Excel file:")
        for sheet_name in excel_data.keys():
            rows, cols = excel_data[sheet_name].shape
            print(f"   - {sheet_name}: {rows} rows, {cols} columns")
        
        return excel_data
        
    except Exception as e:
        print(f"❌ Error loading Excel file: {e}")
        raise

def clean_dataframe_for_sql(df):
    """Clean DataFrame for SQL insertion"""
    # Replace NaN values with None (which becomes NULL in SQL)
    df = df.where(pd.notnull(df), None)
    
    # Convert any datetime columns to string format
    for col in df.columns:
        if df[col].dtype == 'datetime64[ns]':
            df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
            df[col] = df[col].where(df[col] != 'NaT', None)
    
    return df

def insert_countrycode_data(conn, cursor, df):
    """Insert data into CRS_CountryCode table"""
    try:
        print(f"📥 Inserting {len(df)} records into [Ref].[CRS_CountryCode]...")
        
        # Clean the DataFrame
        df_clean = clean_dataframe_for_sql(df)
        
        # Map DataFrame columns to table columns
        # Adjust column mapping based on your Excel sheet structure
        column_mapping = {
            # Excel column name -> SQL column name
            # Update these based on your actual Excel column names
            0: 'CountryShortCode',  # Assuming first column is short code
            1: 'Country',           # Assuming second column is country name
            2: 'Country2',          # Adjust as needed
            3: 'Country3'           # Adjust as needed
        }
        
        insert_query = """
        INSERT INTO [Ref].[CRS_CountryCode] 
        ([CountryShortCode], [Country], [Country2], [Country3])
        VALUES (?, ?, ?, ?)
        """
        
        success_count = 0
        error_count = 0
        
        for index, row in df_clean.iterrows():
            try:
                # Extract values based on column mapping or by position
                if len(df_clean.columns) >= 4:
                    values = (
                        row.iloc[0] if pd.notnull(row.iloc[0]) else None,  # CountryShortCode
                        row.iloc[1] if pd.notnull(row.iloc[1]) else None,  # Country
                        row.iloc[2] if pd.notnull(row.iloc[2]) else None,  # Country2
                        row.iloc[3] if pd.notnull(row.iloc[3]) else None   # Country3
                    )
                else:
                    # Handle case where Excel has fewer columns
                    values = tuple(row.iloc[i] if i < len(row) and pd.notnull(row.iloc[i]) else None for i in range(4))
                
                cursor.execute(insert_query, values)
                success_count += 1
                
                if success_count % 100 == 0:
                    conn.commit()
                    print(f"   Inserted {success_count} records...")
                    
            except Exception as e:
                error_count += 1
                print(f"   Error inserting row {index}: {e}")
                if error_count > 10:  # Stop if too many errors
                    print("   Too many errors, stopping insertion...")
                    break
        
        conn.commit()
        print(f"✅ Successfully inserted {success_count} records into [Ref].[CRS_CountryCode]")
        if error_count > 0:
            print(f"⚠️  {error_count} records failed to insert")
        
        return success_count
        
    except Exception as e:
        print(f"❌ Error inserting CountryCode data: {e}")
        traceback.print_exc()
        return 0

def insert_accountreport_data(conn, cursor, df):
    """Insert data into CRS_GH_AccountReport table"""
    try:
        print(f"📥 Inserting {len(df)} records into [DATA].[CRS_GH_AccountReport]...")
        
        # Clean the DataFrame
        df_clean = clean_dataframe_for_sql(df)
        
        # Get the column names from the DataFrame
        columns = list(df_clean.columns)
        
        # Build dynamic insert query based on available columns
        # Map Excel columns to SQL columns (you may need to adjust this mapping)
        sql_columns = [
            'ParentID', 'DocTypeIndic2', 'DocRefId3', 'AccountNumber', 'AccNumberType',
            'ClosedAccount', 'DormantAccount', 'UndocumentedAccount', 'ResCountryCode4',
            'AcctHolderType', 'nameType', 'FirstName', 'LastName', 'MiddleName',
            'CountryCode5', 'Street', 'PostCode', 'City', 'BirthDate', 'TIN6',
            'issuedBy7', 'AccountBalance', 'currCode', 'Type', 'PaymentAmnt',
            'currCode8', 'Processed'
        ]
        
        # Build insert query
        column_placeholders = ', '.join(['?' for _ in sql_columns])
        column_names = ', '.join([f'[{col}]' for col in sql_columns])
        
        insert_query = f"""
        INSERT INTO [DATA].[CRS_GH_AccountReport] 
        ({column_names})
        VALUES ({column_placeholders})
        """
        
        success_count = 0
        error_count = 0
        
        for index, row in df_clean.iterrows():
            try:
                # Extract values, handling missing columns
                values = []
                for i, sql_col in enumerate(sql_columns):
                    if i < len(row):
                        value = row.iloc[i] if pd.notnull(row.iloc[i]) else None
                        # Handle boolean conversion for Processed column
                        if sql_col == 'Processed' and value is not None:
                            value = bool(value) if str(value).lower() in ['true', '1', 'yes'] else False
                        values.append(value)
                    else:
                        values.append(None)
                
                cursor.execute(insert_query, tuple(values))
                success_count += 1
                
                if success_count % 100 == 0:
                    conn.commit()
                    print(f"   Inserted {success_count} records...")
                    
            except Exception as e:
                error_count += 1
                print(f"   Error inserting row {index}: {e}")
                if error_count > 10:
                    print("   Too many errors, stopping insertion...")
                    break
        
        conn.commit()
        print(f"✅ Successfully inserted {success_count} records into [DATA].[CRS_GH_AccountReport]")
        if error_count > 0:
            print(f"⚠️  {error_count} records failed to insert")
        
        return success_count
        
    except Exception as e:
        print(f"❌ Error inserting AccountReport data: {e}")
        traceback.print_exc()
        return 0

def insert_messagespec_data(conn, cursor, df):
    """Insert data into CRS_GH_MessageSpec table"""
    try:
        print(f"📥 Inserting {len(df)} records into [DATA].[CRS_GH_MessageSpec]...")
        
        # Clean the DataFrame
        df_clean = clean_dataframe_for_sql(df)
        
        sql_columns = [
            'ParentID', 'version', 'SendingCompanyIN', 'TransmittingCountry',
            'ReceivingCountry', 'MessageType', 'MessageRefId', 'MessageTypeIndic',
            'ReportingPeriod', 'Timestamp', 'ResCountryCode', 'TIN', 'issuedBy',
            'Name', 'CountryCode', 'AddressFree', 'DocTypeIndic', 'DocRefId', 'Processed'
        ]
        
        # Build insert query
        column_placeholders = ', '.join(['?' for _ in sql_columns])
        column_names = ', '.join([f'[{col}]' for col in sql_columns])
        
        insert_query = f"""
        INSERT INTO [DATA].[CRS_GH_MessageSpec] 
        ({column_names})
        VALUES ({column_placeholders})
        """
        
        success_count = 0
        error_count = 0
        
        for index, row in df_clean.iterrows():
            try:
                # Extract values, handling missing columns
                values = []
                for i, sql_col in enumerate(sql_columns):
                    if i < len(row):
                        value = row.iloc[i] if pd.notnull(row.iloc[i]) else None
                        # Handle boolean conversion for Processed column
                        if sql_col == 'Processed' and value is not None:
                            value = bool(value) if str(value).lower() in ['true', '1', 'yes'] else False
                        values.append(value)
                    else:
                        values.append(None)
                
                cursor.execute(insert_query, tuple(values))
                success_count += 1
                
                if success_count % 100 == 0:
                    conn.commit()
                    print(f"   Inserted {success_count} records...")
                    
            except Exception as e:
                error_count += 1
                print(f"   Error inserting row {index}: {e}")
                if error_count > 10:
                    print("   Too many errors, stopping insertion...")
                    break
        
        conn.commit()
        print(f"✅ Successfully inserted {success_count} records into [DATA].[CRS_GH_MessageSpec]")
        if error_count > 0:
            print(f"⚠️  {error_count} records failed to insert")
        
        return success_count
        
    except Exception as e:
        print(f"❌ Error inserting MessageSpec data: {e}")
        traceback.print_exc()
        return 0

def verify_data_insertion(cursor):
    """Verify that data was successfully inserted into all tables"""
    try:
        print("\n🔍 Verifying data insertion...")
        
        tables = [
            ("[Ref].[CRS_CountryCode]", "CountryCode"),
            ("[DATA].[CRS_GH_AccountReport]", "AccountReport"), 
            ("[DATA].[CRS_GH_MessageSpec]", "MessageSpec")
        ]
        
        total_records = 0
        
        for table_name, friendly_name in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            total_records += count
            print(f"   {friendly_name}: {count:,} records")
            
            if count > 0:
                # Show sample data
                cursor.execute(f"SELECT TOP 2 * FROM {table_name}")
                rows = cursor.fetchall()
                print(f"     Sample data from {friendly_name}:")
                for i, row in enumerate(rows):
                    print(f"       Row {i+1}: {str(row)[:100]}{'...' if len(str(row)) > 100 else ''}")
        
        print(f"\n📊 Total records across all tables: {total_records:,}")
        return total_records
        
    except Exception as e:
        print(f"❌ Error verifying data: {e}")
        return 0

def main():
    """Main function to create CRS tables and load data from Excel"""
    print("=" * 80)
    print("CRS DATA SETUP - TABLE CREATION AND DATA LOADING")
    print("=" * 80)
    
    # Choose environment configuration
    print("Available connection environments:")
    print("1. default - Use default configuration")
    print("2. local_docker - Docker SQL Server (localhost,1433)")
    print("3. local_windows - Windows SQL Server Express")
    print("4. from_env - Use environment variables")
    
    while True:
        choice = input("\nSelect environment (1-4) or press Enter for default: ").strip()
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
        else:
            print("Invalid choice. Please select 1-4.")
    
    # Get Excel file path
    while True:
        excel_file = input("\nEnter path to Excel file (or press Enter to browse): ").strip()
        if not excel_file:
            print("Please provide the path to your Excel file with the CRS data")
            print("Expected sheets: AccountReport, MessageSpec, CountryCode")
            continue
        
        if os.path.exists(excel_file):
            break
        else:
            print(f"File not found: {excel_file}")
    
    print(f"\n📊 Configuration Summary:")
    print(f"   Environment: {environment}")
    print(f"   Excel file: {excel_file}")
    
    # Connect to SQL Server
    conn, cursor = setup_database_connection(environment)
    
    if not conn or not cursor:
        print("❌ Failed to connect to database. Please check your configuration.")
        return
    
    try:
        # Create schemas
        create_schemas_if_not_exist(cursor)
        
        # Create tables
        create_crs_tables(cursor)
        
        # Load Excel data
        excel_data = load_excel_file(excel_file)
        
        # Check for required sheets
        required_sheets = ['AccountReport', 'MessageSpec', 'CountryCode']
        available_sheets = list(excel_data.keys())
        
        print(f"\n📋 Available sheets: {available_sheets}")
        print(f"📋 Required sheets: {required_sheets}")
        
        # Insert data from each sheet
        total_inserted = 0
        
        # Insert CountryCode data
        if 'CountryCode' in excel_data:
            count = insert_countrycode_data(conn, cursor, excel_data['CountryCode'])
            total_inserted += count
        else:
            print("⚠️  Warning: CountryCode sheet not found in Excel file")
        
        # Insert AccountReport data
        if 'AccountReport' in excel_data:
            count = insert_accountreport_data(conn, cursor, excel_data['AccountReport'])
            total_inserted += count
        else:
            print("⚠️  Warning: AccountReport sheet not found in Excel file")
        
        # Insert MessageSpec data
        if 'MessageSpec' in excel_data:
            count = insert_messagespec_data(conn, cursor, excel_data['MessageSpec'])
            total_inserted += count
        else:
            print("⚠️  Warning: MessageSpec sheet not found in Excel file")
        
        # Verify data insertion
        verified_count = verify_data_insertion(cursor)
        
        print("\n" + "=" * 80)
        print("🎉 CRS DATA SETUP COMPLETED")
        print("=" * 80)
        print(f"📊 Total records inserted: {total_inserted:,}")
        print(f"📊 Total records verified: {verified_count:,}")
        print(f"🗃️  Tables created: 3")
        print(f"🔗 Database: {get_connection_config(environment)['database']}")
        print(f"🖥️  Server: {get_connection_config(environment)['server']}")
        
        if verified_count == total_inserted:
            print("✅ All data inserted and verified successfully!")
        else:
            print("⚠️  Data count mismatch - please check for insertion errors")
        
    except Exception as e:
        print(f"\n❌ Error during CRS data setup: {e}")
        traceback.print_exc()
    finally:
        # Close SQL Server connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("\n🔐 Database connection closed")

def quick_setup(environment='local_docker', excel_file_path=None):
    """
    Quick setup function for automated execution.
    
    Args:
        environment (str): Environment configuration to use
        excel_file_path (str): Path to Excel file with CRS data
    
    Returns:
        bool: True if successful, False otherwise
    """
    print(f"🚀 QUICK SETUP: {environment} environment")
    
    if not excel_file_path or not os.path.exists(excel_file_path):
        print("❌ Valid Excel file path required for quick setup")
        return False
    
    try:
        # Connect to database
        conn, cursor = setup_database_connection(environment)
        if not conn or not cursor:
            print("❌ Database connection failed")
            return False
        
        # Create schemas and tables
        create_schemas_if_not_exist(cursor)
        create_crs_tables(cursor)
        
        # Load and insert data
        excel_data = load_excel_file(excel_file_path)
        
        total_inserted = 0
        if 'CountryCode' in excel_data:
            total_inserted += insert_countrycode_data(conn, cursor, excel_data['CountryCode'])
        if 'AccountReport' in excel_data:
            total_inserted += insert_accountreport_data(conn, cursor, excel_data['AccountReport'])
        if 'MessageSpec' in excel_data:
            total_inserted += insert_messagespec_data(conn, cursor, excel_data['MessageSpec'])
        
        # Verify
        verified_count = verify_data_insertion(cursor)
        
        # Cleanup
        cursor.close()
        conn.close()
        
        print(f"✅ Quick setup completed: {total_inserted} records inserted, {verified_count} verified")
        return verified_count > 0
        
    except Exception as e:
        print(f"❌ Quick setup failed: {e}")
        return False

if __name__ == "__main__":
    # Check for command line arguments for automated usage
    if len(sys.argv) > 1:
        if sys.argv[1] == "quick" and len(sys.argv) > 2:
            excel_path = sys.argv[2]
            environment = sys.argv[3] if len(sys.argv) > 3 else 'local_docker'
            quick_setup(environment, excel_path)
        else:
            print("Usage: python crs_data_setup.py [quick <excel_file_path> [environment]]")
    else:
        main()
