# CRS Data Setup

This directory contains scripts for setting up CRS (Common Reporting Standard) tables in SQL Server and loading data from Excel files.

## Files

- `crs_data_setup.py` - Main script for creating CRS tables and loading data
- `test_crs_setup.py` - Test script to verify setup and connection
- `sql_connector.py` - Database connection utilities (existing)
- `transaction_history_setup.py` - Example script (existing)

## Prerequisites

1. SQL Server instance running (local or remote)
2. Python environment with required packages:
   ```bash
   pip install pandas pyodbc openpyxl python-dotenv
   ```
3. Environment variables configured (see `.env` setup below)
4. Excel file with CRS data in specific sheets

## Environment Setup

Create a `.env` file in the project root with your database connection details:

```env
# SQL Server Connection
server_data_studio=localhost,1433
database=master
auth_type=sql
username=SA
password=YourPassword123!
```

## Excel File Format

Your Excel file should contain three sheets with the following names:

### 1. CountryCode Sheet
Columns:
- CountryShortCode (e.g., "ZA", "US")
- Country (e.g., "South Africa", "United States")
- Country2 (alternative name)
- Country3 (another alternative name)

### 2. AccountReport Sheet
Columns should match the CRS_GH_AccountReport table structure:
- ParentID, DocTypeIndic2, DocRefId3, AccountNumber, AccNumberType
- ClosedAccount, DormantAccount, UndocumentedAccount, ResCountryCode4
- AcctHolderType, nameType, FirstName, LastName, MiddleName
- CountryCode5, Street, PostCode, City, BirthDate
- TIN6, issuedBy7, AccountBalance, currCode, Type
- PaymentAmnt, currCode8, Processed

### 3. MessageSpec Sheet
Columns should match the CRS_GH_MessageSpec table structure:
- ParentID, version, SendingCompanyIN, TransmittingCountry
- ReceivingCountry, MessageType, MessageRefId, MessageTypeIndic
- ReportingPeriod, Timestamp, ResCountryCode, TIN, issuedBy
- Name, CountryCode, AddressFree, DocTypeIndic, DocRefId, Processed

## Usage

### Method 1: Interactive Setup
```bash
cd db
python crs_data_setup.py
```

Follow the prompts to:
1. Select database environment
2. Provide Excel file path
3. Monitor the data loading process

### Method 2: Quick Setup (Automated)
```bash
cd db
python crs_data_setup.py quick "path/to/your/excel_file.xlsx" from_env
```

### Method 3: Test First
```bash
cd db
python test_crs_setup.py
```

This will:
- Test database connection
- Check for existing tables
- Validate Excel file format
- Create a sample Excel file if needed

## Database Schema

The script creates the following tables:

### Ref Schema
- `[Ref].[CRS_CountryCode]` - Country reference data

### DATA Schema  
- `[DATA].[CRS_GH_AccountReport]` - Account reporting data
- `[DATA].[CRS_GH_MessageSpec]` - Message specification data

## Features

- ✅ Automatic schema creation (Ref and DATA)
- ✅ Table creation with proper SQL Server data types
- ✅ Batch data insertion with error handling
- ✅ Data validation and verification
- ✅ Support for multiple database environments
- ✅ Excel file validation
- ✅ Sample data generation for testing
- ✅ Comprehensive error reporting

## Troubleshooting

### Connection Issues
1. Verify SQL Server is running
2. Check connection string in `.env` file
3. Ensure SQL Server allows remote connections
4. Verify authentication method (Windows vs SQL)

### Excel Issues
1. Ensure Excel file has correct sheet names
2. Check column names match expected format
3. Verify file is not password protected
4. Use `.xlsx` format (not `.xls`)

### Data Issues
1. Check for null values in required fields
2. Verify data types match table schema
3. Look for special characters in text fields
4. Check date formats

## Example Output

```
================================================================================
CRS DATA SETUP - TABLE CREATION AND DATA LOADING
================================================================================

🔄 Connecting to database using 'from_env' configuration...
   Server: localhost,1433
   Database: master
   Auth Type: sql

✅ Database connection successful
🔍 Checking and creating schemas...
✅ Schemas checked/created successfully
🔨 Creating CRS tables...
✅ Created table: [Ref].[CRS_CountryCode]
✅ Created table: [DATA].[CRS_GH_AccountReport]
✅ Created table: [DATA].[CRS_GH_MessageSpec]
✅ All CRS tables created successfully

📁 Loading Excel file: sample_crs_data.xlsx
📊 Found 3 sheets in Excel file:
   - CountryCode: 5 rows, 4 columns
   - AccountReport: 3 rows, 27 columns
   - MessageSpec: 2 rows, 19 columns

📥 Inserting 5 records into [Ref].[CRS_CountryCode]...
✅ Successfully inserted 5 records into [Ref].[CRS_CountryCode]

📥 Inserting 3 records into [DATA].[CRS_GH_AccountReport]...
✅ Successfully inserted 3 records into [DATA].[CRS_GH_AccountReport]

📥 Inserting 2 records into [DATA].[CRS_GH_MessageSpec]...
✅ Successfully inserted 2 records into [DATA].[CRS_GH_MessageSpec]

🔍 Verifying data insertion...
   CountryCode: 5 records
   AccountReport: 3 records
   MessageSpec: 2 records

📊 Total records across all tables: 10

================================================================================
🎉 CRS DATA SETUP COMPLETED
================================================================================
📊 Total records inserted: 10
📊 Total records verified: 10
🗃️  Tables created: 3
🔗 Database: master
🖥️  Server: localhost,1433
✅ All data inserted and verified successfully!
```

## Support

If you encounter issues:
1. Run the test script first: `python test_crs_setup.py`
2. Check the error logs for specific issues
3. Verify your Excel file format matches the expected schema
4. Ensure database permissions are correct
