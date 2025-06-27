#!/usr/bin/env python3
"""
Setup script for Snowflake Customer Dashboard
"""

import os
import sys
import subprocess
import shutil

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print("✅ Python version check passed")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def create_env_file():
    """Create .env file from template if it doesn't exist"""
    if os.path.exists('.env'):
        print("⚠️ .env file already exists, skipping creation")
        return True
    
    print("📝 Creating .env file from template...")
    env_template = """# Snowflake Configuration
SNOWFLAKE_ACCOUNT=your_snowflake_account_identifier
SNOWFLAKE_USER=your_snowflake_username
SNOWFLAKE_PASSWORD=your_snowflake_password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=your_database_name
SNOWFLAKE_SCHEMA=PUBLIC
SNOWFLAKE_ROLE=ACCOUNTADMIN

# Google OAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8501

# Application Configuration
APP_SECRET_KEY=your_secret_key_for_session_management
DEBUG=True
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_template)
        print("✅ .env file created successfully")
        print("⚠️ Remember to update the .env file with your actual credentials!")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def check_streamlit():
    """Check if Streamlit is available"""
    try:
        import streamlit
        print("✅ Streamlit is available")
        return True
    except ImportError:
        print("❌ Streamlit not found - please install requirements first")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Snowflake Customer Dashboard...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed at requirements installation")
        return False
    
    # Create environment file
    if not create_env_file():
        print("❌ Setup failed at .env file creation")
        return False
    
    # Check if Streamlit is working
    if not check_streamlit():
        print("❌ Setup failed at Streamlit check")
        return False
    
    print("=" * 50)
    print("🎉 Setup completed successfully!")
    print("")
    print("📋 Next steps:")
    print("1. Update the .env file with your Snowflake and Google OAuth credentials")
    print("2. Set up your Snowflake tables (see README.md for schema)")
    print("3. Configure Google OAuth in Google Cloud Console")
    print("4. Run the application: streamlit run app.py")
    print("")
    print("📖 For detailed instructions, see README.md")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 