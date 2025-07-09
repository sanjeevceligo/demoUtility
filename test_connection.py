#!/usr/bin/env python3
"""
Test Snowflake connection with user credentials
"""

import snowflake.connector
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_connection():
    """Test Snowflake connection with user's credentials"""
    
    # User's credentials
    connection_params = {
        'account': '',
        'user': '',
        'password': '',
        'database': 'DATA_ROOM',
        'schema': 'MONGODB',
        'role': 'PRODUCT_ANALYST',
        'warehouse': 'COMPUTE_WH',
        'authenticator': 'EXTERNALBROWSER',
        'client_session_keep_alive': True,
        'login_timeout': 30,
        'network_timeout': 30
    }
    
    try:
        logger.info(f"Testing connection to Snowflake...")
        logger.info(f"Account: {connection_params['account']}")
        logger.info(f"User: {connection_params['user']}")
        logger.info(f"Database: {connection_params['database']}")
        logger.info(f"Schema: {connection_params['schema']}")
        logger.info(f"Authenticator: {connection_params['authenticator']}")
        
        # Attempt connection
        conn = snowflake.connector.connect(**connection_params)
        
        # Test query
        with conn.cursor() as cursor:
            cursor.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_ROLE(), CURRENT_WAREHOUSE()")
            result = cursor.fetchone()
            
            if result:
                print("\n✅ Connection Successful!")
                print(f"User: {result[0]}")
                print(f"Account: {result[1]}")
                print(f"Database: {result[2]}")
                print(f"Schema: {result[3]}")
                print(f"Role: {result[4]}")
                print(f"Warehouse: {result[5]}")
            else:
                print("❌ No result from connection test query")
                return False
            
            # Test a simple query
            cursor.execute("SHOW TABLES LIMIT 5")
            tables = cursor.fetchall()
            print(f"\nFound {len(tables)} tables in {connection_params['database']}.{connection_params['schema']}")
            for table in tables:
                print(f"  - {table[1]}")  # Table name is in column 1
        
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Connection failed: {str(e)}")
        print(f"❌ Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1) 
