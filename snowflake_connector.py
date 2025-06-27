import snowflake.connector
from snowflake.connector import DictCursor
import pandas as pd
import streamlit as st
from config import Config
import logging
from typing import Optional, Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SnowflakeConnector:
    """
    A robust Snowflake connector with connection pooling and error handling
    """
    
    def __init__(self):
        self.connection = None
    
    def connect(self) -> bool:
        """Establish connection to Snowflake using session credentials or config fallback"""
        try:
            # Close existing connection if any
            if self.connection:
                try:
                    self.connection.close()
                except:
                    pass
                self.connection = None
            
            # Try to get credentials from session state first (check multiple locations)
            real_creds = st.session_state.get('real_snowflake_credentials', {})
            
            # Also check if credentials are stored in user_info (from auth system)
            if not real_creds and 'user_info' in st.session_state:
                user_info = st.session_state.user_info
                if user_info.get('snowflake_credentials'):
                    real_creds = user_info['snowflake_credentials']
            
            if real_creds and real_creds.get('user'):
                # Use session credentials (from OAuth login)
                connection_params = {
                    'account': real_creds.get('account', Config.SNOWFLAKE_ACCOUNT),
                    'user': real_creds.get('user', Config.SNOWFLAKE_USERNAME),
                    'password': real_creds.get('password', Config.SNOWFLAKE_PASSWORD),
                    'database': real_creds.get('database', Config.SNOWFLAKE_DATABASE),
                    'schema': real_creds.get('schema', Config.SNOWFLAKE_SCHEMA),
                    'role': real_creds.get('role', Config.SNOWFLAKE_ROLE),
                    'warehouse': real_creds.get('warehouse', Config.SNOWFLAKE_WAREHOUSE),
                    'authenticator': real_creds.get('authenticator', Config.SNOWFLAKE_AUTHENTICATOR),
                    'client_session_keep_alive': True,
                    'login_timeout': 30,
                    'network_timeout': 30
                }
                logger.info(f"Using session credentials - Account: {connection_params['account']}, User: {connection_params['user']}, Authenticator: {connection_params['authenticator']}")
            else:
                # Use config credentials as fallback
                connection_params = Config.get_snowflake_config()
                logger.info(f"Using config credentials - Account: {connection_params['account']}, User: {connection_params['user']}, Authenticator: {connection_params['authenticator']}")
            
            # Attempt connection
            logger.info(f"Attempting connection to Snowflake with account: {connection_params['account']}")
            self.connection = snowflake.connector.connect(**connection_params)
            logger.info("Successfully connected to Snowflake")
            return True
                
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Failed to connect to Snowflake: {error_msg}")
            
            # Provide more helpful error messages
            if "incorrect username or password" in error_msg.lower():
                if hasattr(st, 'error'):
                    st.error("❌ Authentication failed: Please check your username and password")
            elif "account" in error_msg.lower() or "could not connect to snowflake backend" in error_msg.lower():
                if hasattr(st, 'error'):
                    st.error("❌ Account error: Please verify your account identifier")
            elif "warehouse" in error_msg.lower():
                if hasattr(st, 'error'):
                    st.error("❌ Warehouse error: Please check if your warehouse exists and is accessible")
            elif "role" in error_msg.lower():
                if hasattr(st, 'error'):
                    st.error("❌ Role error: Please verify your role permissions")
            else:
                if hasattr(st, 'error'):
                    st.error(f"❌ Connection failed: {error_msg}")
            return False
    
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> Optional[pd.DataFrame]:
        """
        Execute a query and return results as a pandas DataFrame
        
        Args:
            query: SQL query string
            params: Optional parameters for parameterized queries
            
        Returns:
            DataFrame with query results or None if error
        """
        try:
            if not self.connect():
                return None
            
            if not self.connection:
                logger.error("No connection available")
                return None
                
            with self.connection.cursor(DictCursor) as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                results = cursor.fetchall()
                
                if results:
                    df = pd.DataFrame(results)
                    logger.info(f"Query executed successfully, returned {len(df)} rows")
                    return df
                else:
                    logger.info("Query executed successfully but returned no results")
                    return pd.DataFrame()
                    
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            st.error(f"❌ Query failed: {str(e)}")
            return None
    
    def get_table_info(self, table_name: str) -> Optional[pd.DataFrame]:
        """
        Get information about a table's structure
        
        Args:
            table_name: Name of the table
            
        Returns:
            DataFrame with table information
        """
        query = f"""
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            IS_NULLABLE,
            COLUMN_DEFAULT,
            COMMENT
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = '{table_name.upper()}'
        ORDER BY ORDINAL_POSITION
        """
        
        return self.execute_query(query)
    
    def get_customer_configurations(self, filters: Optional[Dict[str, Any]] = None) -> Optional[pd.DataFrame]:
        """
        Get customer configurations with optional filtering
        
        Args:
            filters: Optional dictionary of filters to apply
            
        Returns:
            DataFrame with customer configuration data
        """
        base_query = """
        SELECT 
            CUSTOMER_ID,
            CUSTOMER_NAME,
            CONFIGURATION_TYPE,
            CONFIGURATION_VALUE,
            CREATED_DATE,
            UPDATED_DATE,
            STATUS,
            REGION
        FROM CUSTOMER_CONFIGURATIONS
        WHERE 1=1
        """
        
        # Add filters if provided
        if filters:
            if 'customer_id' in filters and filters['customer_id']:
                base_query += f" AND CUSTOMER_ID = '{filters['customer_id']}'"
            if 'status' in filters and filters['status']:
                base_query += f" AND STATUS = '{filters['status']}'"
            if 'region' in filters and filters['region']:
                base_query += f" AND REGION = '{filters['region']}'"
        
        base_query += " ORDER BY UPDATED_DATE DESC"
        
        return self.execute_query(base_query)
    
    def get_customer_details(self, customer_id: Optional[str] = None) -> Optional[pd.DataFrame]:
        """
        Get detailed customer information
        
        Args:
            customer_id: Optional specific customer ID to filter by
            
        Returns:
            DataFrame with customer details
        """
        query = """
        SELECT 
            CUSTOMER_ID,
            CUSTOMER_NAME,
            EMAIL,
            PHONE,
            ADDRESS,
            CITY,
            STATE,
            COUNTRY,
            POSTAL_CODE,
            ACCOUNT_TYPE,
            SUBSCRIPTION_LEVEL,
            CREATED_DATE,
            LAST_LOGIN_DATE,
            STATUS
        FROM CUSTOMER_DETAILS
        WHERE 1=1
        """
        
        if customer_id:
            query += f" AND CUSTOMER_ID = '{customer_id}'"
            
        query += " ORDER BY CREATED_DATE DESC"
        
        return self.execute_query(query)
    
    def get_available_tables(self) -> List[str]:
        """
        Get list of available tables in the current schema
        
        Returns:
            List of table names
        """
        query = """
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = CURRENT_SCHEMA()
        ORDER BY TABLE_NAME
        """
        
        result = self.execute_query(query)
        if result is not None and not result.empty:
            return result['TABLE_NAME'].tolist()
        return []
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the Snowflake connection and return status information
        
        Returns:
            Dictionary with connection status and details
        """
        try:
            if self.connect():
                # Get specific connection by ID
                query = "select * from connections WHERE _id='63c530e37509483cdcc1af96'"
                
                result = self.execute_query(query)
                if result is not None and not result.empty:
                    return {
                        'status': 'success',
                        'message': 'Connection successful - Found specific connection record',
                        'record_count': len(result),
                        'details': result.iloc[0].to_dict()
                    }
                else:
                    return {
                        'status': 'success',
                        'message': 'Connection successful - No records found with specified ID',
                        'record_count': 0,
                        'details': {}
                    }
            
            return {'status': 'failed', 'details': {}}
            
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def close_connection(self):
        """Close the Snowflake connection"""
        try:
            if self.connection and not self.connection.is_closed():
                self.connection.close()
                logger.info("Snowflake connection closed")
        except Exception as e:
            logger.error(f"Error closing connection: {str(e)}")

# Create a global connector instance
@st.cache_resource
def get_snowflake_connector():
    """Get a cached Snowflake connector instance"""
    return SnowflakeConnector() 