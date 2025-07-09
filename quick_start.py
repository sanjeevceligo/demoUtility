#!/usr/bin/env python3
"""
🚀 Customer Data Analytics - Quick Start Script
Ultra-modern dashboard launcher with comprehensive setup and dependency management

Usage:
    python3 quick_start.py              # Start with default settings
    python3 quick_start.py --port 8502  # Start on custom port
    python3 quick_start.py --dev        # Start in development mode
"""

import os
import sys
import subprocess
import argparse
import time
from pathlib import Path

# Professional color output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color

def print_status(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.NC}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.NC}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.NC}")

def print_info(message):
    print(f"{Colors.CYAN}ℹ️  {message}{Colors.NC}")

def print_header(message):
    print(f"{Colors.PURPLE}{message}{Colors.NC}")

def print_banner():
    """Print professional banner"""
    print("=" * 70)
    print(f"{Colors.BOLD}🚀 CUSTOMER DATA ANALYTICS - Starting Up...{Colors.NC}")
    print("=" * 70)

def check_python():
    """Check Python installation"""
    print_header("🐍 Checking Python Installation...")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} found")
        return True
    else:
        print_error("Python 3.8 or higher is required")
        return False

def setup_virtual_environment():
    """Setup virtual environment"""
    print_header("🔧 Setting up Virtual Environment...")
    
    venv_path = Path("venv")
    if not venv_path.exists():
        print_info("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print_status("Virtual environment created")
    else:
        print_status("Virtual environment exists")
    
    return venv_path

def install_dependencies():
    """Install required dependencies"""
    print_header("📦 Installing Dependencies...")
    print_info("Installing professional UI/UX packages...")
    
    # Determine pip path based on OS
    if os.name == 'nt':  # Windows
        pip_path = Path("venv/Scripts/pip")
    else:  # Unix-like (macOS, Linux)
        pip_path = Path("venv/bin/pip")
    
    try:
        # Upgrade pip
        subprocess.run([str(pip_path), "install", "--upgrade", "pip"], 
                      capture_output=True, check=True)
        
        # Install requirements
        if Path("requirements.txt").exists():
            subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], 
                          capture_output=True, check=True)
            print_status("All dependencies installed successfully")
        else:
            print_warning("requirements.txt not found, installing core packages...")
            core_packages = [
                "streamlit>=1.29.0",
                "pandas>=2.1.4",
                "plotly>=5.17.0",
                "numpy>=1.24.3"
            ]
            for package in core_packages:
                subprocess.run([str(pip_path), "install", package], 
                              capture_output=True, check=True)
            print_status("Core packages installed")
        
        return True
    except subprocess.CalledProcessError as e:
        print_warning("Some dependencies may have failed to install")
        print_info("Continuing with available packages...")
        return False

