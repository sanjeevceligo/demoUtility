#!/usr/bin/env python3
"""
Setup script to create .env file with Snowflake configuration
"""

import os

def create_env_file():
    """Create .env file with Snowflake configuration"""
    print("🔧 Setting up Snowflake Dashboard Environment")
    print("=" * 50)
    
    # Your known Snowflake details
    config = {
        'SNOWFLAKE_ACCOUNT': 'nsqaufd.uua36379',
        'SNOWFLAKE_USER': 'sanjeev.mishra@celigo.com',
        'SNOWFLAKE_WAREHOUSE': 'COMPUTE_WH',
        'SNOWFLAKE_DATABASE': 'DATA_ROOM',
        'SNOWFLAKE_SCHEMA': 'PUBLIC',
        'SNOWFLAKE_ROLE': 'PRODUCT_ANALYST'
    }
    
    print("Using your Snowflake configuration:")
    for key, value in config.items():
        if key != 'SNOWFLAKE_PASSWORD':
            print(f"  {key}: {value}")
    
    # Get password securely
    import getpass
    password = getpass.getpass("\n🔐 Enter your Snowflake password: ")
    config['SNOWFLAKE_PASSWORD'] = password
    
    # Create .env file
    env_content = "# Snowflake Configuration for Real Data Connection\n"
    for key, value in config.items():
        env_content += f"{key}={value}\n"
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("\n✅ .env file created successfully!")
    print("🚀 You can now run the dashboard with real Snowflake data!")
    print("\nTo start the dashboard:")
    print("  python3 -m streamlit run app.py --server.port 8504")

if __name__ == "__main__":
    create_env_file() 