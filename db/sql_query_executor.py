# this script validates and exectues SQL queries against a database.

from pathlib import Path
import sys
import os
src_dir = str(Path(__file__).parent.parent)
sys.path.append(src_dir)

import re
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

try:
    from db.sql_connector import connect_to_sql_server
except ImportError:
    print("Error: Could not import connect_to_sql_server. Ensure the db/sql_connector.py file exists and is correctly implemented.")

def validate_sql_query(query):
    """
    Validates SQL query to ensure it's safe and only contains SELECT statements.
    Returns (is_valid, error_message).
    """
    
    
    # Normalize query - remove comments and extra whitespace
    normalized_query = re.sub(r'--.*', '', query)  # Remove line comments
    normalized_query = re.sub(r'/\*.*?\*/', '', normalized_query, flags=re.DOTALL)  # Remove block comments
    normalized_query = ' '.join(normalized_query.split()).upper()  # Normalize whitespace and convert to uppercase
    
    # List of dangerous SQL keywords that should be blocked
    dangerous_keywords = [
        'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER', 'TRUNCATE',
        'MERGE', 'REPLACE', 'EXEC', 'EXECUTE', 'CALL', 'DECLARE', 
        'GRANT', 'REVOKE', 'COMMIT', 'ROLLBACK', 'SAVEPOINT',
        'BACKUP', 'RESTORE', 'SHUTDOWN',
        'OPENROWSET', 'OPENDATASOURCE'
    ]
    
    # Removed 'SET', 'USE', 'BEGIN', 'TRANSACTION', 'LOCK', 'UNLOCK', 'SHOW', 'DESCRIBE', 'EXPLAIN', 'LOAD', 'OUTFILE', 'INFILE', 'IMPORT', 'EXPORT', 'BULK'
    # as these may appear in legitimate complex queries
    
    # Check for dangerous standalone keywords (with word boundaries)
    for keyword in dangerous_keywords:
        # Look for the keyword as a distinct word (with word boundaries)
        if re.search(r'\b' + keyword + r'\b', normalized_query):
            # Special case for 'SET' which might appear in legitimate contexts like SET ROWCOUNT
            if keyword == 'SET' and (re.search(r'\bSET\s+NOCOUNT\b', normalized_query) or 
                                     re.search(r'\bSET\s+ROWCOUNT\b', normalized_query)):
                continue
            return False, f"Dangerous SQL keyword detected: {keyword}"
    
    # Ensure query starts with SELECT
    if not normalized_query.strip().startswith('SELECT'):
        return False, "Only SELECT statements are allowed"
    
    # Check for suspicious patterns - but be smarter about it
    suspicious_patterns = [
        r';\s*(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)',  # Multiple statements with dangerous operations
        r'UNION.*?(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)',  # Union injection with dangerous operations
        r'--.*;',  # Comment followed by semicolon (potential comment-based SQL injection)
        r'/\*.*?;.*?\*/',  # Block comment containing semicolon
        r'\bXP_\w+',  # Extended stored procedures (potential for privilege escalation)
        r'\bSP_\w+EXEC',  # Stored procedures that might execute dynamic SQL
        r'WAITFOR\s+DELAY',  # Time-based SQL injection technique
        r'CONVERT\s*\(\s*INT\s*,',  # Common in blind SQL injection attempts
        r'@@VERSION',  # Server fingerprinting 
        r'SELECT.*?INTO\s+(?!@)' # Writing to files, but allow INTO for variables
    ]
    
    # Remove overly aggressive patterns:
    # r"'.*?'.*?;" - Was incorrectly flagging legitimate quotes in WHERE clauses
    # r'OR\s+1\s*=\s*1' - Too aggressive, can appear in legitimate conditions
    # r'AND\s+1\s*=\s*1' - Too aggressive, can appear in legitimate conditions
    
    for pattern in suspicious_patterns:
        if re.search(pattern, normalized_query, re.IGNORECASE):
            return False, f"Suspicious SQL pattern detected: {pattern}"
    
    # Additional checks for known SQL injection patterns
    # Check for common SQL injection patterns in a smarter way
    injection_patterns = [
        r"(\bOR|\bAND)\s+['\"]\s*['\"]\s*=",  # OR/AND with empty string comparison
        r"(\bOR|\bAND)\s+\d+\s*=\s*\d+\s+--", # OR/AND with always true condition and comment
        r"(\bOR|\bAND)\s+\w+\s*=\s*\w+\s+--", # OR/AND with condition and comment
        r"(\bOR|\bAND)\s+\d+\s*=\s*\d+\s+/\*", # OR/AND with always true condition and comment block
        r"'\s*;\s*--",  # Single quote followed by semicolon and comment
        r"'\s*;\s*/\*",  # Single quote followed by semicolon and comment block
    ]
    
    for pattern in injection_patterns:
        if re.search(pattern, normalized_query, re.IGNORECASE):
            return False, f"SQL injection pattern detected: {pattern}"
    
    # If a query passes all these checks, it's likely safe
    return True, "Query is valid"

