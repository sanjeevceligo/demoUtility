# 🚀 Deployment Guide - Snowflake Analytics Dashboard

This guide explains how to deploy the Snowflake Analytics Dashboard to a Git repository and how team members can run it locally.

## 📋 Table of Contents

1. [Setting Up Git Repository](#setting-up-git-repository)
2. [Pushing to GitHub](#pushing-to-github)
3. [Team Member Setup](#team-member-setup)
4. [Running from Any Directory](#running-from-any-directory)
5. [Troubleshooting](#troubleshooting)

---

## 🏗️ Setting Up Git Repository

### 1. Initialize Git Repository

```bash
# Navigate to your project directory
cd /Users/sanjeevmishra/Documents/test

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Snowflake Analytics Dashboard with E2E team features"
```

### 2. Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click "New" to create a new repository
3. Name it: `snowflake-analytics-dashboard`
4. Description: `Professional E2E Team Analytics Dashboard for Snowflake Data Analysis`
5. Choose **Public** or **Private** based on your needs
6. **Don't** initialize with README (we already have one)
7. Click "Create repository"

### 3. Connect Local Repository to GitHub

```bash
# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/snowflake-analytics-dashboard.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## 🚀 Pushing to GitHub

### Initial Push
```bash
# Add all changes
git add .

# Commit changes
git commit -m "Add comprehensive dashboard with professional E2E analytics features"

# Push to GitHub
git push origin main
```

### For Future Updates
```bash
# Check status
git status

# Add specific files or all changes
git add .
# OR git add specific_file.py

# Commit with descriptive message
git commit -m "Add new dashboard feature: real-time monitoring"

# Push changes
git push origin main
```

---

## 👥 Team Member Setup

### Quick Start (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/snowflake-analytics-dashboard.git

# 2. Navigate to project directory
cd snowflake-analytics-dashboard

# 3. Run the automated setup script
python3 setup_project.py

# 4. Start the dashboard
./start_dashboard.sh    # macOS/Linux
# OR
start_dashboard.bat     # Windows
```

### Manual Setup

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/snowflake-analytics-dashboard.git
cd snowflake-analytics-dashboard

# 2. Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python3 -m streamlit run app.py --server.port 8509
```

---

## 🔄 Running from Any Directory

### Option 1: Create Global Script (macOS/Linux)

```bash
# Create a global script
sudo nano /usr/local/bin/snowflake-dashboard

# Add this content:
#!/bin/bash
cd /path/to/snowflake-analytics-dashboard
python3 -m streamlit run app.py --server.port 8509

# Make it executable
sudo chmod +x /usr/local/bin/snowflake-dashboard

# Now you can run from anywhere:
snowflake-dashboard
```

### Option 2: Add to PATH (Windows)

1. Add the project directory to your System PATH
2. Create a batch file in the project directory:

```batch
@echo off
cd /d "%~dp0"
python -m streamlit run app.py --server.port 8509
```

### Option 3: Python Entry Point

Add this to your Python scripts directory:

```python
#!/usr/bin/env python3
"""
Global launcher for Snowflake Analytics Dashboard
"""
import os
import subprocess
import sys

# Update this path to your project location
PROJECT_PATH = "/path/to/snowflake-analytics-dashboard"

def main():
    os.chdir(PROJECT_PATH)
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8509"])

if __name__ == "__main__":
    main()
```

---

## 🌐 Team Access Instructions

### For New Team Members

1. **Get Repository Access**
   ```bash
   git clone https://github.com/YOUR_USERNAME/snowflake-analytics-dashboard.git
   cd snowflake-analytics-dashboard
   ```

2. **Run Setup**
   ```bash
   python3 setup_project.py
   ```

3. **Get Snowflake Credentials**
   - Ask team lead for Snowflake account details
   - Account: `NSQAUFD-UUA36379`
   - Username: Your company email
   - Password: Your password
   - Authenticator: `externalbrowser`

4. **Start Dashboard**
   ```bash
   ./start_dashboard.sh
   ```

5. **Access Application**
   - Open browser: http://localhost:8509
   - Login with your Snowflake credentials
   - Start exploring the analytics!

---

## 🔧 Configuration Options

### Custom Port
```bash
# Run on different port
python3 -m streamlit run app.py --server.port 8510
```

### Custom Host (for team access)
```bash
# Allow access from other machines
python3 -m streamlit run app.py --server.port 8509 --server.address 0.0.0.0
```

### Environment Variables
```bash
# Set environment variables for configuration
export STREAMLIT_SERVER_PORT=8509
export SNOWFLAKE_ACCOUNT=NSQAUFD-UUA36379
python3 -m streamlit run app.py
```

---

## 🛠️ Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Kill existing processes
pkill -f streamlit

# Or use different port
python3 -m streamlit run app.py --server.port 8510
```

#### Dependencies Issues
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Or use virtual environment
python3 -m venv fresh_env
source fresh_env/bin/activate
pip install -r requirements.txt
```

#### Snowflake Connection Issues
1. Verify credentials in the app login form
2. Check if external browser authentication is working
3. Ensure network connectivity to Snowflake
4. Try different authenticator methods

#### Permission Issues (macOS/Linux)
```bash
# Make scripts executable
chmod +x start_dashboard.sh
chmod +x setup_project.py
```

---

## 📊 Production Deployment

### For Production Environment

1. **Use Environment Variables**
   ```bash
   export SNOWFLAKE_ACCOUNT=your_account
   export SNOWFLAKE_USER=your_user
   export STREAMLIT_SERVER_PORT=8080
   ```

2. **Run with Docker** (Optional)
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8509
   CMD ["streamlit", "run", "app.py", "--server.port", "8509", "--server.address", "0.0.0.0"]
   ```

3. **Use Process Manager**
   ```bash
   # Install PM2
   npm install -g pm2
   
   # Create ecosystem file
   echo 'module.exports = {
     apps: [{
       name: "snowflake-dashboard",
       script: "streamlit",
       args: "run app.py --server.port 8509",
       interpreter: "python3"
     }]
   }' > ecosystem.config.js
   
   # Start with PM2
   pm2 start ecosystem.config.js
   ```

---

## 🔐 Security Considerations

1. **Never commit credentials** - they're in .gitignore
2. **Use environment variables** for sensitive data
3. **Restrict repository access** to authorized team members
4. **Regular security updates** for dependencies
5. **Use HTTPS** in production deployments

---

## 📝 Quick Reference Commands

```bash
# Setup new environment
git clone https://github.com/YOUR_USERNAME/snowflake-analytics-dashboard.git
cd snowflake-analytics-dashboard
python3 setup_project.py

# Daily usage
./start_dashboard.sh

# Update from repository
git pull origin main

# Share your changes
git add .
git commit -m "Your changes description"
git push origin main
```

---

## 🎯 Success Checklist

- [ ] Repository created and pushed to GitHub
- [ ] Team members can clone and run locally
- [ ] Setup script works on different systems
- [ ] Application runs on consistent port (8509)
- [ ] Snowflake authentication working
- [ ] All dashboard features functional
- [ ] Documentation is clear and complete

---

## 🆘 Getting Help

1. **Check the logs** in the `logs/` directory
2. **Review the README.md** for feature documentation
3. **Check GitHub Issues** for known problems
4. **Contact team lead** for Snowflake access issues

---

*This dashboard provides comprehensive analytics for E2E team operations with professional visualizations and real-time monitoring capabilities.* 