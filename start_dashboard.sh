#!/bin/bash

# 🚀 Customer Data Analytics - Startup Script
# Ultra-modern dashboard launcher with comprehensive setup

echo "=================================================================="
echo "🚀 CUSTOMER DATA ANALYTICS - Starting Up..."
echo "=================================================================="

# Color codes for professional output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored status
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

print_header() {
    echo -e "${PURPLE}$1${NC}"
}

# Check if Python is installed
print_header "🐍 Checking Python Installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_status "Python found: $PYTHON_VERSION"
else
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if command -v pip3 &> /dev/null; then
    print_status "pip3 is available"
else
    print_error "pip3 is not installed. Please install pip3."
    exit 1
fi

# Check if virtual environment exists, create if not
print_header "🔧 Setting up Virtual Environment..."
if [ ! -d "venv" ]; then
    print_info "Creating virtual environment..."
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_status "Virtual environment exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate
print_status "Virtual environment activated"

# Install/upgrade dependencies
print_header "📦 Installing Dependencies..."
print_info "Installing professional UI/UX packages..."

pip install --upgrade pip > /dev/null 2>&1
if pip install -r requirements.txt > /dev/null 2>&1; then
    print_status "All dependencies installed successfully"
else
    print_warning "Some dependencies may have failed to install"
    print_info "Continuing with available packages..."
fi

# Check if .env file exists
print_header "🔐 Checking Environment Configuration..."
if [ ! -f ".env" ]; then
    print_warning ".env file not found"
    print_info "Creating sample .env file..."
    cat > .env << EOL
# Snowflake Configuration
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
EOL
    print_status "Sample .env file created"
    print_info "Please update .env with your actual Snowflake credentials"
else
    print_status ".env file exists"
fi

# Check for required files
print_header "📁 Verifying Required Files..."
required_files=("app.py" "auth.py" "snowflake_connector.py" "config.py")
all_files_exist=true

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_status "$file found"
    else
        print_error "$file is missing"
        all_files_exist=false
    fi
done

if [ "$all_files_exist" = false ]; then
    print_error "Some required files are missing. Please ensure all files are present."
    exit 1
fi

# Clear any existing streamlit cache
print_header "🧹 Clearing Cache..."
if [ -d ".streamlit" ]; then
    rm -rf .streamlit/cache
    print_status "Streamlit cache cleared"
fi

# Create logs directory if it doesn't exist
mkdir -p logs
print_status "Logs directory ready"

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=localhost

# Professional startup message
print_header "🌟 Launching Customer Data Analytics..."
echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                              ║${NC}"
echo -e "${BLUE}║         🚀 CUSTOMER DATA ANALYTICS v2.0                     ║${NC}"
echo -e "${BLUE}║                                                              ║${NC}"
echo -e "${BLUE}║         Ultra-modern dashboard ║${NC}"
echo -e "${BLUE}║                                                              ║${NC}"
echo -e "${BLUE}║         🌐 URL: http://localhost:8501                       ║${NC}"
echo -e "${BLUE}║         👤 User ID: 651ea52d8dea360ada3126a5                ║${NC}"
echo -e "${BLUE}║                                                              ║${NC}"
echo -e "${BLUE}║         Press Ctrl+C to stop the dashboard                  ║${NC}"
echo -e "${BLUE}║                                                              ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Launch the dashboard
print_status "Starting Streamlit dashboard..."
print_info "Opening browser automatically..."

# Start streamlit with professional configuration
streamlit run app.py \
    --server.port=8501 \
    --server.address=localhost \
    --server.headless=false \
    --browser.gatherUsageStats=false \
    --theme.primaryColor="#667eea" \
    --theme.backgroundColor="#ffffff" \
    --theme.secondaryBackgroundColor="#f8fafc" \
    --theme.textColor="#1e293b"
