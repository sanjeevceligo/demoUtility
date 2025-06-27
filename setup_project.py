#!/usr/bin/env python3
"""
Snowflake Analytics Dashboard - Setup Script
============================================

This script helps you set up the Snowflake Analytics Dashboard quickly and easily.
It will install dependencies, check system requirements, and guide you through the setup process.

Usage:
    python3 setup_project.py
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

def print_banner():
    """Print a welcome banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║        📊 Snowflake Analytics Dashboard Setup               ║
    ║                                                              ║
    ║        🚀 Professional E2E Team Analytics Platform          ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} detected. Python 3.8+ required.")
        print("   Please upgrade Python and try again.")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible!")

def check_system_info():
    """Display system information"""
    print("\n🖥️  System Information:")
    print(f"   OS: {platform.system()} {platform.release()}")
    print(f"   Architecture: {platform.machine()}")
    print(f"   Python: {sys.version.split()[0]}")

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    try:
        # Upgrade pip first
        print("   Upgrading pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        print("   Installing packages from requirements.txt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print("✅ All dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating project directories...")
    directories = [
        "logs",
        "temp",
        "exports",
        ".streamlit"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✅ Created: {directory}/")

def create_streamlit_config():
    """Create Streamlit configuration"""
    print("\n⚙️  Creating Streamlit configuration...")
    
    config_dir = Path(".streamlit")
    config_dir.mkdir(exist_ok=True)
    
    config_content = """[general]
disableWatchdogWarning = false

[logger]
level = "info"

[client]
caching = true
displayEnabled = true

[server]
headless = false
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
"""
    
    config_file = config_dir / "config.toml"
    with open(config_file, "w") as f:
        f.write(config_content)
    
    print("   ✅ Streamlit configuration created!")

def create_launch_script():
    """Create convenient launch scripts"""
    print("\n🚀 Creating launch script...")
    
    # For Windows
    if platform.system() == "Windows":
        script_content = """@echo off
echo Starting Snowflake Analytics Dashboard...
python -m streamlit run app.py --server.port 8509
pause
"""
        with open("start_dashboard.bat", "w") as f:
            f.write(script_content)
        print("   ✅ Created: start_dashboard.bat")
    
    # For Unix-like systems (macOS, Linux)
    else:
        script_content = """#!/bin/bash
echo "🚀 Starting Snowflake Analytics Dashboard..."
echo "📊 Opening on http://localhost:8509"
echo "🔥 Press Ctrl+C to stop the server"
echo ""
python3 -m streamlit run app.py --server.port 8509
"""
        script_file = "start_dashboard.sh"
        with open(script_file, "w") as f:
            f.write(script_content)
        
        # Make executable
        os.chmod(script_file, 0o755)
        print("   ✅ Created: start_dashboard.sh")

def display_next_steps():
    """Display next steps for the user"""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE! ")
    print("="*60)
    
    print("\n📋 Next Steps:")
    print("   1. Start the dashboard:")
    
    if platform.system() == "Windows":
        print("      • Double-click 'start_dashboard.bat'")
        print("      • OR run: python -m streamlit run app.py --server.port 8509")
    else:
        print("      • Run: ./start_dashboard.sh")
        print("      • OR run: python3 -m streamlit run app.py --server.port 8509")
    
    print("\n   2. Open your browser to: http://localhost:8509")
    print("\n   3. Use the login form in the app to enter your Snowflake credentials:")
    print("      • Account: NSQAUFD-UUA36379 (or your account)")
    print("      • Username: your-email@domain.com")
    print("      • Password: your-password")
    print("      • Authenticator: externalbrowser (for Google OAuth)")
    
    print("\n📚 Documentation:")
    print("   • Check README.md for detailed information")
    print("   • See google_oauth_guide.md for authentication setup")
    
    print("\n🔧 Troubleshooting:")
    print("   • If port 8509 is busy, edit the port number in the launch script")
    print("   • For connection issues, verify your Snowflake credentials")
    print("   • Check logs/ directory for detailed error information")
    
    print("\n🌟 Features Available:")
    print("   • Executive Dashboard with real-time metrics")
    print("   • Dev & QA Hub with system analytics")
    print("   • Live Monitoring with performance tracking")
    print("   • Query Builder with 50+ production queries")
    print("   • Professional visualizations and exports")
    
    print("\n" + "="*60)

def main():
    """Main setup function"""
    print_banner()
    
    # Check system requirements
    check_python_version()
    check_system_info()
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed during dependency installation.")
        sys.exit(1)
    
    # Create project structure
    create_directories()
    create_streamlit_config()
    create_launch_script()
    
    # Show completion message
    display_next_steps()

if __name__ == "__main__":
    main() 