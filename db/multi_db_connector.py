import pyodbc
import os
import platform
import dotenv
from typing import Dict, List, Tuple, Optional, Any
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

class MultiDatabaseConnector:
    """
    A comprehensive class for managing multiple simultaneous database connections
    across different servers and databases.
    """
    
    def __init__(self):
        self.connections = {}
        self.connection_lock = threading.Lock()
        self.current_platform = platform.system().lower()
        self._load_environment_variables()
    
    def _load_environment_variables(self):
        """Load environment variables from various .env file locations."""
        env_locations = [
            os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'),  # Project root .env
            os.path.join(os.path.dirname(__file__), '.env'),  # Current directory .env
            os.path.join(os.path.expanduser('~'), '.env')    # User home directory .env
        ]
        
        for env_path in env_locations:
            if os.path.exists(env_path):
                dotenv.load_dotenv(env_path)
                print(f"Loaded environment variables from {env_path}")
                return
        
        print("No .env file found. Will use provided parameters or defaults.")
    
    def get_available_odbc_drivers(self):
        """Get list of available SQL Server ODBC drivers, prioritized by version."""
        try:
            all_drivers = pyodbc.drivers()
            sql_drivers = [d for d in all_drivers if 'SQL Server' in d]
            
            if not sql_drivers:
                print("Warning: No SQL Server ODBC drivers found. Install ODBC drivers for SQL Server.")
                print("macOS: brew install msodbcsql17 or brew install msodbcsql18")
                return []
                
            # Priority order for drivers
            driver_priority = [
                'ODBC Driver 18 for SQL Server',
                'ODBC Driver 17 for SQL Server',
                'SQL Server Native Client 11.0',
                'SQL Server Native Client 10.0',
                'SQL Server'
            ]
            
            # Sort drivers by priority
            prioritized_drivers = []
            for preferred in driver_priority:
                if preferred in sql_drivers:
                    prioritized_drivers.append(preferred)
            
            # Add any remaining drivers
            for driver in sql_drivers:
                if driver not in prioritized_drivers:
                    prioritized_drivers.append(driver)
                    
            return prioritized_drivers
        except Exception as e:
            print(f"Error detecting ODBC drivers: {e}")
            return []
    
    def build_connection_string(self, driver, server, database, auth_type, username=None, password=None):
        """Build connection string based on authentication type and platform."""
        base_str = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};"
        
        if auth_type == 'windows':
            return base_str + "Trusted_Connection=yes;"
        elif auth_type == 'sql':
            if not username or not password:
                raise ValueError("Username and password required for SQL authentication")
            
            conn_str = base_str + f"UID={username};PWD={password};"
            
            # Add additional parameters for non-Windows platforms
            if self.current_platform != 'windows':
                conn_str += "TrustServerCertificate=Yes;Encrypt=no;LoginTimeout=30;"
            
            return conn_str
        else:
            raise ValueError(f"Invalid authentication type: {auth_type}")
    
    def connect_single_database(self, connection_name, server, database, auth_type='sql', 
                               username=None, password=None):
        """
        Connect to a single database and store the connection.
        
        Args:
            connection_name (str): Unique name for this connection
            server (str): SQL Server instance name
            database (str): Database name
            auth_type (str): Authentication type ('windows' or 'sql')
            username (str, optional): SQL Server login username
            password (str, optional): SQL Server login password
            
        Returns:
            bool: True if connection successful, False otherwise
        """
        # Load from environment if not provided
        server = server or os.environ.get("server_data_studio") or os.environ.get("SERVER")
        database = database or os.environ.get("database") or os.environ.get("DATABASE")
        username = username or os.environ.get("username") or os.environ.get("SQL_USERNAME")
        password = password or os.environ.get("password") or os.environ.get("SQL_PASSWORD")
        
        # Verify required parameters
        if not server or not database:
            print(f"Error: Missing server or database for connection '{connection_name}'")
            return False
        
        # For macOS, SQL auth is the only option
        if self.current_platform == 'darwin' and auth_type.lower() != 'sql':
            print(f"Warning: On macOS, changing auth_type from '{auth_type}' to 'sql' for {connection_name}")
            auth_type = 'sql'
            
        if auth_type.lower() == 'sql' and (not username or not password):
            print(f"Error: SQL authentication requires username and password for {connection_name}")
            return False
        
        # Get available drivers
        available_drivers = self.get_available_odbc_drivers()
        if not available_drivers:
            print(f"Error: No ODBC drivers available for {connection_name}")
            return False
        
        # Try to connect with each driver
        for driver in available_drivers:
            try:
                conn_str = self.build_connection_string(
                    driver, server, database, auth_type, username, password
                )
                
                print(f"Attempting connection '{connection_name}': {auth_type} auth using {driver}")
                
                conn = pyodbc.connect(conn_str, timeout=10)
                cursor = conn.cursor()
                
                # Test the connection
                cursor.execute("SELECT 1")
                cursor.fetchone()
                
                # Store the connection thread-safely
                with self.connection_lock:
                    self.connections[connection_name] = {
                        'connection': conn,
                        'cursor': cursor,
                        'server': server,
                        'database': database,
                        'auth_type': auth_type,
                        'driver': driver
                    }
                
                print(f"✓ Successfully connected '{connection_name}' to {server}/{database}")
                return True
                
            except Exception as e:
                print(f"✗ Failed '{connection_name}' with {driver}: {str(e)}")
                continue
        
        print(f"✗ All connection attempts failed for '{connection_name}'")
        return False
    
    def connect_multiple_databases_same_server(self, server, databases, auth_type='sql', 
                                             username=None, password=None):
        """
        Connect to multiple databases on the same server.
        
        Args:
            server (str): SQL Server instance name
            databases (list): List of database names
            auth_type (str): Authentication type
            username (str, optional): Username
            password (str, optional): Password
            
        Returns:
            dict: Results of connection attempts
        """
        results = {}
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_db = {}
            
            for database in databases:
                connection_name = f"{server.replace(',', '_').replace('.', '_')}_{database}"
                future = executor.submit(
                    self.connect_single_database,
                    connection_name, server, database, auth_type, username, password
                )
                future_to_db[future] = database
            
            for future in as_completed(future_to_db):
                database = future_to_db[future]
                try:
                    success = future.result()
                    results[database] = success
                except Exception as e:
                    results[database] = False
                    print(f"Exception connecting to {database}: {e}")
        
        return results
    
    def connect_multiple_servers(self, server_configs):
        """
        Connect to multiple databases across different servers simultaneously.
        
        Args:
            server_configs (list): List of dictionaries with connection details
                                  Each dict: {name, server, database, auth_type, username, password}
        
        Returns:
            dict: Results of connection attempts
        """
        results = {}
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_config = {}
            
            for config in server_configs:
                connection_name = config.get('name') or f"{config['server']}_{config['database']}"
                future = executor.submit(
                    self.connect_single_database,
                    connection_name,
                    config['server'],
                    config['database'],
                    config.get('auth_type', 'sql'),
                    config.get('username'),
                    config.get('password')
                )
                future_to_config[future] = connection_name
            
            for future in as_completed(future_to_config):
                connection_name = future_to_config[future]
                try:
                    success = future.result()
                    results[connection_name] = success
                except Exception as e:
                    results[connection_name] = False
                    print(f"Exception connecting to {connection_name}: {e}")
        
        return results
    
    def get_connection(self, connection_name):
        """Get a specific connection by name."""
        with self.connection_lock:
            return self.connections.get(connection_name)
    
    def list_connections(self):
        """List all active connections."""
        with self.connection_lock:
            return list(self.connections.keys())
    
    def get_connection_info(self, connection_name):
        """Get detailed information about a connection."""
        with self.connection_lock:
            if connection_name in self.connections:
                conn_info = self.connections[connection_name].copy()
                # Remove connection objects for safe display
                conn_info.pop('connection', None)
                conn_info.pop('cursor', None)
                return conn_info
            return None
    
    def execute_query(self, connection_name, query, params=None):
        """
        Execute a query on a specific connection.
        
        Args:
            connection_name (str): Name of the connection
            query (str): SQL query to execute
            params (tuple, optional): Query parameters
            
        Returns:
            list: Query results
        """
        conn_info = self.get_connection(connection_name)
        if not conn_info:
            raise ValueError(f"Connection '{connection_name}' not found")
        
        cursor = conn_info['cursor']
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        return cursor.fetchall()
    
    def execute_query_on_all(self, query, params=None):
        """
        Execute the same query on all active connections.
        
        Args:
            query (str): SQL query to execute
            params (tuple, optional): Query parameters
            
        Returns:
            dict: Results from each connection
        """
        results = {}
        connection_names = self.list_connections()
        
        for conn_name in connection_names:
            try:
                result = self.execute_query(conn_name, query, params)
                results[conn_name] = result
            except Exception as e:
                results[conn_name] = f"Error: {str(e)}"
        
        return results
    
    def test_all_connections(self):
        """Test all active connections."""
        print("\n" + "="*80)
        print("TESTING ALL ACTIVE CONNECTIONS")
        print("="*80)
        
        connection_names = self.list_connections()
        if not connection_names:
            print("No active connections to test.")
            return
        
        for conn_name in connection_names:
            try:
                print(f"\nTesting connection: {conn_name}")
                conn_info = self.get_connection_info(conn_name)
                print(f"  Server: {conn_info['server']}")
                print(f"  Database: {conn_info['database']}")
                print(f"  Auth Type: {conn_info['auth_type']}")
                print(f"  Driver: {conn_info['driver']}")
                
                # Test basic query
                result = self.execute_query(conn_name, "SELECT @@SERVERNAME as server_name, DB_NAME() as database_name, GETDATE() as current_time")
                if result:
                    row = result[0]
                    print(f"  ✓ Server: {row.server_name}")
                    print(f"  ✓ Database: {row.database_name}")
                    print(f"  ✓ Time: {row.current_time}")
                else:
                    print("  ✗ No result from test query")
                    
            except Exception as e:
                print(f"  ✗ Error testing {conn_name}: {str(e)}")
    
    def close_connection(self, connection_name):
        """Close a specific connection."""
        with self.connection_lock:
            if connection_name in self.connections:
                try:
                    conn_info = self.connections[connection_name]
                    conn_info['cursor'].close()
                    conn_info['connection'].close()
                    del self.connections[connection_name]
                    print(f"Closed connection '{connection_name}'")
                    return True
                except Exception as e:
                    print(f"Error closing connection '{connection_name}': {e}")
                    return False
            else:
                print(f"Connection '{connection_name}' not found")
                return False
    
    def close_all_connections(self):
        """Close all active connections."""
        connection_names = self.list_connections().copy()
        for conn_name in connection_names:
            self.close_connection(conn_name)
        print(f"Closed {len(connection_names)} connections")


