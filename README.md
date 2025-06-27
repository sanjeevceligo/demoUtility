# 📊 Snowflake Analytics Dashboard

A comprehensive **Streamlit-based analytics dashboard** for real-time Snowflake data analysis with Google OAuth authentication, featuring production-ready queries and advanced visualizations.

## ✨ Key Features

### 🔐 **Authentication**
- **Google OAuth 2.0** integration with PKCE security
- **UI-based credential capture** - no environment file configuration needed
- **External browser authentication** for Snowflake
- **Session management** with secure credential storage

### 📊 **Dashboard Pages**

#### 1. **Dashboard Overview** 
- **Live Metrics**: Real-time counts of users, connections, flows, and licenses
- **Quick Data Explorer**: Instant analysis with pre-built queries
- **Connection Analysis**: OAuth connections by app, HTTP endpoints usage
- **Anomaly Detection**: Recent anomalies timeline and alerts
- **Canary Rollout**: Phase distribution and rollout analytics
- **System Health**: License tiers and user verification status

#### 2. **Connection Test**
- Real-time Snowflake connection validation
- **External Browser Authentication** support
- Connection status indicators
- Database schema exploration

#### 3. **Customer Configurations**
- **Connection Management**: Search by ID, app type, user
- **Import/Export Analysis**: Adaptor type statistics and visualizations
- **Flow Configurations**: Complex flow analysis with processor/generator counts
- **Full Object Views**: Complete JSON configuration display

#### 4. **Customer Details**
- **User Search**: By ID or email with microservices configuration
- **User Analytics**: Tier segmentation and domain distribution
- **License Management**: License info and audit trail tracking
- **HTTP Microservices**: Enablement analysis and statistics

#### 5. **Analytics & Insights**
- **System Analytics**: Connection apps, import/export patterns
- **Canary Analytics**: Phase distribution and user segmentation
- **Anomaly Analytics**: Timeline visualization and user-specific anomalies
- **Integration Analytics**: Complex flow analysis and settings inspection

#### 6. **Query Builder**
- **SQL Editor** with syntax highlighting
- **Real-time execution** with result visualization
- **Production Query Library** with 50+ pre-built queries
- **Export capabilities** (CSV, Excel, JSON)

## 🗂️ **Production Query Categories**

### 🔍 **User & Account Analysis**
- User lookup by ID/email
- Microservices configuration analysis
- User verification status distribution

### 📤 **Export/Import Operations**
- Export/import details by ID
- Adaptor type analysis and trends
- Full object structure inspection

### ⚙️ **Flow Management**
- Flow configuration analysis
- Complex flow identification (processors/generators)
- Response mapping validation
- User-specific flow analytics

### 🔗 **Connection Analysis**
- OAuth connections by application
- HTTP endpoint usage patterns
- Connection distribution analysis
- Endpoint import activity correlation

### 📜 **License & Audit Management**
- License information retrieval
- Microservice rollout audit trails
- Active license tier distribution

### 🎯 **User Segmentation & Tiers**
- Customer segment classification (internal/free/paid)
- Domain-based user distribution (NA/EU)
- Active user analysis with usage statistics
- HTTP microservices enablement tracking

### ⚠️ **Anomaly Detection**
- Real-time anomaly event monitoring
- User-specific anomaly tracking
- API anomaly analysis
- App-based anomaly correlation

### 🚀 **Canary Rollout Management**
- Release group management
- Phase distribution analysis
- Audit trail correlation
- User migration tracking

### ⚙️ **Integration & System Settings**
- Canary deployment settings
- S3 scripts data analysis
- Integration configuration inspection

## 🛠️ **Technical Implementation**

### **Real Data Integration**
- **50+ Production Queries** covering all major data entities
- **Live Snowflake Connection** with external browser auth
- **Real-time Metrics** and analytics
- **Session-based Credential Management**

### **Visualizations**
- **Plotly Interactive Charts**: Pie charts, bar charts, scatter plots, timelines
- **Real-time Data Refresh**: Live connection status and metrics
- **Export Capabilities**: CSV, Excel, JSON download options
- **Responsive Design**: Mobile-friendly interface

### **Performance & Security**
- **Connection Pooling** for optimal performance
- **PKCE OAuth Security** for enhanced protection
- **Session State Management** for user experience
- **Error Handling** with graceful fallbacks

## 🚀 **Quick Start**

### **Prerequisites**
```bash
pip install -r requirements.txt
```

### **Launch Dashboard**
```bash
python3 -m streamlit run app.py --server.port 8507
```

### **Access Application**
- **Local URL**: http://localhost:8507
- **Authentication**: Use UI-based login (no config files needed)
- **Snowflake Credentials**: Enter directly in the dashboard

## 📊 **Sample Queries**

### **Quick Analytics**
```sql
-- OAuth Connections by App
SELECT APP, Count(*) as ConnectionCount FROM
(SELECT * FROM DATA_ROOM.MONGODB.CONNECTIONS WHERE HTTP:auth:oauth is NOT NULL) 
Group by APP ORDER BY ConnectionCount desc

-- User Tier Analysis
SELECT CASE 
    WHEN u.emaildomain='celigo.com' THEN 'internal'
    WHEN nc.customer_segment = '' THEN 'free' 
    ELSE nc.customer_segment END tiers,
IFF(u.subdomain is null, 'NA', 'EU') domain,
count(distinct c._userid) from connections c
-- ... (full query in Query Builder)

-- Recent Anomalies
select * from influxdb.anomaly_events order by time desc limit 50
```

## 🔧 **Configuration**

### **Snowflake Connection**
- **Account**: NSQAUFD-UUA36379
- **Database**: DATA_ROOM
- **Schema**: MONGODB
- **Authentication**: EXTERNALBROWSER (OAuth)
- **User**: Your email address
- **Password**: Your password

### **Dashboard Settings**
- **Port**: 8507 (configurable)
- **Theme**: Modern gradient UI with glassmorphism
- **Session Management**: Automatic credential storage
- **Export Formats**: CSV, Excel, JSON

## 📈 **Analytics Capabilities**

- **Real-time Monitoring**: Live connection and system status
- **Trend Analysis**: Historical data patterns and insights
- **Anomaly Detection**: Automated alerts and visualizations
- **User Segmentation**: Customer tier and usage analysis
- **Performance Metrics**: System health and optimization insights
- **Canary Management**: Release rollout tracking and analysis

## 🛡️ **Security Features**

- **OAuth 2.0 with PKCE**: Enhanced security for authentication
- **Session Encryption**: Secure credential storage
- **Browser-based Auth**: No local credential storage
- **Connection Validation**: Real-time status verification
- **Audit Trail**: Complete user action logging

## 🔄 **Updates & Maintenance**

The dashboard automatically connects to your live Snowflake instance and provides real-time data analysis. All queries are production-ready and optimized for performance.

**Features Added**:
- ✅ Real Snowflake data integration
- ✅ 50+ production queries
- ✅ Interactive visualizations
- ✅ User segmentation analytics
- ✅ Anomaly detection dashboard
- ✅ Canary rollout management
- ✅ Export capabilities
- ✅ Modern UI with animations

**Perfect for**:
- Data Analysts
- System Administrators  
- Product Managers
- DevOps Engineers
- Business Intelligence Teams

---

🎯 **Ready to analyze your Snowflake data with professional dashboards and real-time insights!** 