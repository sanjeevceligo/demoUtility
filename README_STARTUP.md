# Customer Data Analytics - Startup Guide

## Overview

This document provides comprehensive startup instructions for the Customer Data Analytics platform, designed with enterprise-grade UI/UX patterns and optimized for production deployment.

## Quick Start Options

### Option 1: Automated Startup Script (Recommended)

```bash
# Execute the automated startup script
./start_dashboard.sh
```

### Option 2: Python-Based Launcher

```bash
# Execute the cross-platform Python launcher
python3 quick_start.py

# Specify custom port configuration
python3 quick_start.py --port 8502

# Enable development mode with auto-reload
python3 quick_start.py --dev
```

### Option 3: Direct Streamlit Execution

```bash
# Install required dependencies
pip install -r requirements.txt

# Launch application directly
streamlit run app.py --server.port=8501
```

## Setup Requirements

### System Requirements
- Python 3.8 or higher
- pip3 package manager
- 4GB RAM minimum
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Automatic Dependency Installation
Both startup scripts will automatically install all required dependencies including:
- UI/UX Enhancement Libraries
- Advanced Visualization Tools
- Performance Optimization Packages
- Security & Authentication Libraries

## Access Information

### Default URLs
- **Primary Dashboard:** `http://localhost:8501`
- **Alternative Port:** `http://localhost:8502` (if 8501 is unavailable)

### User Configuration
- **User ID:** `651ea52d8dea360ada3126a5`
- **Default Role:** `PRODUCT_ANALYST`
- **Database:** `DATA_ROOM`
- **Schema:** `MONGODB`

## Management Commands

### Dashboard Restart
```bash
# Stop current session (Ctrl+C) then execute:
./start_dashboard.sh

# Alternative: Using Python launcher
python3 quick_start.py
```

### Dependency Updates
```bash
# Upgrade all packages to latest versions
pip install -r requirements.txt --upgrade

# Alternative: Allow startup script to handle updates
./start_dashboard.sh  # Automatically updates on startup
```

### Cache Management and Reset
```bash
# Clear Streamlit cache
rm -rf .streamlit/cache

# Clear Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +

# Clear application logs
rm -rf logs/*

# Complete system reset (startup script handles all cleanup)
./start_dashboard.sh
```

### Environment Configuration
```bash
# Edit environment variables
nano .env

# Sample .env configuration:
SNOWFLAKE_ACCOUNT=your_account_here
SNOWFLAKE_USER=your_username_here
SNOWFLAKE_PASSWORD=your_password_here
SNOWFLAKE_DATABASE=DATA_ROOM
SNOWFLAKE_SCHEMA=MONGODB
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_ROLE=PRODUCT_ANALYST
DEFAULT_USER_ID=651ea52d8dea360ada3126a5
```

## Troubleshooting

### Port Conflict Resolution
```bash
# Check what process is using port 8501
lsof -i :8501

# Terminate the process
kill -9 <PID>

# Alternative: Use different port
python3 quick_start.py --port 8502
```

### Module Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python path configuration
echo $PYTHONPATH

# Add current directory to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Permission Errors (Unix-like Systems)
```bash
# Set executable permissions
chmod +x start_dashboard.sh
chmod +x quick_start.py

# Execute with elevated permissions if required
sudo ./start_dashboard.sh
```

### Browser Access Issues
- Manually navigate to `http://localhost:8501`
- Use incognito/private browsing mode
- Clear browser cache and cookies
- Test with alternative browser

## Dashboard Features

### Core Analytics
- Customer Data Analytics (Main Dashboard)
- Connection Test & Diagnostics
- Customer Configuration Management
- Advanced Customer Details
- Interactive Query Builder

### Developer & QA Hub
- System Architecture Visualization
- Real-time Performance Monitoring
- Flow Analytics & Insights
- Anomaly Detection System
- Rollout Tracking Dashboard

### Live Monitoring
- Real-time Metrics Display
- Professional Alert Center
- Advanced Trend Analysis
- Comprehensive Health Checks

## UI/UX Features

### Enterprise-Grade Design
- **Glassmorphism Effects** - Modern transparency and blur
- **Professional Gradients** - Consistent color theming
- **Smooth Animations** - Cubic-bezier transitions
- **Advanced Hover Effects** - Interactive micro-animations
- **Responsive Design** - Optimized for all screen sizes

### Professional Authentication
- **OAuth 2.0 Integration** - Secure authentication flow
- **Professional Success Indicators** - Clean user feedback
- **User Profile Management** - Comprehensive user info
- **Session Management** - Secure login/logout

## Performance Optimization

### Cache Management
- Automatic cache clearing on startup
- Optimized data loading strategies
- Efficient memory management

### Loading Optimization
- Professional loading animations
- Asynchronous data fetching
- Minimal resource usage

## Mobile & Desktop Support

- **Desktop:** Full feature set with enhanced UI
- **Tablet:** Responsive layout with touch optimization
- **Mobile:** Core features with mobile-first design

## Security Features

- Secure credential management
- Environment variable protection
- Session security
- Professional authentication flow

## Support & Maintenance

### Regular Updates
```bash
# Pull latest changes (if using git)
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart dashboard
./start_dashboard.sh
```

### Performance Monitoring
- Built-in performance metrics
- Real-time monitoring dashboard
- System health indicators
- Alert management system

---

## Best Practices

1. **Bookmark the Dashboard:** `http://localhost:8501`
2. **Use Development Mode** for rapid iteration: `python3 quick_start.py --dev`
3. **Monitor Logs:** Check `logs/` directory for detailed information
4. **Regular Updates:** Run startup script weekly for optimal performance
5. **Environment Setup:** Always configure `.env` file with your credentials

---

This Customer Data Analytics platform is built with modern web technologies and professional design principles to provide enterprise-grade analytics capabilities. 