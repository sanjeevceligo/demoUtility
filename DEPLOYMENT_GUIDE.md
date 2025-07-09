# Deployment Guide - Snowflake Analytics Dashboard

This document provides comprehensive deployment instructions for the Snowflake Analytics Dashboard, including repository setup, team onboarding, and production deployment considerations.

## Table of Contents

1. [Setting Up Git Repository](#setting-up-git-repository)
2. [Pushing to GitHub](#pushing-to-github)
3. [Team Member Setup](#team-member-setup)
4. [Running from Any Directory](#running-from-any-directory)
5. [Troubleshooting](#troubleshooting)

---

## Setting Up Git Repository

### 1. Initialize Git Repository

```bash
# Navigate to project directory
cd /Users/sanjeevmishra/Documents/test

# Initialize git repository
git init

# Add all files to staging
git add .

# Create initial commit
git commit -m "Initial commit: Snowflake Analytics Dashboard with E2E team features"
```

### 2. Create GitHub Repository

1. Navigate to [GitHub](https://github.com) and authenticate
2. Create new repository with the following specifications:
   - Repository name: `snowflake-analytics-dashboard`
   - Description: `Professional E2E Team Analytics Dashboard for Snowflake Data Analysis`
   - Visibility: Configure based on organizational requirements
   - Do not initialize with README (existing README will be used)
3. Create repository

### 3. Connect Local Repository to Remote

```bash
# Add GitHub remote origin (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/snowflake-analytics-dashboard.git

# Set main branch and push
git branch -M main
git push -u origin main
```

---

## Pushing to GitHub

### Initial Push
```bash
# Stage all changes
git add .

# Commit with descriptive message
git commit -m "Add comprehensive dashboard with professional E2E analytics features"

# Push to remote repository
git push origin main
```

### For Future Updates
```bash
# Check repository status
git status

# Stage changes (all or specific files)
git add .
# OR git add specific_file.py

# Commit with descriptive message
git commit -m "Add new dashboard feature: real-time monitoring"

# Push changes to remote
git push origin main
```

---

## Team Member Setup

### Automated Setup (Recommended)

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/snowflake-analytics-dashboard.git

# Navigate to project directory
cd snowflake-analytics-dashboard

# Execute automated setup script
python3 setup_project.py

# Start dashboard application
./start_dashboard.sh    # macOS/Linux
# OR
start_dashboard.bat     # Windows (if available)
```

### Manual Setup Process

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/snowflake-analytics-dashboard.git
cd snowflake-analytics-dashboard

# Create isolated virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install required dependencies
pip install -r requirements.txt

# Launch application
python3 -m streamlit run app.py --server.port 8509
```

---

## Running from Any Directory

### Option 1: System-wide Script Installation (macOS/Linux)

```bash
# Create global executable script
sudo nano /usr/local/bin/snowflake-dashboard

# Add script content:
#!/bin/bash
cd /path/to/snowflake-analytics-dashboard
python3 -m streamlit run app.py --server.port 8509

# Set executable permissions
sudo chmod +x /usr/local/bin/snowflake-dashboard

# Execute from any directory
snowflake-dashboard
```

### Option 2: Windows PATH Configuration

1. Add project directory to System PATH environment variable
2. Create batch file in project directory:

```batch
@echo off
cd /d "%~dp0"
python -m streamlit run app.py --server.port 8509
```

### Option 3: Python Entry Point

Create global Python launcher:

```python
#!/usr/bin/env python3
"""
Global launcher for Snowflake Analytics Dashboard
"""
import os
import subprocess
import sys

# Configure project path
PROJECT_PATH = "/path/to/snowflake-analytics-dashboard"

def main():
    os.chdir(PROJECT_PATH)
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8509"])

if __name__ == "__main__":
    main()
```

---

## Team Access Instructions

### New Team Member Process

1. **Repository Access**
   ```bash
   git clone https://github.com/YOUR_USERNAME/snowflake-analytics-dashboard.git
   cd snowflake-analytics-dashboard
   ```

2. **Environment Setup**
   ```bash
   python3 setup_project.py
   ```

3. **Credential Configuration**
   - Obtain Snowflake account credentials from team administrator
   - Configure environment variables per .env.example template
   - Use external browser authentication for secure access

4. **Application Launch**
   ```bash
   ./start_dashboard.sh
   ```

5. **Application Access**
   - Navigate to http://localhost:8509
   - Authenticate using configured Snowflake credentials
   - Access dashboard analytics interface

---

## Configuration Options

### Custom Port Configuration
```bash
# Specify alternative port
python3 -m streamlit run app.py --server.port 8510
```

### Network Access Configuration
```bash
# Enable external network access
python3 -m streamlit run app.py --server.port 8509 --server.address 0.0.0.0
```

### Environment Variable Configuration
```bash
# Configure runtime environment
export STREAMLIT_SERVER_PORT=8509
export SNOWFLAKE_ACCOUNT=your_account_identifier
python3 -m streamlit run app.py
```

---
### Frontend & UI Framework
- **Streamlit** `1.29.0` - Main web application framework for creating interactive dashboards
- **Plotly** `5.17.0` - Interactive data visualizations (charts, graphs, plots)
- **Altair** `5.2.0` - Statistical data visualization library
- **Streamlit Extensions**:
  - `streamlit-lottie` - Animated graphics and micro-interactions
  - `streamlit-elements` - Enhanced UI components
  - `streamlit-extras` - Additional UI utilities and widgets
  - `streamlit-option-menu` - Professional navigation menus
  - `streamlit-card` - Card-based UI components
  - `streamlit-aggrid` - Advanced data grid functionality

### Backend & Database
- **Python** `3.8+` - Core programming language
- **Snowflake** - Cloud data warehouse platform
- **snowflake-connector-python** `3.6.0` - Official Snowflake Python connector
- **Pandas** `2.1.4` - Data manipulation and analysis library
- **NumPy** `1.24.3` - Numerical computing library

### Authentication & Security
- **Google OAuth 2.0** - User authentication with PKCE security
- **Snowflake Authentication** - Database connection security
- **Session Management** - Secure credential storage and session handling
- **External Browser Authentication** - Enhanced security for Snowflake connections

### Data Science & Analytics
- **Scikit-learn** `≥1.3.0` - Machine learning and data analysis
- **SciPy** `≥1.11.0` - Scientific computing and statistical analysis
- **Seaborn** `≥0.12.0` - Statistical data visualization
- **Matplotlib** `≥3.7.0` - Comprehensive plotting library
- **Bokeh** `≥3.0.0` - Advanced interactive visualizations
- **NetworkX** `≥2.8.8` - Network analysis and graph theory

### Configuration & Deployment
- **python-dotenv** `1.0.0` - Environment variable management
- **OpenPyXL** `3.1.2` - Excel file processing and export
- **Shell Scripts** - Automated deployment and startup scripts
- **Git** - Version control and collaboration

### Development Tools
- **Virtual Environment** - Python environment isolation
- **Requirements Management** - Dependency tracking and installation
- **Configuration Files** - Streamlit and application settings
- **Logging** - Application monitoring and debugging

## Troubleshooting

### Common Issues and Resolutions

#### Port Conflict Resolution
```bash
# Terminate existing processes
pkill -f streamlit

# Alternative: Use different port
python3 -m streamlit run app.py --server.port 8510
```

#### Dependency Management Issues
```bash
# Force reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Alternative: Fresh virtual environment
python3 -m venv fresh_env
source fresh_env/bin/activate
pip install -r requirements.txt
```

#### Snowflake Connection Issues
1. Verify credentials in application login interface
2. Confirm external browser authentication functionality
3. Validate network connectivity to Snowflake endpoints
4. Test alternative authentication methods

#### Permission Issues (Unix-like Systems)
```bash
# Set executable permissions
chmod +x start_dashboard.sh
chmod +x setup_project.py
```

---

## Production Deployment

### Production Environment Configuration

#### Environment Variable Management
```bash
export SNOWFLAKE_ACCOUNT=your_account_identifier
export SNOWFLAKE_USER=your_username
export STREAMLIT_SERVER_PORT=8080
```

#### Docker Containerization
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8509
CMD ["streamlit", "run", "app.py", "--server.port", "8509", "--server.address", "0.0.0.0"]
```

#### Process Management with PM2
```bash
# Install PM2 process manager
npm install -g pm2

# Create ecosystem configuration
echo 'module.exports = {
  apps: [{
    name: "snowflake-dashboard",
    script: "streamlit",
    args: "run app.py --server.port 8509",
    interpreter: "python3"
  }]
}' > ecosystem.config.js

# Start application with PM2
pm2 start ecosystem.config.js
```

---

## Security Considerations

### Security Best Practices

1. **Credential Management**: Never commit sensitive credentials to version control
2. **Environment Variables**: Use environment variables for sensitive configuration
3. **Access Control**: Restrict repository access to authorized personnel
4. **Dependency Updates**: Maintain regular security updates for all dependencies
5. **Transport Security**: Use HTTPS for all production deployments
6. **Authentication**: Implement proper authentication mechanisms
7. **Network Security**: Configure appropriate firewall rules and network access controls

---

## Operations and Maintenance

### Standard Operating Procedures

#### Environment Setup
```bash
git clone https://github.com/YOUR_USERNAME/snowflake-analytics-dashboard.git
cd snowflake-analytics-dashboard
python3 setup_project.py
```

#### Daily Operations
```bash
./start_dashboard.sh
```

#### Update Management
```bash
git pull origin main
```

#### Change Management
```bash
git add .
git commit -m "Descriptive change message"
git push origin main
```

### Deployment Verification Checklist

- [ ] Repository successfully created and pushed to GitHub
- [ ] Team members can clone and execute locally
- [ ] Setup automation functions across target systems
- [ ] Application runs on consistent port configuration
- [ ] Snowflake authentication integration functional
- [ ] All dashboard features operational
- [ ] Documentation complete and accessible

### Support and Escalation

1. **Log Analysis**: Review application logs in `logs/` directory
2. **Documentation Review**: Consult README.md for feature documentation
3. **Issue Tracking**: Check GitHub Issues for known problems and solutions
4. **Administrative Support**: Contact team administrator for access-related issues

---

## Additional Resources

This dashboard provides comprehensive analytics capabilities for E2E team operations with professional visualizations and real-time monitoring functionality. For additional technical support and feature requests, consult the project documentation and issue tracking system. 
