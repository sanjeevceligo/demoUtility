# Manual Google OAuth Setup Guide

## Enhanced Authentication Overview

This document provides comprehensive instructions for configuring Google OAuth authentication for the dashboard application. Access the dashboard at **http://localhost:8501** to view three authentication options:

### Option 1: Quick Demo (Recommended for Initial Evaluation)
- Navigate to "Quick Demo" tab
- Click "Enter Demo Mode"
- Instant access to explore all features and capabilities

### Option 2: Manual Google Authentication

#### Step 1: Obtain Google OAuth Credentials
1. Navigate to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing project
3. Navigate to "APIs & Services" → "Credentials"
4. Click "Create Credentials" → "OAuth 2.0 Client IDs"
5. Application type: "Web application"
6. Add authorized redirect URIs:
   - `http://localhost:8501`
   - `http://localhost:8501/auth/callback`

#### Step 2: Configure Dashboard Authentication
1. Navigate to "Manual Login" tab in the dashboard
2. Enter your Google Client ID
3. Enter your Google Client Secret
4. Add your name and email address
5. Click "Authenticate Manually"

### Option 3: OAuth Setup Guide
- Detailed step-by-step configuration instructions
- Configuration validation tools
- Testing and verification utilities

## Quick Start Recommendation

1. **Initial Evaluation**: Use "Quick Demo" to explore the dashboard capabilities
2. **Production Setup**: Configure Google OAuth for production deployment
3. **Database Connection**: Snowflake connection is pre-configured and ready for testing

## Snowflake Connection Configuration

The dashboard is pre-configured with the following connection parameters:
- **Account**: nsqaufd.uua36379
- **User**: sanjeev.mishra@celigo.com
- **Database**: DATA_ROOM
- **Role**: PRODUCT_ANALYST

Visit the "Connection Test" page to verify your Snowflake connection status.

---

To begin using the dashboard, navigate to **http://localhost:8501** and select your preferred authentication method. 