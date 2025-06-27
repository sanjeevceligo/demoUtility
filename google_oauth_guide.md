# 🔑 Manual Google OAuth Setup Guide

## Your Dashboard Now Has Enhanced Authentication!

Visit your dashboard at **http://localhost:8501** and you'll see three authentication options:

### 🎯 **Option 1: Quick Demo (Recommended to Start)**
- Click "🚀 Quick Demo" tab
- Click "🎯 Enter Demo Mode" 
- **Instant access** to explore all features!

### 🔑 **Option 2: Manual Google Authentication**

#### Step 1: Get Google OAuth Credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Go to "APIs & Services" → "Credentials"
4. Click "Create Credentials" → "OAuth 2.0 Client IDs"
5. Application type: "Web application"
6. Add authorized redirect URIs:
   - `http://localhost:8501`
   - `http://localhost:8501/auth/callback`

#### Step 2: Configure in Dashboard
1. Go to "🔑 Manual Login" tab in your dashboard
2. Enter your Google Client ID
3. Enter your Google Client Secret
4. Add your name and email
5. Click "🚀 Authenticate Manually"

### ⚙️ **Option 3: OAuth Setup Guide**
- Detailed step-by-step instructions
- Configuration checker
- Testing tools

## 🎯 **Quick Start Recommendation:**

1. **Right now**: Use "🚀 Quick Demo" to explore the dashboard
2. **Later**: Set up Google OAuth for production use
3. **Your Snowflake**: Already configured and ready to test!

## 🔗 **Your Snowflake Connection:**

Your dashboard is configured for:
- **Account**: nsqaufd.uua36379
- **User**: sanjeev.mishra@celigo.com
- **Database**: DATA_ROOM
- **Role**: PRODUCT_ANALYST

Visit the "Connection Test" page to verify your Snowflake connection!

---

**Ready to go!** 🚀 Open **http://localhost:8501** and start exploring! 