def check_environment():
    """Check and create environment configuration"""
    print_header("🔐 Checking Environment Configuration...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print_warning(".env file not found")
        print_info("Creating sample .env file...")
        
        env_content = """# Snowflake Configuration
SNOWFLAKE_ACCOUNT=your_account_here
SNOWFLAKE_USER=your_username_here
SNOWFLAKE_PASSWORD=your_password_here
SNOWFLAKE_DATABASE=DATA_ROOM
SNOWFLAKE_SCHEMA=MONGODB
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_ROLE=PRODUCT_ANALYST

# Dashboard Configuration
DASHBOARD_PORT=8501
DASHBOARD_HOST=localhost
DEBUG_MODE=False

# User Configuration
DEFAULT_USER_ID=651ea52d8dea360ada3126a5
"""
        
        with open(".env", "w") as f:
            f.write(env_content)
        
        print_status("Sample .env file created")
        print_info("Please update .env with your actual Snowflake credentials")
    else:
        print_status(".env file exists")

def verify_files():
    """Verify required files exist"""
    print_header("📁 Verifying Required Files...")
    
    required_files = ["app.py", "auth.py", "snowflake_connector.py", "config.py"]
    all_files_exist = True
    
    for file in required_files:
        if Path(file).exists():
            print_status(f"{file} found")
        else:
            print_error(f"{file} is missing")
            all_files_exist = False
    
    return all_files_exist

def clear_cache():
    """Clear Streamlit cache"""
    print_header("🧹 Clearing Cache...")
    
    cache_dir = Path(".streamlit/cache")
    if cache_dir.exists():
        import shutil
        shutil.rmtree(cache_dir)
        print_status("Streamlit cache cleared")
    
    # Create logs directory
    Path("logs").mkdir(exist_ok=True)
    print_status("Logs directory ready")

def print_launch_banner(port=8501, user_id="651ea52d8dea360ada3126a5"):
    """Print professional launch banner"""
    print_header("🌟 Launching Customer Data Analytics...")
    print()
    
    border = "╔" + "═" * 60 + "╗"
    empty = "║" + " " * 60 + "║"
    
    print(f"{Colors.BLUE}{border}{Colors.NC}")
    print(f"{Colors.BLUE}{empty}{Colors.NC}")
    print(f"{Colors.BLUE}║         🚀 CUSTOMER DATA ANALYTICS v2.0                     ║{Colors.NC}")
    print(f"{Colors.BLUE}{empty}{Colors.NC}")
    print(f"{Colors.BLUE}║         Ultra-modern dashboard ║{Colors.NC}")
    print(f"{Colors.BLUE}{empty}{Colors.NC}")
    print(f"{Colors.BLUE}║         🌐 URL: http://localhost:{port:<25}║{Colors.NC}")
    print(f"{Colors.BLUE}║         👤 User ID: {user_id:<30}║{Colors.NC}")
    print(f"{Colors.BLUE}{empty}{Colors.NC}")
    print(f"{Colors.BLUE}║         Press Ctrl+C to stop the dashboard              ║{Colors.NC}")
    print(f"{Colors.BLUE}{empty}{Colors.NC}")
    print(f"{Colors.BLUE}╚{'═' * 60}╝{Colors.NC}")
    print()

def launch_dashboard(port=8501, dev_mode=False):
    """Launch the Streamlit dashboard"""
    print_status("Starting Streamlit dashboard...")
    print_info("Opening browser automatically...")
    
    # Determine streamlit path based on OS
    if os.name == 'nt':  # Windows
        streamlit_path = Path("venv/Scripts/streamlit")
    else:  # Unix-like (macOS, Linux)
        streamlit_path = Path("venv/bin/streamlit")
    
    # Build streamlit command
    cmd = [
        str(streamlit_path), "run", "app.py",
        f"--server.port={port}",
        "--server.address=localhost",
        "--server.headless=false",
        "--browser.gatherUsageStats=false",
        "--theme.primaryColor=#667eea",
        "--theme.backgroundColor=#ffffff",
        "--theme.secondaryBackgroundColor=#f8fafc",
        "--theme.textColor=#1e293b"
    ]
    
    if dev_mode:
        cmd.extend(["--server.runOnSave=true"])
        print_info("Development mode enabled - auto-reload on file changes")
    
    # Set environment variables
    env = os.environ.copy()
    env["PYTHONPATH"] = env.get("PYTHONPATH", "") + ":" + str(Path.cwd())
    
    try:
        subprocess.run(cmd, env=env)
    except KeyboardInterrupt:
        print()
        print_status("Dashboard stopped by user")
    except Exception as e:
        print_error(f"Failed to start dashboard: {e}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Customer Data Analytics Launcher")
    parser.add_argument("--port", type=int, default=8501, help="Port to run dashboard on")
    parser.add_argument("--dev", action="store_true", help="Enable development mode")
    parser.add_argument("--no-install", action="store_true", help="Skip dependency installation")
    
    args = parser.parse_args()
    
    print_banner()
    
    # Pre-flight checks
    if not check_python():
        sys.exit(1)
    
    if not args.no_install:
        setup_virtual_environment()
        install_dependencies()
    
    check_environment()
    
    if not verify_files():
        print_error("Some required files are missing. Please ensure all files are present.")
        sys.exit(1)
    
    clear_cache()
    print_launch_banner(args.port)
    
    # Small delay for dramatic effect
    time.sleep(1)
    
    launch_dashboard(args.port, args.dev)

if __name__ == "__main__":
    main() 