def demo_multiple_connections():
    """Demonstration of multiple database connections."""
    print("="*80)
    print("MULTI-DATABASE CONNECTION DEMO")
    print("="*80)
    
    # Initialize the connector
    connector = MultiDatabaseConnector()
    
    # Example 1: Connect to multiple databases on the same server
    print("\n1. Connecting to multiple databases on the same server...")
    databases = ['master', 'tempdb', 'msdb']
    results = connector.connect_multiple_databases_same_server(
        server="localhost,1433",
        databases=databases,
        auth_type='sql',
        username="SA",
        password=os.environ.get("password")
    )
    
    print("Results from same-server connections:")
    for db, success in results.items():
        status = "✓ Success" if success else "✗ Failed"
        print(f"  {db}: {status}")
    
    # Example 2: Connect to multiple servers with different configurations
    print("\n2. Connecting to multiple servers...")
    server_configs = [
        {
            'name': 'local_master',
            'server': 'localhost,1433',
            'database': 'master',
            'auth_type': 'sql',
            'username': 'SA',
            'password': os.environ.get("password")
        },
        {
            'name': 'local_tempdb',
            'server': '127.0.0.1,1433',
            'database': 'tempdb',
            'auth_type': 'sql',
            'username': 'SA',
            'password': os.environ.get("password")
        },
        # Add more server configurations as needed
    ]
    
    results = connector.connect_multiple_servers(server_configs)
    print("Results from multi-server connections:")
    for conn_name, success in results.items():
        status = "✓ Success" if success else "✗ Failed"
        print(f"  {conn_name}: {status}")
    
    # Test all connections
    connector.test_all_connections()
    
    # Example 3: Execute queries on specific connections
    print("\n3. Executing queries on specific connections...")
    active_connections = connector.list_connections()
    if active_connections:
        for conn_name in active_connections[:2]:  # Test first 2 connections
            try:
                print(f"\nQuerying {conn_name}:")
                results = connector.execute_query(
                    conn_name, 
                    "SELECT COUNT(*) as table_count FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
                )
                if results:
                    print(f"  User tables in database: {results[0].table_count}")
            except Exception as e:
                print(f"  Error querying {conn_name}: {e}")
    
    # Example 4: Execute the same query on all connections
    print("\n4. Executing same query on all connections...")
    all_results = connector.execute_query_on_all("SELECT DB_NAME() as current_database")
    for conn_name, result in all_results.items():
        if isinstance(result, list) and result:
            print(f"  {conn_name}: {result[0].current_database}")
        else:
            print(f"  {conn_name}: {result}")
    
    # Clean up
    print("\n5. Cleaning up connections...")
    connector.close_all_connections()
    
    print("\nDemo completed!")


if __name__ == "__main__":
    demo_multiple_connections()
