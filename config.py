import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the Snowflake Dashboard application"""
    
    # Snowflake Configuration - Updated with working credentials
    # Note: The actual account resolves to ATA59684 from the connection test
    SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT', 'NSQAUFD-UUA36379')
    SNOWFLAKE_USERNAME = os.getenv('SNOWFLAKE_USERNAME', 'sanjeev.mishra@celigo.com')
    SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER', 'sanjeev.mishra@celigo.com')  # Fallback compatibility
    SNOWFLAKE_PASSWORD = os.getenv('SNOWFLAKE_PASSWORD', 'Rinku@0120')
    SNOWFLAKE_DATABASE = os.getenv('SNOWFLAKE_DATABASE', 'DATA_ROOM')
    SNOWFLAKE_SCHEMA = os.getenv('SNOWFLAKE_SCHEMA', 'MONGODB')
    SNOWFLAKE_AUTHENTICATOR = os.getenv('SNOWFLAKE_AUTHENTICATOR', 'EXTERNALBROWSER')
    SNOWFLAKE_WAREHOUSE = os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH')
    SNOWFLAKE_ROLE = os.getenv('SNOWFLAKE_ROLE', 'PRODUCT_ANALYST')
    
    # Authentication settings
    
    @classmethod
    def get_snowflake_config(cls):
        """Get complete Snowflake configuration"""
        return {
            'account': cls.SNOWFLAKE_ACCOUNT,
            'user': cls.SNOWFLAKE_USERNAME,
            'password': cls.SNOWFLAKE_PASSWORD,
            'database': cls.SNOWFLAKE_DATABASE,
            'schema': cls.SNOWFLAKE_SCHEMA,
            'authenticator': cls.SNOWFLAKE_AUTHENTICATOR,
            'warehouse': cls.SNOWFLAKE_WAREHOUSE,
            'role': cls.SNOWFLAKE_ROLE,
            'client_session_keep_alive': True,
            'login_timeout': 30,
            'network_timeout': 30
        }
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        required_fields = [
            'SNOWFLAKE_ACCOUNT',
            'SNOWFLAKE_USER', 
            'SNOWFLAKE_DATABASE'
        ]
        
        missing_fields = []
        for field in required_fields:
            if not getattr(cls, field):
                missing_fields.append(field)
        
        return missing_fields 