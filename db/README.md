# SQL Server Database Setup & Connection Scripts

This directory contains scripts to create and populate SQL Server tables with synthetic data using cross-platform connection methods.

## Files

1. **sql_connector.py** - Cross-platform SQL Server connection module with authentication fallback
2. **test_sql_connection.py** - Comprehensive connection testing script
3. **transaction_history_setup.py** - Transaction data generator and table setup
4. **sql_server_setup.py** - Customer data generator (legacy)
5. **generate_sql_data.py** - Original data generation script

## Prerequisites

### 1. SQL Server Installation

#### Windows
- **SQL Server Express** (free): Download from Microsoft
- **SQL Server Developer Edition** (free): Full-featured for development
- **Docker**: `docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=YourStrongPassword123" -p 1433:1433 --name sqlserver -d mcr.microsoft.com/mssql/server:2019-latest`

#### macOS/Linux
- **Docker** (recommended): 
  ```bash
  docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=YourStrongPassword123" -p 1433:1433 --name sqlserver -d mcr.microsoft.com/mssql/server:2019-latest
  ```
- **Azure SQL Database**: Cloud-based option

### 2. Python Environment Setup

⚠️ **Important for macOS Users**: Use **local Python virtual environment** instead of Anaconda/Conda environments for better ODBC driver compatibility.

#### Recommended Setup (macOS & Windows)
```bash
# Create local Python virtual environment (NOT conda)
python3 -m venv sql_env
source sql_env/bin/activate  # macOS/Linux
# OR
sql_env\Scripts\activate     # Windows

# Install required packages
pip install -r requirements.txt
```

#### Why Not Anaconda/Conda on macOS?
- Conda environments can have ODBC driver path conflicts
- System-level ODBC drivers may not be accessible from conda environments
- Local venv uses system Python, ensuring proper driver access

### 3. ODBC Driver Installation

#### Windows
```powershell
# Download and install Microsoft ODBC Driver for SQL Server
# Option 1: Download from Microsoft website
# https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

# Option 2: Using winget (Windows 10/11)
winget install Microsoft.ODBCDriverforSQLServer

# Option 3: Using chocolatey
choco install sqlserver-odbcdriver

# Verify installation
Get-OdbcDriver | Where-Object {$_.Name -like "*SQL Server*"}
```

#### macOS
```bash
# Install Microsoft ODBC Driver 17 or 18 for SQL Server
# Method 1: Using Homebrew (recommended)
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
brew install msodbcsql17

# Method 2: Manual installation
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/ubuntu/20.04/prod focal main" > /etc/apt/sources.list.d/mssql-release.list'

# For Apple Silicon Macs (M1/M2), you might need:
arch -x86_64 brew install msodbcsql17

# Verify installation
odbcinst -q -d -n "ODBC Driver 17 for SQL Server"
```

#### Linux (Ubuntu/Debian)
```bash
# Add Microsoft repository
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

# Install driver
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Verify installation
odbcinst -q -d
```

### 4. Python Package Installation

```bash
# Core packages
pip install pyodbc pandas faker python-dotenv

# Optional packages for enhanced functionality
pip install sqlalchemy jupyter notebook

# Create requirements.txt
cat > requirements.txt << EOF
pyodbc>=4.0.35
pandas>=1.5.0
faker>=15.0.0
python-dotenv>=0.19.0
sqlalchemy>=1.4.0
warnings
os
sys
platform
datetime
EOF
```

### 5. Environment Configuration

Create a `.env` file in the project root:
```bash
# .env file
password=YourStrongPassword123
server_data_studio=localhost,1433
database=master
auth_type=sql
username=SA
```

## Debugging ODBC Driver Issues

### macOS Debugging Guide

#### Check Available Drivers
```bash
# List all ODBC drivers
odbcinst -q -d

# Check specific SQL Server drivers
odbcinst -q -d -n "ODBC Driver 17 for SQL Server"
odbcinst -q -d -n "ODBC Driver 18 for SQL Server"

# Python check
python -c "import pyodbc; print(pyodbc.drivers())"
```

#### Common macOS Issues & Solutions

1. **Driver Not Found Error**
```python
# Error: ('01000', "[01000] [unixODBC][Driver Manager]Can't open lib...")
```
**Solution:**
```bash
# Reinstall with Homebrew
brew uninstall msodbcsql17
brew install msodbcsql17

# Or try manual path fix
export DYLD_LIBRARY_PATH=/usr/local/lib:$DYLD_LIBRARY_PATH
```

2. **Anaconda/Conda Environment Issues**
```bash
# Don't use conda for this project
conda deactivate

# Use system Python instead
python3 -m venv sql_env
source sql_env/bin/activate
pip install pyodbc
```

3. **Apple Silicon (M1/M2) Issues**
```bash
# Install using x86_64 architecture
arch -x86_64 brew install msodbcsql17

# Or use Rosetta for Python
arch -x86_64 python3 -m venv sql_env
source sql_env/bin/activate
pip install pyodbc
```

