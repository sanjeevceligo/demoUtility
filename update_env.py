#!/usr/bin/env python3
"""
Update .env file with correct working Snowflake configuration
"""

import os

def update_env_file():
    """Update .env file with working Snowflake configuration"""
    print("🔧 Updating Snowflake Configuration")
    print("=" * 50)
    
    # Your working Snowflake configuration
    config = {
        'SNOWFLAKE_ACCOUNT': 'NSQAUFD-UUA36379',
        'SNOWFLAKE_USERNAME': 'sanjeev.mishra@celigo.com',
        'SNOWFLAKE_DATABASE': 'DATA_ROOM',
        'SNOWFLAKE_SCHEMA': 'MONGODB',
        'SNOWFLAKE_AUTHENTICATOR': 'snowflake',
        'SNOWFLAKE_WAREHOUSE': 'COMPUTE_WH',
        'SNOWFLAKE_ROLE': 'PRODUCT_ANALYST'
    }
    
    print("Using your working Snowflake configuration:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    # Get password securely
    import getpass
    password = getpass.getpass("\n🔐 Enter your Snowflake password: ")
    config['SNOWFLAKE_PASSWORD'] = password
    
    # Create .env file with correct configuration
    env_content = "# Working Snowflake Configuration\n"
    for key, value in config.items():
        env_content += f"{key}={value}\n"
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("\n✅ .env file updated with working configuration!")
    print("🚀 This should now connect to your Snowflake DATA_ROOM.MONGODB database!")

if __name__ == "__main__":
    update_env_file() 