def execute_multiple_sql_code(sql_code, connection=None):
    """
    Accepts a string containing one or more SQL queries, each enclosed in triple backticks.
    Executes each query sequentially and stores the results in a list.
    
    Parameters:
    - sql_code: String containing SQL queries in ```sql code blocks
    - connection: Database connection object (pyodbc connection)
    
    Returns a list of results (SELECT returns DataFrame as JSON, validation errors return error messages).
    """
    
    if connection is None:
        # Try to establish a connection if none is provided
        connection, cursor = connect_to_sql_server()
        
        if connection is None:
            return [{"query": "", "result": "Error: No database connection provided", "status": "connection_error"}]
    
    # Extract SQL queries from code blocks
    queries = re.findall(r'```\s*sql\s*(.*?)```', sql_code, re.DOTALL) or re.findall(r'```(.*?)```', sql_code, re.DOTALL)
    
    if not queries:
        return [{"query": sql_code, 
                "result": "No SQL queries found in the provided code. Please format queries in ```sql code blocks.",
                "status": "format_error"}]
    
    results = []
    
    for query_idx, query in enumerate(queries):
        query = query.strip()
        if not query:
            results.append({
                "query": "", 
                "result": f"Empty query found in code block #{query_idx+1}",
                "status": "validation_error"
            })
            continue
            
        # Validate the query first
        is_valid, validation_message = validate_sql_query(query)
        
        if not is_valid:
            results.append({
                "query": query, 
                "result": f"Query validation failed: {validation_message}",
                "status": "validation_error"
            })
            continue
        
        try:
            print(f"Running Query #{query_idx+1} ______________________")
            print(f"Executing query: {query[:100]}{'...' if len(query) > 100 else ''}")
            print("\n")
            
            # Execute query using pandas read_sql_query
            df = pd.read_sql_query(query, connection)
            
            print(f"Query executed successfully - returned {len(df)} rows with {len(df.columns)} columns")
            
            # Handle results
            result_data = {
                "query": query,
                "status": "success",
                "row_count": len(df),
                "column_count": len(df.columns),
                "columns": df.columns.tolist()
            }
            
            # Convert to JSON with error handling
            try:
                result_data["result"] = df.to_json(orient='records', date_format='iso')
            except Exception as json_err:
                result_data["result"] = f"Error converting results to JSON: {str(json_err)}"
                result_data["status"] = "json_error"
                result_data["column_info"] = {col: str(dtype) for col, dtype in df.dtypes.items()}
                
            results.append(result_data)
                
        except Exception as e:
            results.append({
                "query": query, 
                "result": f"Error executing SQL: {str(e)}",
                "status": "execution_error"
            })
    
    return results

def execute_sql_with_pyodbc(sql_code, server=None, database=None, auth_type='sql', username=None, password=None):
    """
    Execute SQL queries using pyodbc with the connect_to_sql_server function.
    
    Parameters:
    - sql_code: String containing SQL queries in ```sql code blocks
    - server: Server name (defaults to environment variable)
    - database: Database name (defaults to environment variable)
    - auth_type: Authentication type ('windows' or 'sql')
    - username: SQL Server login username (if using SQL auth)
    - password: SQL Server login password (if using SQL auth)
    
    Returns a list of query results.
    """
    
    # Use connect_to_sql_server to establish a connection
    connection, cursor = connect_to_sql_server(
        server=server,
        database=database,
        auth_type=auth_type,
        username=username,
        password=password
    )
    
    # If no connection could be established
    if connection is None:
        return [{"query": "", 
                "result": "Could not connect to SQL Server. Check server settings and credentials.", 
                "status": "connection_error"}]
    
    # Now process SQL queries
    try:
        # Extract SQL queries from code blocks
        queries = re.findall(r'```\s*sql\s*(.*?)```', sql_code, re.DOTALL) or re.findall(r'```(.*?)```', sql_code, re.DOTALL)
        
        if not queries:
            connection.close()
            return [{"query": sql_code, 
                    "result": "No SQL queries found in the provided code. Please format queries in ```sql code blocks.",
                    "status": "format_error"}]
        
        # Use the existing execute_multiple_sql_code function since it already has all the needed logic
        results = execute_multiple_sql_code(sql_code, connection)
        
        return results
    
    finally:
        # Ensure connection is closed regardless of success or error
        if connection:
            connection.close()

# example usage
if __name__ == "__main__":
    # Example SQL code with multiple queries
    sql_code = """
    ```sql
    SELECT top 10 * 
    FROM [master].[dbo].[transaction_history] WITH (NOLOCK);
    ```
    
    ```sql
    SELECT COUNT(*) FROM [master].[dbo].[transaction_history] WITH (NOLOCK);
    ```
    
    ```sql
    SELECT TOP 100 * 
    FROM [master].[dbo].[customer_information] WITH (NOLOCK);
    ```
    """
    
    results = execute_sql_with_pyodbc(sql_code)
    
    for result in results:
        
        print(f"Query: {result['query']}")
        # print(f"Result: {result['result']}")
        print(f"Status: {result['status']}")
        print("-" * 50)
        print("\n\n")

