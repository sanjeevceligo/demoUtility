#!/usr/bin/env python3
"""
Snowflake Setup Helper for nsqaufd.uua36379 instance
"""

import os
import sys
import getpass

def setup_snowflake_config():
    """Interactive setup for Snowflake configuration"""
    print("🏔️ Snowflake Dashboard Setup")
    print("=" * 50)
    print(f"Configuring for: https://app.snowflake.com/nsqaufd/uua36379/")
    print("")
    
    # Get user credentials
    print("📝 Please provide your Snowflake credentials:")
    print("(These will be saved to .env file)")
    print("")
    
    username = input("Snowflake Username: ").strip()
    password = getpass.getpass("Snowflake Password: ").strip()
    
    print("")
    print("🗄️ Database Configuration:")
    database = input("Database Name (press Enter for default): ").strip()
    if not database:
        database = "DEMO_DB"
    
    warehouse = input("Warehouse Name (press Enter for COMPUTE_WH): ").strip()
    if not warehouse:
        warehouse = "COMPUTE_WH"
    
    schema = input("Schema Name (press Enter for PUBLIC): ").strip()
    if not schema:
        schema = "PUBLIC"
    
    role = input("Role Name (press Enter for ACCOUNTADMIN): ").strip()
    if not role:
        role = "ACCOUNTADMIN"
    
    # Create .env file
    env_content = f"""# Snowflake Configuration for nsqaufd.uua36379
SNOWFLAKE_ACCOUNT=nsqaufd.uua36379
SNOWFLAKE_USER={username}
SNOWFLAKE_PASSWORD={password}
SNOWFLAKE_WAREHOUSE={warehouse}
SNOWFLAKE_DATABASE={database}
SNOWFLAKE_SCHEMA={schema}
SNOWFLAKE_ROLE={role}

# Google OAuth Configuration (optional for now)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8501

# Application Configuration
APP_SECRET_KEY=snowflake_dashboard_secret_key_2024
DEBUG=True
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("")
        print("✅ Configuration saved to .env file!")
        return True
    except Exception as e:
        print(f"❌ Failed to save configuration: {e}")
        return False

def test_connection():
    """Test the Snowflake connection"""
    print("")
    print("🧪 Testing Snowflake connection...")
    
    try:
        # Import here to avoid issues if not installed
        import snowflake.connector
        from config import Config
        
        config = Config()
        
        # Test connection
        conn = snowflake.connector.connect(
            account=config.SNOWFLAKE_ACCOUNT,
            user=config.SNOWFLAKE_USER,
            password=config.SNOWFLAKE_PASSWORD,
            warehouse=config.SNOWFLAKE_WAREHOUSE,
            database=config.SNOWFLAKE_DATABASE,
            schema=config.SNOWFLAKE_SCHEMA,
            role=config.SNOWFLAKE_ROLE,
            login_timeout=30
        )
        
        # Test query
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_VERSION(), CURRENT_USER(), CURRENT_DATABASE()")
        result = cursor.fetchone()
        
        print("✅ Connection successful!")
        print(f"   Snowflake Version: {result[0]}")
        print(f"   Connected User: {result[1]}")
        print(f"   Current Database: {result[2]}")
        
        cursor.close()
        conn.close()
        return True
        
    except ImportError:
        print("⚠️ Snowflake connector not available. Run: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        print("")
        print("💡 Common issues:")
        print("   - Check your username/password")
        print("   - Verify the database and warehouse names exist")
        print("   - Ensure your account has proper permissions")
        return False

def setup_sample_data():
    """Offer to set up sample data"""
    print("")
    setup_data = input("🎯 Would you like to set up sample data? (y/n): ").strip().lower()
    
    if setup_data == 'y':
        print("")
        print("📋 To set up sample data:")
        print("1. Open your Snowflake console: https://app.snowflake.com/nsqaufd/uua36379/")
        print("2. Run the SQL commands from 'sample_schema.sql'")
        print("3. This will create the CUSTOMER_DETAILS and CUSTOMER_CONFIGURATIONS tables")
        print("4. Sample data will be inserted automatically")
        print("")
        print("💡 After setting up the data, restart your dashboard for full functionality!")

def main():
    """Main setup function"""
    if not setup_snowflake_config():
        print("❌ Setup failed")
        return False
    
    if not test_connection():
        print("⚠️ Connection test failed - please check your credentials")
        print("You can still run the dashboard in demo mode")
    
    setup_sample_data()
    
    print("")
    print("🚀 Setup complete!")
    print("")
    print("📋 Next steps:")
    print("1. Start the dashboard: python3 -m streamlit run app.py")
    print("2. Open your browser to: http://localhost:8501")
    print("3. Test your Snowflake connection in the 'Connection Test' page")
    print("")
    print("🔗 Your Snowflake instance: https://app.snowflake.com/nsqaufd/uua36379/")
    return True

if __name__ == "__main__":
    main() 