4. **Permission Issues**
```bash
# Fix ODBC configuration file permissions
sudo chmod 644 /etc/odbcinst.ini
sudo chmod 644 /etc/odbc.ini
```

#### Testing Driver Installation
```python
# test_driver.py
import pyodbc

print("Available ODBC drivers:")
for driver in pyodbc.drivers():
    print(f"  - {driver}")

# Test specific driver
try:
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost,1433;"
        "DATABASE=master;"
        "UID=SA;"
        "PWD=YourPassword123;"
        "TrustServerCertificate=Yes;"
        "Encrypt=no;"
    )
    conn = pyodbc.connect(conn_str, timeout=5)
    print("✓ Driver working correctly!")
    conn.close()
except Exception as e:
    print(f"✗ Driver issue: {e}")
```

### Windows Debugging Guide

#### Check Available Drivers
```powershell
# PowerShell - List ODBC drivers
Get-OdbcDriver | Where-Object {$_.Name -like "*SQL*"}

# Command Prompt
odbcad32.exe  # Opens ODBC Data Source Administrator

# Python check
python -c "import pyodbc; print(pyodbc.drivers())"
```

#### Common Windows Issues & Solutions

1. **32-bit vs 64-bit Driver Mismatch**
```bash
# Ensure Python architecture matches ODBC driver architecture
python -c "import platform; print(platform.architecture())"

# Install matching driver version
# 64-bit Python needs 64-bit ODBC driver
# 32-bit Python needs 32-bit ODBC driver
```

2. **Missing Visual C++ Redistributables**
```powershell
# Install Visual C++ Redistributable
# Download from Microsoft website or use:
winget install Microsoft.VCRedist.2015+.x64
```

## Usage Examples

### Quick Connection Test
```bash
# Test connection with default settings
python test_sql_connection.py

# Test specific configuration
python -c "
from sql_connector import connect_to_sql_server
conn, cursor = connect_to_sql_server('localhost,1433', 'master', 'sql', 'SA', 'YourPassword')
if conn: print('✓ Connected successfully')
"
```

### Generate Customer Data
```bash
# Generate customer data table
python sql_server_setup.py

# Generate transaction history
python transaction_history_setup.py
```

### Interactive Setup
```python
# Use the interactive setup for custom configurations
from transaction_history_setup import main
main()  # Follow the prompts
```

## Troubleshooting Checklist

### Connection Issues
- [ ] SQL Server is running and accessible
- [ ] Firewall allows connections on port 1433
- [ ] Correct server address format (`localhost,1433` vs `localhost\SQLEXPRESS`)
- [ ] Valid credentials (SA user enabled with correct password)
- [ ] Database exists and is accessible

### ODBC Driver Issues
- [ ] ODBC driver installed and registered
- [ ] Python architecture matches driver architecture (32-bit vs 64-bit)
- [ ] Using local Python venv (not conda) on macOS
- [ ] Visual C++ Redistributables installed (Windows)
- [ ] Proper permissions on ODBC configuration files

### Python Environment Issues
- [ ] All required packages installed
- [ ] No conflicting package versions
- [ ] Environment variables set correctly
- [ ] Using compatible Python version (3.7+)

## Performance Tips

1. **Connection Pooling**: For production applications, implement connection pooling
2. **Batch Inserts**: Use batch operations for large data sets
3. **Indexing**: Create appropriate indexes on frequently queried columns
4. **Connection Timeout**: Adjust timeout values based on network conditions

## Security Considerations

1. **Environment Variables**: Store sensitive credentials in `.env` files
2. **SQL Injection**: Use parameterized queries (implemented in scripts)
3. **Encryption**: Enable SSL/TLS for production connections
4. **Least Privilege**: Use dedicated database users with minimal required permissions

## Advanced Configuration

### Custom Connection Strings
```python
# Windows Authentication
conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=server;DATABASE=db;Trusted_Connection=yes;"

# SQL Authentication with encryption
conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=server;DATABASE=db;UID=user;PWD=pass;Encrypt=yes;"

# Connection with specific timeout and SSL settings
conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=server;DATABASE=db;UID=user;PWD=pass;TrustServerCertificate=Yes;Encrypt=no;LoginTimeout=30;"
```

### Environment-Specific Configurations
The scripts support multiple environment configurations:
- `default`: Uses CONFIG settings
- `local_docker`: Docker SQL Server setup
- `local_windows`: Windows SQL Server Express
- `from_env`: Uses environment variables
- `custom`: Interactive configuration

## Support

For issues specific to:
- **ODBC Drivers**: Check Microsoft documentation and GitHub issues
- **pyodbc**: Visit the pyodbc GitHub repository
- **SQL Server**: Microsoft SQL Server documentation
- **Docker SQL Server**: Microsoft SQL Server Docker documentation

Remember: When in doubt on macOS, try using a local Python virtual environment instead of conda/anaconda environments!
