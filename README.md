![Screenshot 2025-06-30 at 3 33 51 PM](https://github.com/user-attachments/assets/162d469d-55ba-4be7-9f20-811d34d2521b)# Snowflake Analytics Dashboard

A comprehensive Streamlit-based analytics dashboard for real-time Snowflake data analysis with Google OAuth authentication, featuring production-ready queries and advanced visualizations.

## Key Features

### Authentication
- Google OAuth 2.0 integration with PKCE security
- UI-based credential capture - no environment file configuration needed
- External browser authentication for Snowflake
- Session management with secure credential storage

### Dashboard Pages

#### 1. Dashboard Overview
- Live Metrics: Real-time counts of users, connections, flows, and licenses
- Quick Data Explorer: Instant analysis with pre-built queries
- Connection Analysis: OAuth connections by app, HTTP endpoints usage
- Anomaly Detection: Recent anomalies timeline and alerts
- Canary Rollout: Phase distribution and rollout analytics
- System Health: License tiers and user verification status

#### 2. Connection Test
- Real-time Snowflake connection validation
- External Browser Authentication support
- Connection status indicators
- Database schema exploration

#### 3. Customer Configurations
- Connection Management: Search by ID, app type, user
- Import/Export Analysis: Adaptor type statistics and visualizations
- Flow Configurations: Complex flow analysis with processor/generator counts
- Full Object Views: Complete JSON configuration display

#### 4. Customer Details
- User Search: By ID or email with microservices configuration
- User Analytics: Tier segmentation and domain distribution
- License Management: License info and audit trail tracking
- HTTP Microservices: Enablement analysis and statistics

#### 5. Analytics & Insights
- System Analytics: Connection apps, import/export patterns
- Canary Analytics: Phase distribution and user segmentation
- Anomaly Analytics: Timeline visualization and user-specific anomalies
- Integration Analytics: Complex flow analysis and settings inspection

#### 6. Query Builder
- SQL Editor with syntax highlighting
- Real-time execution with result visualization
- Production Query Library with 50+ pre-built queries
- Export capabilities (CSV, Excel, JSON)

## Production Query Categories

### User & Account Analysis
- User lookup by ID/email
- Microservices configuration analysis
- User verification status distribution

### Export/Import Operations
- Export/import details by ID
- Adaptor type analysis and trends
- Full object structure inspection

### Flow Management
- Flow configuration analysis
- Complex flow identification (processors/generators)
- Response mapping validation
- User-specific flow analytics

### Connection Analysis
- OAuth connections by application
- HTTP endpoint usage patterns
- Connection distribution analysis
- Endpoint import activity correlation

### License & Audit Management
- License information retrieval
- Microservice rollout audit trails
- Active license tier distribution

### User Segmentation & Tiers
- Customer segment classification (internal/free/paid)
- Domain-based user distribution (NA/EU)
- Active user analysis with usage statistics
- HTTP microservices enablement tracking

### Anomaly Detection
- Real-time anomaly event monitoring
- User-specific anomaly tracking
- API anomaly analysis
- App-based anomaly correlation

### Canary Rollout Management
- Release group management
- Phase distribution analysis
- Audit trail correlation
- User migration tracking

### Integration & System Settings
- Canary deployment settings
- S3 scripts data analysis
- Integration configuration inspection

## Technical Implementation

### Real Data Integration
- 50+ Production Queries covering all major data entities
- Live Snowflake Connection with external browser auth
- Real-time Metrics and analytics
- Session-based Credential Management

### Visualizations
- Plotly Interactive Charts: Pie charts, bar charts, scatter plots, timelines
- Real-time Data Refresh: Live connection status and metrics
- Export Capabilities: CSV, Excel, JSON download options
- Responsive Design: Mobile-friendly interface

### Performance & Security
- Connection Pooling for optimal performance
- PKCE OAuth Security for enhanced protection
- Session State Management for user experience
- Error Handling with graceful fallbacks

![Screenshot 2025-06-30 at 3 33 51 PM](https://github.com/user-attachments/assets/102417b5-4065-4c1d-af9c-d5126e09837a)
![Screenshot 2025-06-30 at 3 33 04 PM](https://github.com/user-attachments/assets/7964d883-f070-4ad2-ac43-05298b41170a)
![Screenshot 2025-06-30 at 3 32 32 PM](https://github.com/user-attachments/assets/b1a2c418-a82d-479d-88e4-51619eac165d)
![Screenshot 2025-06-30 at 3 31 24 PM](https://github.com/user-attachments/assets/ffc9e956-76fb-4e38-bdd9-3c800e11d531)
![Screenshot 2025-06-30 at 3 30 46 PM](https://github.com/user-attachments/assets/bf71f530-7b09-4435-a3d0-f1fea7ef3b17)
![Screenshot 2025-06-30 at 3 30 21 PM](https://github.com/user-attachments/assets/957a74ae-dc86-4f67-92f9-d5d98a8712ea)
![Screenshot 2025-06-30 at 3 29 53 PM](https://github.com/user-attachments/assets/25f933d0-a422-4bb0-bc26-d89e4e853d52)
![Screenshot 2025-06-30 at 3 29 24 PM](https://github.com/user-attachments/assets/b2919fcd-ea43-4cd0-82dc-2443b58c41bf)
![Screenshot 2025-06-30 at 3 28 51 PM](https://github.com/user-attachments/assets/006f3222-fa7a-4079-9e66-3b2c5971e52e)
![Screenshot 2025-06-30 at 3 28 34 PM](https://github.com/user-attachments/assets/76652b43-0671-4202-8f17-8572d3545556)

## Getting Started

### System Requirements
- Python 3.8 or higher
- pip package manager
- Git (for cloning the repository)
- Active internet connection for Snowflake access
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation Guide

#### Step 1: Clone the Repository
```bash
git clone https://github.com/sanjeevceligo/demoUtility.git
cd demoUtility
```

#### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Configure Environment Variables
```bash
# Copy the environment template
cp .env.example .env

# Edit the .env file with your Snowflake credentials
# Use any text editor (nano, vim, vscode, etc.)
nano .env
```

Update your `.env` file with the following values:
```bash
SNOWFLAKE_ACCOUNT=your_account_identifier
SNOWFLAKE_USERNAME=your_username@domain.com
SNOWFLAKE_DATABASE=DATA_ROOM
SNOWFLAKE_SCHEMA=MONGODB
SNOWFLAKE_AUTHENTICATOR=snowflake
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_ROLE=PRODUCT_ANALYST%
```

#### Step 5: Test Snowflake Connection
```bash
# Test your Snowflake connection
python test_connection.py
```

### Running the Dashboard

#### Option 1: Using the Start Script (Recommended)
```bash
# Make the script executable (macOS/Linux)
chmod +x start_dashboard.sh

# Run the dashboard
./start_dashboard.sh
```

#### Option 2: Direct Streamlit Command
```bash
# Run with default port (8507)
python3 -m streamlit run app.py --server.port 8507

# Run with custom port
python3 -m streamlit run app.py --server.port 8080

# Run with additional options
python3 -m streamlit run app.py --server.port 8507 --server.headless true
```

#### Option 3: Using Python Run Script
```bash
# Alternative run method
python run.py
```

#### Option 4: Quick Start Script
```bash
# For first-time setup and launch
python quick_start.py
```

### Accessing the Dashboard

1. **Local Access**: Open your browser and navigate to:
   - Default: `http://localhost:8507`
   - Custom port: `http://localhost:YOUR_PORT`

2. **Authentication**: 
   - The dashboard will prompt for Snowflake credentials
   - Use your configured credentials from the `.env` file
   - OAuth authentication will open in your browser

3. **Dashboard Navigation**:
   - **Dashboard Overview**: Main analytics and metrics
   - **Connection Test**: Verify Snowflake connectivity
   - **Customer Configurations**: Search and analyze configurations
   - **Customer Details**: User analytics and insights
   - **Analytics & Insights**: Advanced analytics features
   - **Query Builder**: Custom SQL queries and reporting

### Configuration Options

#### Environment Variables
Update your `.env` file with the following options:

```bash
# Required Snowflake Configuration
SNOWFLAKE_ACCOUNT=your_account_identifier
SNOWFLAKE_USERNAME=your_username@domain.com
SNOWFLAKE_DATABASE=DATA_ROOM
SNOWFLAKE_SCHEMA=MONGODB
SNOWFLAKE_AUTHENTICATOR=snowflake
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_ROLE=PRODUCT_ANALYST%

# Optional Configuration
STREAMLIT_SERVER_PORT=8507
STREAMLIT_SERVER_HEADLESS=false
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

#### Streamlit Configuration
The dashboard includes a pre-configured `.streamlit/config.toml` file with optimized settings:

```toml
[logger]
level = "info"

[server]
headless = false
enableCORS = true
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

### Troubleshooting

#### Common Issues and Solutions

**1. Connection Errors**
```bash
# Test your Snowflake connection
python test_connection.py

# Check your .env file configuration
cat .env
```

**2. Module Not Found Errors**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**3. Port Already in Use**
```bash
# Use a different port
python3 -m streamlit run app.py --server.port 8080

# Or find and kill the process using port 8507
lsof -ti:8507 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8507   # Windows
```

**4. Authentication Issues**
```bash
# Verify Snowflake credentials
python test_connection.py

# Check if external browser authentication is working
# Ensure you're not in a headless environment
```

**5. Permission Errors**
```bash
# Make scripts executable (macOS/Linux)
chmod +x start_dashboard.sh
chmod +x quick_start.py
```

### Development Mode

#### Running in Development Mode
```bash
# Enable auto-reload for development
streamlit run app.py --server.runOnSave true --server.port 8507
```

#### Environment Setup for Development
```bash
# Install development dependencies
pip install -r requirements.txt

# Run setup script for development environment
python setup_project.py
```

### Advanced Usage

#### Custom Configuration
```bash
# Run with custom configuration
python setup_env.py
python3 -m streamlit run app.py --server.port 8507
```

#### Batch Processing
```bash
# Run enhanced queries
python enhanced_queries.py

# Run dashboard features
python enhanced_dashboard_features.py
```

### Export and Data Management

The dashboard supports multiple export formats:
- CSV exports for data analysis
- Excel exports for reporting
- JSON exports for API integration

Access export features through the Query Builder page or individual dashboard sections.

## Sample Queries

### Quick Analytics
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

## Additional Configuration

### Dashboard Customization
- **Port**: Default 8507 (configurable via command line or environment variables)
- **Theme**: Modern gradient UI with glassmorphism design
- **Session Management**: Automatic credential storage and session persistence
- **Export Formats**: CSV, Excel, JSON support across all features
- **Auto-refresh**: Configurable real-time data refresh intervals
- **Query Timeout**: Adjustable timeout settings for long-running queries

### Performance Optimization
- **Connection Pooling**: Automatic connection management for optimal performance
- **Caching**: Query result caching for improved response times
- **Lazy Loading**: On-demand data loading for better initial load times
- **Batch Processing**: Support for bulk operations and data processing

## Analytics Capabilities

- Real-time Monitoring: Live connection and system status
- Trend Analysis: Historical data patterns and insights
- Anomaly Detection: Automated alerts and visualizations
- User Segmentation: Customer tier and usage analysis
- Performance Metrics: System health and optimization insights
- Canary Management: Release rollout tracking and analysis

## Security Features

- OAuth 2.0 with PKCE: Enhanced security for authentication
- Session Encryption: Secure credential storage
- Browser-based Auth: No local credential storage
- Connection Validation: Real-time status verification
- Audit Trail: Complete user action logging

## Updates & Maintenance

The dashboard automatically connects to your live Snowflake instance and provides real-time data analysis. All queries are production-ready and optimized for performance. 
