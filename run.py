#!/usr/bin/env python3
"""
Quick run script for Snowflake Customer Dashboard
"""

import os
import sys
import subprocess

def run_dashboard():
    """Run the Streamlit dashboard"""
    print("🚀 Starting Snowflake Customer Dashboard...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️ No .env file found. Creating template...")
        print("Please update the .env file with your credentials before running again.")
        
        # Run setup script
        try:
            subprocess.check_call([sys.executable, "setup.py"])
            return
        except subprocess.CalledProcessError:
            print("❌ Setup failed. Please run setup.py manually.")
            return
    
    # Check if app.py exists
    if not os.path.exists('app.py'):
        print("❌ app.py not found. Please ensure all files are present.")
        return
    
    # Run the Streamlit app
    try:
        print("🌟 Opening dashboard in your browser...")
        subprocess.check_call([sys.executable, "-m", "streamlit", "run", "app.py"])
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start dashboard: {e}")
        print("💡 Try running: streamlit run app.py")
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")

if __name__ == "__main__":
    run_dashboard() 