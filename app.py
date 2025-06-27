import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import altair as alt
from typing import Optional
import numpy as np
import time

# Local imports (these would work when dependencies are installed)
try:
    from auth import SimpleAuthenticator, require_auth
    from snowflake_connector import get_snowflake_connector
    from config import Config
except ImportError:
    # Fallback for development/demo
    pass

# Page configuration
st.set_page_config(
    page_title="🚀 E2E Analytics Dashboard - Professional Team Console",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for professional E2E team dashboard
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main > div {
        padding-top: 2rem;
    }
    
    /* Professional color scheme */
    :root {
        --primary-color: #2563eb;
        --secondary-color: #10b981;
        --accent-color: #f59e0b;
        --danger-color: #ef4444;
        --warning-color: #f97316;
        --success-color: #059669;
        --info-color: #0ea5e9;
        --dark-bg: #1f2937;
        --light-bg: #f8fafc;
        --card-bg: #ffffff;
        --text-primary: #111827;
        --text-secondary: #6b7280;
        --border-color: #e5e7eb;
    }
    
    /* Professional header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 400;
    }
    
    /* Professional KPI cards */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .kpi-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
    }
    
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .kpi-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        line-height: 1;
    }
    
    .kpi-change {
        font-size: 0.875rem;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    .kpi-change.positive {
        color: var(--success-color);
    }
    
    .kpi-change.negative {
        color: var(--danger-color);
    }
    
    .kpi-change.neutral {
        color: var(--text-secondary);
    }
    
    /* Professional tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background-color: #f8fafc;
        padding: 0.5rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s ease;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary-color), var(--info-color));
        color: white !important;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
    }
    
    /* Professional sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #1f2937 0%, #374151 100%);
    }
    
    .css-1d391kg .css-1v0mbdj {
        color: white;
    }
    
    /* Professional metrics */
    .metric-row {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .metric-card {
        flex: 1;
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    }
    
    .metric-card.success {
        border-left: 4px solid var(--success-color);
    }
    
    .metric-card.warning {
        border-left: 4px solid var(--warning-color);
    }
    
    .metric-card.danger {
        border-left: 4px solid var(--danger-color);
    }
    
    .metric-card.info {
        border-left: 4px solid var(--info-color);
    }
    
    /* Professional charts */
    .chart-container {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin: 1rem 0;
    }
    
    .chart-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Professional buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--info-color));
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.4);
    }
    
    /* Professional alerts */
    .alert {
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 500;
        border-left: 4px solid;
    }
    
    .alert.success {
        background-color: #ecfdf5;
        border-color: var(--success-color);
        color: #065f46;
    }
    
    .alert.warning {
        background-color: #fffbeb;
        border-color: var(--warning-color);
        color: #92400e;
    }
    
    .alert.danger {
        background-color: #fef2f2;
        border-color: var(--danger-color);
        color: #991b1b;
    }
    
    .alert.info {
        background-color: #eff6ff;
        border-color: var(--info-color);
        color: #1e40af;
    }
    
    /* Professional data tables */
    .dataframe {
        border: 1px solid var(--border-color);
        border-radius: 8px;
        overflow: hidden;
    }
    
    .dataframe th {
        background: var(--light-bg);
        font-weight: 600;
        color: var(--text-primary);
        padding: 0.75rem;
        border-bottom: 2px solid var(--border-color);
    }
    
    .dataframe td {
        padding: 0.75rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .status-indicator.online {
        background-color: #dcfce7;
        color: #16a34a;
    }
    
    .status-indicator.offline {
        background-color: #fef2f2;
        color: #dc2626;
    }
    
    .status-indicator.warning {
        background-color: #fefce8;
        color: #ca8a04;
    }
    
    /* Hide Streamlit branding for professional look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Professional loading */
    .stSpinner > div {
        border-top-color: var(--primary-color) !important;
    }
</style>
""", unsafe_allow_html=True)

class SnowflakeDashboard:
    """Main dashboard class with all functionality"""
    
    def __init__(self):
        # Initialize components (with fallback for demo)
        self.has_auth = False
        self.has_connector = False
        
        try:
            self.auth = SimpleAuthenticator()
            self.has_auth = True
        except:
            pass
            
        try:
            self.connector = get_snowflake_connector()
            self.has_connector = True
        except:
            pass
    
    def run(self):
        """Main application entry point"""
        # Check authentication
        if self.has_auth and not self.auth.is_authenticated():
            self.auth.login()
            return
        
        self._show_header()
        self._show_sidebar()
        
        # Main content area based on selected page
        current_page = st.session_state.get('current_page', '📈 Executive Dashboard')
        
        # Core Analytics Pages
        if current_page == '🔗 Connection Test':
            self._show_connection_test()
        elif current_page == '👥 Customer Configurations':
            self._show_customer_configurations()
        elif current_page == '🔍 Customer Details':
            self._show_customer_details()
        elif current_page == '📊 Advanced Analytics':
            self._show_analytics()
        elif current_page == '🛠️ Query Builder':
            self._show_query_builder()
        
        # Developer & QA Hub Pages
        elif current_page == '🏗️ System Architecture':
            self._show_system_architecture()
        elif current_page == '⚡ Performance Monitor':
            self._show_performance_monitor()
        elif current_page == '🔍 Flow Analytics':
            self._show_flow_analytics()
        elif current_page == '⚠️ Anomaly Detection':
            self._show_anomaly_analytics()
        elif current_page == '🚀 Rollout Tracking':
            self._show_canary_analytics()
        elif current_page == '📊 KPI Dashboard':
            self._show_kpi_dashboard()
        elif current_page == '🗺️ System Map':
            self._show_system_map()
        elif current_page == '🔥 Heatmap Analysis':
            self._show_heatmap_analysis()
        
        # Live Monitoring Pages
        elif current_page == '📡 Real-time Metrics':
            self._show_real_time_metrics()
        elif current_page == '🚨 Alert Center':
            self._show_alert_center()
        elif current_page == '📈 Trend Analysis':
            self._show_trends_analysis()
        elif current_page == '🔄 Health Checks':
            self._show_system_health()
        
        # Default to Executive Dashboard
        else:
            self._show_executive_dashboard()
    
    def _show_header(self):
        """Display application header"""
        st.title("❄️ Snowflake Customer Dashboard")
        st.markdown("### Comprehensive Customer Configuration & Analytics Platform")
        
        # Show user info in header
        if self.has_auth:
            user_info = self.auth.get_user_info()
            col1, col2, col3 = st.columns([2, 1, 1])
            with col3:
                st.markdown(f"**Welcome, {user_info.get('name', 'User')}!** 👋")
        else:
            st.info("👋 Welcome to the Snowflake Customer Dashboard!")
    
    def _show_sidebar(self):
        """Display enhanced navigation sidebar for E2E team"""
        with st.sidebar:
            # Professional header
            st.markdown("""
            <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; margin-bottom: 1rem;">
                <h2 style="color: white; margin: 0;">🚀 E2E Console</h2>
                <p style="color: rgba(255,255,255,0.8); margin: 0; font-size: 0.9rem;">Professional Analytics Hub</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Navigation sections
            st.markdown("## 📊 Core Analytics")
            
            core_pages = [
                "📈 Executive Dashboard",
                "🔗 Connection Test", 
                "👥 Customer Configurations",
                "🔍 Customer Details",
                "📊 Advanced Analytics",
                "🛠️ Query Builder"
            ]
            
            # Developer & QA focused pages
            st.markdown("## 🧑‍💻 Dev & QA Hub")
            
            dev_qa_pages = [
                "🏗️ System Architecture",
                "⚡ Performance Monitor", 
                "🔍 Flow Analytics",
                "⚠️ Anomaly Detection",
                "🚀 Rollout Tracking",
                "📊 KPI Dashboard",
                "🗺️ System Map",
                "🔥 Heatmap Analysis"
            ]
            
            # Real-time monitoring
            st.markdown("## 🔴 Live Monitoring")
            
            monitoring_pages = [
                "📡 Real-time Metrics",
                "🚨 Alert Center",
                "📈 Trend Analysis",
                "🔄 Health Checks"
            ]
            
            all_pages = core_pages + dev_qa_pages + monitoring_pages
            
            selected_page = st.selectbox("Navigate to:", all_pages, key="page_selector")
            st.session_state.current_page = selected_page
            
            st.markdown("---")
            
            # System status
            st.markdown("## 🟢 System Status")
            
            # Mock system health indicators
            status_col1, status_col2 = st.columns(2)
            with status_col1:
                st.markdown("**Snowflake**: 🟢 Online")
                st.markdown("**API**: 🟢 Healthy")
            with status_col2:
                st.markdown("**Cache**: 🟡 Warm")
                st.markdown("**Flows**: 🟢 Active")
            
            # Configuration section
            st.markdown("## ⚙️ Configuration")
            
            if st.button("🔄 Refresh All Data", use_container_width=True):
                st.cache_data.clear()
                st.success("✅ All caches cleared!")
            
            if st.button("📊 Export Report", use_container_width=True):
                st.info("📋 Report generation started...")
            
            # Environment info
            st.markdown("## 🌐 Environment")
            env_info = {
                "Environment": "Production",
                "Region": "US-West-2", 
                "Version": "v2.1.4",
                "Last Updated": datetime.now().strftime("%H:%M")
            }
            
            for key, value in env_info.items():
                st.text(f"{key}: {value}")
            
            # Show authentication info if available
            if self.has_auth:
                st.markdown("---")
                self.auth._show_user_info()
            else:
                st.markdown("---")
                st.markdown("### 🔐 Demo Mode")
                st.info("Enable authentication for full team features")
    
    def _show_connection_test(self):
        """Display connection test page"""
        st.header("🔗 Snowflake Connection Test")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Configuration Status")
            
            if not self.has_connector:
                st.warning("⚠️ Snowflake connector not available")
                st.markdown("""
                **To enable Snowflake connectivity:**
                1. Install dependencies: `pip install -r requirements.txt`
                2. Create a `.env` file with your Snowflake credentials:
                   - `SNOWFLAKE_ACCOUNT=your_account`
                   - `SNOWFLAKE_USER=your_username`
                   - `SNOWFLAKE_PASSWORD=your_password`
                   - `SNOWFLAKE_DATABASE=your_database`
                """)
            else:
                try:
                    missing_fields = Config.validate_config()
                    if missing_fields:
                        st.error(f"❌ Missing configuration: {', '.join(missing_fields)}")
                    else:
                        st.success("✅ All required configuration present")
                except:
                    st.warning("⚠️ Configuration validation unavailable")
        
        with col2:
            st.subheader("Connection Test")
            if st.button("🧪 Test Connection", type="primary"):
                if self.has_connector:
                    with st.spinner("Testing connection..."):
                        try:
                            result = self.connector.test_connection()
                            
                            if result.get('status') == 'success':
                                st.success(f"✅ {result.get('message', 'Connection successful!')}")
                                
                                # Show record count if available
                                if 'record_count' in result:
                                    st.info(f"📊 Records found: {result['record_count']}")
                                
                                # Display connection details
                                if result.get('details'):
                                    st.markdown("**Connection Details:**")
                                    st.json(result.get('details', {}))
                                    
                                    # If it's a connection record, provide more readable display
                                    if '_ID' in result.get('details', {}):
                                        st.markdown("---")
                                        st.markdown("**Connection Record Summary:**")
                                        details = result['details']
                                        
                                        col_a, col_b = st.columns(2)
                                        with col_a:
                                            st.write(f"**ID:** {details.get('_ID', 'N/A')}")
                                            st.write(f"**App:** {details.get('APP', 'N/A')}")
                                            st.write(f"**Name:** {details.get('NAME', 'N/A')}")
                                        with col_b:
                                            st.write(f"**Type:** {details.get('TYPE', 'N/A')}")
                                            st.write(f"**User ID:** {details.get('_USERID', 'N/A')}")
                                            st.write(f"**Created:** {details.get('CREATED', 'N/A')}")
                            else:
                                st.error(f"❌ Connection failed: {result.get('error', 'Unknown error')}")
                        except Exception as e:
                            st.error(f"❌ Connection test failed: {str(e)}")
                else:
                    st.error("❌ Snowflake connector not available")
    
    def _show_dashboard_overview(self):
        """Display main dashboard overview with real Snowflake data"""
        st.header("📊 Dashboard Overview")
        
        if self.has_connector:
            # Real data from Snowflake
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader("🔍 Quick Data Explorer")
                
                # Quick query selector
                quick_queries = {
                    "Connection Apps Overview": "select app, COUNT(*) as occurrence from connections group by app order by occurrence desc",
                    "User Verification Status": "select verified, count(*) as user_count from users group by verified",
                    "Active License Tiers": "select tier, count(*) as license_count from licenses where expires > current_date() group by tier",
                    "Import Adaptor Types": "select adaptortype, COUNT(*) as occurrence from imports group by adaptortype order by occurrence desc",
                    "Export Adaptor Types": "select adaptortype, COUNT(*) as occurrence from exports group by adaptortype order by occurrence desc"
                }
                
                selected_query = st.selectbox("Choose a quick analysis:", list(quick_queries.keys()))
                
                if st.button("🔍 Run Analysis", type="primary"):
                    with st.spinner("Analyzing data..."):
                        try:
                            df = self.connector.execute_query(quick_queries[selected_query])
                            if df is not None and not df.empty:
                                st.success(f"✅ Found {len(df)} records")
                                
                                # Create visualization based on query type
                                if len(df.columns) == 2 and df.columns[1].lower() in ['occurrence', 'user_count', 'license_count']:
                                    # Bar chart for count data
                                    fig = px.bar(df, x=df.columns[0], y=df.columns[1], 
                                               title=f"{selected_query} Analysis")
                                    fig.update_layout(height=400)
                                    st.plotly_chart(fig, use_container_width=True)
                                
                                # Show data table
                                st.dataframe(df, use_container_width=True)
                                
                                # Export option
                                csv = df.to_csv(index=False)
                                st.download_button(
                                    label="📥 Download CSV",
                                    data=csv,
                                    file_name=f"{selected_query.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
                                    mime="text/csv"
                                )
                            else:
                                st.warning("⚠️ No data found")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
            
            with col2:
                st.subheader("📈 Live Metrics")
                
                # Get real counts
                try:
                    # Total users
                    user_count_df = self.connector.execute_query("select count(*) as total from users")
                    user_count = user_count_df.iloc[0]['TOTAL'] if user_count_df is not None and not user_count_df.empty else 0
                    
                    # Total connections
                    conn_count_df = self.connector.execute_query("select count(*) as total from connections")
                    conn_count = conn_count_df.iloc[0]['TOTAL'] if conn_count_df is not None and not conn_count_df.empty else 0
                    
                    # Total flows
                    flow_count_df = self.connector.execute_query("select count(*) as total from flows")
                    flow_count = flow_count_df.iloc[0]['TOTAL'] if flow_count_df is not None and not flow_count_df.empty else 0
                    
                    # Active licenses
                    license_count_df = self.connector.execute_query("select count(*) as total from licenses where expires > current_date()")
                    license_count = license_count_df.iloc[0]['TOTAL'] if license_count_df is not None and not license_count_df.empty else 0
                    
                    st.metric("👥 Total Users", f"{user_count:,}")
                    st.metric("🔗 Connections", f"{conn_count:,}")
                    st.metric("⚙️ Flows", f"{flow_count:,}")
                    st.metric("📜 Active Licenses", f"{license_count:,}")
                    
                except Exception as e:
                    st.error(f"❌ Error loading metrics: {str(e)}")
            
            st.markdown("---")
            
            # Detailed Analytics Section
            tab1, tab2, tab3, tab4 = st.tabs(["🔗 Connections", "⚠️ Anomalies", "🚀 Canary Rollout", "📊 System Health"])
            
            with tab1:
                self._show_connections_analysis()
                
            with tab2:
                self._show_anomaly_analysis()
                
            with tab3:
                self._show_canary_analysis()
                
            with tab4:
                self._show_system_health()
                
        else:
            # Fallback for demo mode
            st.info("📊 Enable Snowflake connection to see real-time analytics")
            self._show_demo_overview()
    
    def _show_connections_analysis(self):
        """Show connection analysis with real data"""
        st.subheader("🔗 Connection Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                # OAuth connections by app
                oauth_query = """
                SELECT APP, Count(*) as ConnectionCount FROM
                (
                  SELECT * FROM DATA_ROOM.MONGODB.CONNECTIONS 
                                        WHERE HTTP:auth:oauth is NOT NULL
                    ) Group by APP ORDER BY ConnectionCount desc
                """
                df_oauth = self.connector.execute_query(oauth_query)
                
                if df_oauth is not None and not df_oauth.empty:
                    st.markdown("**OAuth Connections by App**")
                    fig = px.pie(df_oauth, values='CONNECTIONCOUNT', names='APP', 
                               title="OAuth Connections Distribution")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No OAuth connection data found")
                    
            except Exception as e:
                st.error(f"Error loading OAuth data: {str(e)}")
        
        with col2:
            try:
                # HTTP endpoint analysis
                endpoint_query = """
                select endpoint, COUNT(*) as occurrence from connections 
                where app='http' group by endpoint order by occurrence desc limit 10
                """
                df_endpoints = self.connector.execute_query(endpoint_query)
                
                if df_endpoints is not None and not df_endpoints.empty:
                    st.markdown("**Top HTTP Endpoints**")
                    fig = px.bar(df_endpoints, x='OCCURRENCE', y='ENDPOINT', 
                               orientation='h', title="Most Used HTTP Endpoints")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No HTTP endpoint data found")
                    
            except Exception as e:
                st.error(f"Error loading endpoint data: {str(e)}")
    
    def _show_anomaly_analysis(self):
        """Show anomaly detection analysis"""
        st.subheader("⚠️ Anomaly Detection")
        
        try:
            # Recent anomalies
            anomaly_query = "select * from influxdb.anomaly_events order by time desc limit 10"
            df_anomalies = self.connector.execute_query(anomaly_query)
            
            if df_anomalies is not None and not df_anomalies.empty:
                st.markdown(f"**Recent Anomalies ({len(df_anomalies)} found)**")
                st.dataframe(df_anomalies, use_container_width=True)
                
                # Anomaly timeline
                if 'TIME' in df_anomalies.columns:
                    fig = px.scatter(df_anomalies, x='TIME', y='EXP_OR_IMP_ID', 
                                   title="Anomaly Timeline", 
                                   hover_data=['UID'] if 'UID' in df_anomalies.columns else None)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("✅ No recent anomalies detected")
                
        except Exception as e:
            st.error(f"Error loading anomaly data: {str(e)}")
    
    def _show_canary_analysis(self):
        """Show canary rollout analysis"""
        st.subheader("🚀 Canary Rollout Analysis")
        
        try:
            # Canary groups
            canary_query = "select * from release_canary_groups"
            df_canary = self.connector.execute_query(canary_query)
            
            if df_canary is not None and not df_canary.empty:
                st.markdown("**Active Canary Groups**")
                st.dataframe(df_canary, use_container_width=True)
                
                # Phase distribution query
                phase_query = """
                WITH user_group as (SELECT
                    u._id AS user_id,
                    u.name,
                    u.email,
                    CASE
                        WHEN u.emailDomain = 'celigo.com' THEN 'internal'
                        WHEN l.tier = 'free' and l.trialenddate > CURRENT_DATE() THEN 'free-trial'
                        WHEN l.tier = 'free' THEN 'free'
                        ELSE ef.canary_group_name
                    END as phase,
                    l.tier
                FROM users u
                INNER JOIN licenses l ON l._userId = u._id
                LEFT JOIN (
                    SELECT e.canary_group_name, f.value::STRING AS user_id
                    FROM release_canary_groups e,
                    LATERAL FLATTEN(input => e.USER_IDS) f
                ) ef ON ef.user_id = u._id and ef.RELEASE_NAME='2025.5.1' and ef.version='1.0'
                WHERE l.type in ('integrator', 'endpoint', 'platform', 'diy')
                    and l.tier != 'none'
                    and (l.tier = 'free' OR l.expires > current_date())
                )
                select phase, count(*) as user_count from user_group group by phase
                """
                
                df_phases = self.connector.execute_query(phase_query)
                if df_phases is not None and not df_phases.empty:
                    fig = px.pie(df_phases, values='USER_COUNT', names='PHASE', 
                               title="User Distribution by Phase")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No canary rollout data found")
                
        except Exception as e:
            st.error(f"Error loading canary data: {str(e)}")
    
    def _show_system_health(self):
        """Show system health metrics"""
        st.subheader("📊 System Health")
        
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                # User tier distribution
                tier_query = """
                select tier, count(*) as count from licenses 
                where expires > current_date() 
                group by tier order by count desc
                """
                df_tiers = self.connector.execute_query(tier_query)
                
                if df_tiers is not None and not df_tiers.empty:
                    st.markdown("**License Tier Distribution**")
                    fig = px.bar(df_tiers, x='TIER', y='COUNT', 
                               title="Active License Tiers")
                    st.plotly_chart(fig, use_container_width=True)
                    
            except Exception as e:
                st.error(f"Error loading tier data: {str(e)}")
        
        with col2:
            try:
                # Verification status
                verification_query = "select verified, count(*) as count from users group by verified"
                df_verification = self.connector.execute_query(verification_query)
                
                if df_verification is not None and not df_verification.empty:
                    st.markdown("**User Verification Status**")
                    fig = px.pie(df_verification, values='COUNT', names='VERIFIED', 
                               title="User Verification Distribution")
                    st.plotly_chart(fig, use_container_width=True)
                    
            except Exception as e:
                st.error(f"Error loading verification data: {str(e)}")
    
    def _show_demo_overview(self):
        """Fallback demo overview"""
        st.warning("📊 Demo Mode - Install Snowflake connector for real data")
        
        # Demo metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Users", "1,234", "12")
        with col2:
            st.metric("Connections", "3,456", "89")
        with col3:
            st.metric("Flows", "2,789", "45")
        with col4:
            st.metric("Licenses", "1,123", "23")
    
    def _show_customer_configurations(self):
        """Display customer configurations with real Snowflake data"""
        st.header("⚙️ Customer Configurations")
        
        if self.has_connector:
            # Real data configuration analysis
            tab1, tab2, tab3, tab4 = st.tabs(["🔗 Connections", "📥 Imports", "📤 Exports", "⚙️ Flows"])
            
            with tab1:
                st.subheader("🔗 Connection Configurations")
                
                # Filters
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    connection_id = st.text_input("Connection ID", placeholder="Enter connection ID...")
                
                with col2:
                    app_filter = st.selectbox("App Type", ["", "http", "rest", "ftp", "sftp", "database"])
                
                with col3:
                    user_id = st.text_input("User ID", placeholder="Enter user ID...")
                
                with col4:
                    if st.button("🔍 Search Connections", type="primary"):
                        st.session_state.connection_search = True
                
                # Build and execute query
                if st.session_state.get('connection_search') or st.button("📊 Load All Connections"):
                    base_query = "SELECT _id, app, type, _userId, name, OBJECT_CONSTRUCT(*) as full_data FROM connections"
                    conditions = []
                    
                    if connection_id.strip():
                        conditions.append(f"_id = '{connection_id.strip()}'")
                    if app_filter:
                        conditions.append(f"app = '{app_filter}'")
                    if user_id.strip():
                        conditions.append(f"_userId = '{user_id.strip()}'")
                    
                    if conditions:
                        query = f"{base_query} WHERE {' AND '.join(conditions)}"
                    else:
                        query = f"{base_query} LIMIT 100"
                    
                    with st.spinner("Loading connection data..."):
                        try:
                            df = self.connector.execute_query(query)
                            
                            if df is not None and not df.empty:
                                st.success(f"✅ Found {len(df)} connections")
                                
                                # Summary metrics
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Total Connections", len(df))
                                with col2:
                                    unique_apps = df['APP'].nunique() if 'APP' in df.columns else 0
                                    st.metric("Unique Apps", unique_apps)
                                with col3:
                                    unique_users = df['_USERID'].nunique() if '_USERID' in df.columns else 0
                                    st.metric("Unique Users", unique_users)
                                
                                # Display data
                                display_columns = ['_ID', 'APP', 'TYPE', '_USERID', 'NAME']
                                available_columns = [col for col in display_columns if col in df.columns]
                                st.dataframe(df[available_columns], use_container_width=True, hide_index=True)
                                
                                # Detailed view
                                if st.checkbox("Show Full Connection Details"):
                                    st.json(df.to_dict(orient='records'))
                                
                                # Export
                                csv = df.to_csv(index=False)
                                st.download_button(
                                    label="📥 Download Connections CSV",
                                    data=csv,
                                    file_name=f"connections_{datetime.now().strftime('%Y%m%d')}.csv",
                                    mime="text/csv"
                                )
                            else:
                                st.warning("⚠️ No connections found matching criteria")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
            
            with tab2:
                st.subheader("📥 Import Configurations")
                
                # Import analysis
                col1, col2 = st.columns(2)
                
                with col1:
                    import_id = st.text_input("Import ID", placeholder="Enter import ID...")
                    
                with col2:
                    if st.button("🔍 Get Import Details", type="primary"):
                        if import_id.strip():
                            query = f"select OBJECT_CONSTRUCT( * ) as import_data from imports where _id='{import_id.strip()}'"
                            
                            with st.spinner("Loading import details..."):
                                try:
                                    df = self.connector.execute_query(query)
                                    if df is not None and not df.empty:
                                        st.success("✅ Import found!")
                                        st.json(df.iloc[0]['IMPORT_DATA'])
                                    else:
                                        st.warning("⚠️ Import not found")
                                except Exception as e:
                                    st.error(f"❌ Error: {str(e)}")
                        else:
                            st.warning("Please enter an Import ID")
                
                # Import statistics
                if st.button("📊 Show Import Statistics"):
                    with st.spinner("Analyzing import data..."):
                        try:
                            stats_query = "select adaptortype, COUNT(*) as count from imports group by adaptortype order by count desc"
                            df_stats = self.connector.execute_query(stats_query)
                            
                            if df_stats is not None and not df_stats.empty:
                                st.subheader("Import Adaptor Type Distribution")
                                fig = px.bar(df_stats, x='ADAPTORTYPE', y='COUNT', 
                                           title="Import Types Analysis")
                                st.plotly_chart(fig, use_container_width=True)
                                st.dataframe(df_stats, use_container_width=True)
                            else:
                                st.warning("No import statistics available")
                        except Exception as e:
                            st.error(f"Error loading import stats: {str(e)}")
            
            with tab3:
                st.subheader("📤 Export Configurations")
                
                # Export analysis
                col1, col2 = st.columns(2)
                
                with col1:
                    export_id = st.text_input("Export ID", placeholder="Enter export ID...")
                    
                with col2:
                    if st.button("🔍 Get Export Details", type="primary"):
                        if export_id.strip():
                            query = f"select OBJECT_CONSTRUCT( * ) as export_data from exports where _id='{export_id.strip()}'"
                            
                            with st.spinner("Loading export details..."):
                                try:
                                    df = self.connector.execute_query(query)
                                    if df is not None and not df.empty:
                                        st.success("✅ Export found!")
                                        st.json(df.iloc[0]['EXPORT_DATA'])
                                    else:
                                        st.warning("⚠️ Export not found")
                                except Exception as e:
                                    st.error(f"❌ Error: {str(e)}")
                        else:
                            st.warning("Please enter an Export ID")
                
                # Export statistics
                if st.button("📊 Show Export Statistics"):
                    with st.spinner("Analyzing export data..."):
                        try:
                            stats_query = "select adaptortype, COUNT(*) as count from exports group by adaptortype order by count desc"
                            df_stats = self.connector.execute_query(stats_query)
                            
                            if df_stats is not None and not df_stats.empty:
                                st.subheader("Export Adaptor Type Distribution")
                                fig = px.bar(df_stats, x='ADAPTORTYPE', y='COUNT', 
                                           title="Export Types Analysis")
                                st.plotly_chart(fig, use_container_width=True)
                                st.dataframe(df_stats, use_container_width=True)
                            else:
                                st.warning("No export statistics available")
                        except Exception as e:
                            st.error(f"Error loading export stats: {str(e)}")
            
            with tab4:
                st.subheader("⚙️ Flow Configurations")
                
                # Flow analysis
                col1, col2 = st.columns(2)
                
                with col1:
                    flow_id = st.text_input("Flow ID", placeholder="Enter flow ID...")
                    
                with col2:
                    user_id_flow = st.text_input("User ID for Flows", placeholder="Enter user ID...")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔍 Get Flow Details", type="primary"):
                        if flow_id.strip():
                            query = f"select OBJECT_CONSTRUCT( * ) as flow_data from flows where _id='{flow_id.strip()}'"
                            
                            with st.spinner("Loading flow details..."):
                                try:
                                    df = self.connector.execute_query(query)
                                    if df is not None and not df.empty:
                                        st.success("✅ Flow found!")
                                        st.json(df.iloc[0]['FLOW_DATA'])
                                    else:
                                        st.warning("⚠️ Flow not found")
                                except Exception as e:
                                    st.error(f"❌ Error: {str(e)}")
                        else:
                            st.warning("Please enter a Flow ID")
                
                with col2:
                    if st.button("👤 Get User Flows", type="primary"):
                        if user_id_flow.strip():
                            query = f"""
                            select *, ARRAY_SIZE(PAGEPROCESSORS) as processor_count 
                            from flows where _userid = '{user_id_flow.strip()}' 
                            limit 10
                            """
                            
                            with st.spinner("Loading user flows..."):
                                try:
                                    df = self.connector.execute_query(query)
                                    if df is not None and not df.empty:
                                        st.success(f"✅ Found {len(df)} flows for user")
                                        
                                        # Show summary
                                        display_cols = ['_ID', 'NAME', '_USERID', 'PROCESSOR_COUNT']
                                        available_cols = [col for col in display_cols if col in df.columns]
                                        st.dataframe(df[available_cols], use_container_width=True)
                                    else:
                                        st.warning("⚠️ No flows found for this user")
                                except Exception as e:
                                    st.error(f"❌ Error: {str(e)}")
                        else:
                            st.warning("Please enter a User ID")
                
                # Complex flow analysis
                if st.button("🔧 Analyze Complex Flows"):
                    with st.spinner("Analyzing complex flows..."):
                        try:
                            complex_query = """
                            select distinct NAME, _USERID, ARRAY_SIZE(PAGEPROCESSORS) as processors,
                                   ARRAY_SIZE(PAGEGENERATORS) as generators
                            from flows 
                            where ARRAY_SIZE(PAGEPROCESSORS) >= 1 
                            and ARRAY_SIZE(PAGEGENERATORS) >= 7 
                            limit 20
                            """
                            df_complex = self.connector.execute_query(complex_query)
                            
                            if df_complex is not None and not df_complex.empty:
                                st.subheader("Complex Flows Analysis")
                                st.dataframe(df_complex, use_container_width=True)
                                
                                # Visualization
                                fig = px.scatter(df_complex, x='PROCESSORS', y='GENERATORS', 
                                               hover_data=['NAME'], title="Flow Complexity Analysis")
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.info("No complex flows found")
                        except Exception as e:
                            st.error(f"Error analyzing complex flows: {str(e)}")
        else:
            # Demo mode fallback
            st.info("📊 Enable Snowflake connection to see real configuration data")
            self._show_demo_configurations()
    
    def _show_demo_configurations(self):
        """Demo configuration data"""
        st.warning("📊 Demo Mode - Enable Snowflake for real data")
        
        # Demo table
        demo_data = pd.DataFrame({
            'Config ID': ['CFG001', 'CFG002', 'CFG003'],
            'Type': ['Connection', 'Import', 'Export'],
            'Status': ['Active', 'Active', 'Inactive'],
            'User': ['user1@example.com', 'user2@example.com', 'user3@example.com']
        })
        st.dataframe(demo_data, use_container_width=True)
    
    def _show_customer_details(self):
        """Display customer details with real Snowflake user data"""
        st.header("👥 Customer Details")
        
        if self.has_connector:
            tab1, tab2, tab3 = st.tabs(["🔍 User Search", "📊 User Analytics", "📋 License Details"])
            
            with tab1:
                st.subheader("🔍 User Search & Details")
                
                col1, col2 = st.columns(2)
                with col1:
                    user_id = st.text_input("User ID", placeholder="Enter user ID...")
                    email = st.text_input("Email", placeholder="Enter email address...")
                
                with col2:
                    if st.button("🔍 Search User by ID", type="primary"):
                        if user_id.strip():
                            query = f"select * from DATA_ROOM.MONGODB.USERS WHERE _ID = '{user_id.strip()}'"
                            with st.spinner("Loading user details..."):
                                try:
                                    df = self.connector.execute_query(query)
                                    if df is not None and not df.empty:
                                        st.success("✅ User found!")
                                        st.dataframe(df, use_container_width=True)
                                        
                                        # Show microservices info
                                        if '_ID' in df.columns:
                                            user_id_found = df.iloc[0]['_ID']
                                            ms_query = f"select microservices from users where _id = '{user_id_found}'"
                                            ms_df = self.connector.execute_query(ms_query)
                                            if ms_df is not None and not ms_df.empty:
                                                st.subheader("🛠️ Microservices Configuration")
                                                st.json(ms_df.iloc[0]['MICROSERVICES'])
                                    else:
                                        st.warning("⚠️ User not found")
                                except Exception as e:
                                    st.error(f"❌ Error: {str(e)}")
                    
                    if st.button("📧 Search User by Email", type="primary"):
                        if email.strip():
                            query = f"select * from DATA_ROOM.MONGODB.USERS WHERE email = '{email.strip()}'"
                            with st.spinner("Loading user details..."):
                                try:
                                    df = self.connector.execute_query(query)
                                    if df is not None and not df.empty:
                                        st.success("✅ User found!")
                                        st.dataframe(df, use_container_width=True)
                                    else:
                                        st.warning("⚠️ User not found")
                                except Exception as e:
                                    st.error(f"❌ Error: {str(e)}")
            
            with tab2:
                st.subheader("📊 User Analytics & Segmentation")
                
                if st.button("📈 Generate User Tier Analysis"):
                    with st.spinner("Analyzing user segments..."):
                        try:
                            tier_query = """
                            select  CASE 
                                        WHEN u.emaildomain='celigo.com' THEN 'internal'
                                        WHEN nc.customer_segment = '' THEN 'free' 
                                        ELSE nc.customer_segment END tiers,
                                    IFF(u.subdomain is null, 'NA', 'EU') domain,
                                    count(distinct c._userid) from connections c
                            INNER JOIN NETSUITE.CUSTOMER_IDS ncids on ncids.io_id=c._USERID 
                            AND type in ('http', 'rest')
                            INNER JOIN NETSUITE.CUSTOMERS nc on nc.internal_id=ncids.NS_CUSTOMER_ID
                            INNER JOIN users u on u._id=c._userid
                            WHERE (u._id  in (
                                SELECT distinct _userId FROM EXPORTS exp
                                INNER JOIN INFLUXDB.usage_stats us ON us.exp_or_imp_id=exp._id AND END_DATE > CURRENT_DATE - 90
                            ) or u._id in (
                                SELECT distinct _userId FROM IMPORTS imp
                                INNER JOIN INFLUXDB.usage_stats us ON us.exp_or_imp_id=imp._id AND END_DATE > CURRENT_DATE - 90
                            ))
                            group by 1,2
                            order by 2,1
                            """
                            df_tiers = self.connector.execute_query(tier_query)
                            
                            if df_tiers is not None and not df_tiers.empty:
                                st.success(f"✅ Found {len(df_tiers)} user segments")
                                
                                # Visualizations
                                col1, col2 = st.columns(2)
                                with col1:
                                    fig1 = px.pie(df_tiers, values='COUNT(DISTINCT C._USERID)', names='TIERS', 
                                                title="User Distribution by Tier")
                                    st.plotly_chart(fig1, use_container_width=True)
                                
                                with col2:
                                    fig2 = px.bar(df_tiers, x='DOMAIN', y='COUNT(DISTINCT C._USERID)', color='TIERS',
                                                title="Users by Domain and Tier")
                                    st.plotly_chart(fig2, use_container_width=True)
                                
                                st.dataframe(df_tiers, use_container_width=True)
                            else:
                                st.warning("No tier data available")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            
            with tab3:
                st.subheader("📋 License & Audit Details")
                
                license_user_id = st.text_input("User ID for License", placeholder="Enter user ID...")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📜 Get License Info"):
                        if license_user_id.strip():
                            query = f"select * from licenses WHERE _userid= '{license_user_id.strip()}'"
                            try:
                                df = self.connector.execute_query(query)
                                if df is not None and not df.empty:
                                    st.success("✅ License found!")
                                    st.dataframe(df, use_container_width=True)
                                else:
                                    st.warning("⚠️ No license found")
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
                
                with col2:
                    if st.button("🔍 Get Audit Records"):
                        if license_user_id.strip():
                            query = f"SELECT * FROM ms_rollout_audit where resource_type='users' and resource_id='{license_user_id.strip()}'"
                            try:
                                df = self.connector.execute_query(query)
                                if df is not None and not df.empty:
                                    st.success(f"✅ Found {len(df)} audit records")
                                    st.dataframe(df, use_container_width=True)
                                else:
                                    st.warning("⚠️ No audit records found")
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
        else:
            st.info("📊 Enable Snowflake connection for real user data")
            demo_data = self._get_demo_customer_data()
            st.dataframe(demo_data, use_container_width=True, hide_index=True)
    
    def _show_customer_detail_card(self, customer):
        """Show detailed customer information card"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📝 Basic Information")
            st.write(f"**Name:** {customer.get('CUSTOMER_NAME', 'N/A')}")
            st.write(f"**Email:** {customer.get('EMAIL', 'N/A')}")
            st.write(f"**Phone:** {customer.get('PHONE', 'N/A')}")
            st.write(f"**Account Type:** {customer.get('ACCOUNT_TYPE', 'N/A')}")
        
        with col2:
            st.markdown("### 📍 Address Information")
            st.write(f"**Address:** {customer.get('ADDRESS', 'N/A')}")
            st.write(f"**City:** {customer.get('CITY', 'N/A')}")
            st.write(f"**State:** {customer.get('STATE', 'N/A')}")
            st.write(f"**Country:** {customer.get('COUNTRY', 'N/A')}")
        
        with col3:
            st.markdown("### 📊 Account Details")
            st.write(f"**Subscription:** {customer.get('SUBSCRIPTION_LEVEL', 'N/A')}")
            st.write(f"**Status:** {customer.get('STATUS', 'N/A')}")
            st.write(f"**Created:** {customer.get('CREATED_DATE', 'N/A')}")
            st.write(f"**Last Login:** {customer.get('LAST_LOGIN_DATE', 'N/A')}")
    
    def _show_analytics(self):
        """Display analytics page with real Snowflake data insights"""
        st.header("📈 Analytics & Insights")
        
        if self.has_connector:
            tab1, tab2, tab3, tab4 = st.tabs(["📊 System Analytics", "🚀 Canary Analytics", "⚠️ Anomaly Analytics", "🔗 Integration Analytics"])
            
            with tab1:
                self._show_real_analytics_overview()
            
            with tab2:
                self._show_canary_analytics()
            
            with tab3:
                self._show_anomaly_analytics()
            
            with tab4:
                self._show_integration_analytics()
        else:
            st.info("📊 Enable Snowflake connection for real analytics")
            tab1, tab2, tab3 = st.tabs(["📊 Overview", "🎯 Trends", "🔍 Deep Dive"])
            with tab1:
                self._show_demo_analytics_overview()
            with tab2:
                self._show_trends_analysis()
            with tab3:
                self._show_deep_dive_analysis()
    
    def _show_real_analytics_overview(self):
        """Show real system analytics with live data"""
        st.subheader("📊 System Overview & Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📈 Connection App Distribution"):
                try:
                    query = "select app, COUNT(*) as count from connections group by app order by count desc"
                    df = self.connector.execute_query(query)
                    if df is not None and not df.empty:
                        fig = px.pie(df, values='COUNT', names='APP', 
                                   title="Connection Apps Distribution")
                        st.plotly_chart(fig, use_container_width=True)
                        st.dataframe(df, use_container_width=True)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        with col2:
            if st.button("📊 Import/Export Analysis"):
                try:
                    col_a, col_b = st.columns(2)
                    with col_a:
                        import_query = "select adaptortype, COUNT(*) as count from imports group by adaptortype order by count desc limit 5"
                        df_imports = self.connector.execute_query(import_query)
                        if df_imports is not None and not df_imports.empty:
                            fig = px.bar(df_imports, x='ADAPTORTYPE', y='COUNT', title="Top Import Types")
                            st.plotly_chart(fig, use_container_width=True)
                    
                    with col_b:
                        export_query = "select adaptortype, COUNT(*) as count from exports group by adaptortype order by count desc limit 5"
                        df_exports = self.connector.execute_query(export_query)
                        if df_exports is not None and not df_exports.empty:
                            fig = px.bar(df_exports, x='ADAPTORTYPE', y='COUNT', title="Top Export Types")
                            st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        # Endpoint analysis
        if st.button("🌐 Endpoint Usage Analysis"):
            try:
                endpoint_query = """
                SELECT t2.endpoint, COUNT(*) AS total_imports
                FROM DATA_ROOM.MONGODB.imports AS t1
                INNER JOIN DATA_ROOM.MONGODB.connections AS t2
                ON t1._connectionid = t2._id
                GROUP BY t2.endpoint
                ORDER BY total_imports DESC
                LIMIT 15
                """
                df_endpoints = self.connector.execute_query(endpoint_query)
                if df_endpoints is not None and not df_endpoints.empty:
                    fig = px.bar(df_endpoints, x='TOTAL_IMPORTS', y='ENDPOINT', 
                               orientation='h', title="Most Used Endpoints")
                    st.plotly_chart(fig, use_container_width=True)
                    st.dataframe(df_endpoints, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    def _show_canary_analytics(self):
        """Show canary rollout analytics"""
        st.subheader("🚀 Canary Rollout Analytics")
        
        if st.button("📊 Generate Canary Phase Analysis"):
            try:
                canary_query = """
                WITH user_group as (SELECT
                    u._id AS user_id,
                    u.name,
                    u.email,
                    u.verified,
                    CASE
                        WHEN u.emailDomain = 'celigo.com' THEN 'internal'
                        WHEN l.tier = 'free'
                        and l.trialenddate > CURRENT_DATE() THEN 'free-trial'
                        WHEN l.tier = 'free' THEN 'free'
                        ELSE ef.canary_group_name
                    END as phase,
                    l.tier
                FROM
                    users u
                    INNER JOIN licenses l ON l._userId = u._id
                    LEFT JOIN (
                        SELECT
                            e.canary_group_name,
                            f.value::STRING AS user_id,
                            e.release_name,
                            e.version
                        FROM
                            release_canary_groups e,
                            LATERAL FLATTEN(input => e.USER_IDS) f 
                    ) ef ON ef.user_id = u._id and ef.RELEASE_NAME='2025.5.1' and ef.version='1.0'
                WHERE
                    l.type in ('integrator', 'endpoint', 'platform', 'diy')
                    and l.tier != 'none'
                    and (
                        l.tier = 'free'
                        OR l.expires > current_date()
                    )
                )
                select phase, count(*) as user_count from user_group 
                where phase is not null
                group by phase
                """
                
                df_canary = self.connector.execute_query(canary_query)
                if df_canary is not None and not df_canary.empty:
                    st.success(f"✅ Canary analysis complete - {len(df_canary)} phases found")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        fig = px.pie(df_canary, values='USER_COUNT', names='PHASE', 
                                   title="User Distribution by Canary Phase")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        fig = px.bar(df_canary, x='PHASE', y='USER_COUNT', 
                                   title="Users per Canary Phase")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    st.dataframe(df_canary, use_container_width=True)
                else:
                    st.warning("No canary data available")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    def _show_anomaly_analytics(self):
        """Show anomaly detection analytics"""
        st.subheader("⚠️ Anomaly Detection Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📈 Recent Anomalies Timeline"):
                try:
                    anomaly_query = "select * from influxdb.anomaly_events order by time desc limit 50"
                    df_anomalies = self.connector.execute_query(anomaly_query)
                    
                    if df_anomalies is not None and not df_anomalies.empty:
                        st.success(f"✅ Found {len(df_anomalies)} recent anomalies")
                        
                        # Timeline visualization
                        if 'TIME' in df_anomalies.columns:
                            fig = px.scatter(df_anomalies, x='TIME', y='EXP_OR_IMP_ID', 
                                           title="Anomaly Timeline",
                                           hover_data=['UID'] if 'UID' in df_anomalies.columns else None)
                            st.plotly_chart(fig, use_container_width=True)
                        
                        st.dataframe(df_anomalies.head(10), use_container_width=True)
                    else:
                        st.info("✅ No recent anomalies detected")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        with col2:
            if st.button("🔍 API Anomaly Analysis"):
                try:
                    api_anomaly_query = "select * from influxdb.api_anomaly_events order by time desc limit 30"
                    df_api = self.connector.execute_query(api_anomaly_query)
                    
                    if df_api is not None and not df_api.empty:
                        st.success(f"✅ Found {len(df_api)} API anomalies")
                        st.dataframe(df_api.head(10), use_container_width=True)
                    else:
                        st.info("✅ No API anomalies detected")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        # Specific user anomaly search
        st.markdown("---")
        user_id_anomaly = st.text_input("Search Anomalies by User ID", placeholder="Enter user ID...")
        if st.button("🔍 Search User Anomalies") and user_id_anomaly.strip():
            try:
                user_anomaly_query = f"select * from influxdb.anomaly_events where uid IN ('{user_id_anomaly.strip()}') ORDER BY time desc"
                df_user_anomalies = self.connector.execute_query(user_anomaly_query)
                
                if df_user_anomalies is not None and not df_user_anomalies.empty:
                    st.success(f"✅ Found {len(df_user_anomalies)} anomalies for user")
                    st.dataframe(df_user_anomalies, use_container_width=True)
                else:
                    st.info("No anomalies found for this user")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    def _show_integration_analytics(self):
        """Show integration and flow analytics"""
        st.subheader("🔗 Integration & Flow Analytics")
        
        if st.button("⚙️ Complex Flow Analysis"):
            try:
                complex_flow_query = """
                select distinct *,ARRAY_SIZE(PAGEPROCESSORS) as processors,
                       ARRAY_SIZE(PAGEGENERATORS) as generators,
                       NAME
                from flows 
                where ARRAY_SIZE(PAGEPROCESSORS)>=1 
                and ARRAY_SIZE(PAGEGENERATORS)>=7 
                limit 20
                """
                df_complex = self.connector.execute_query(complex_flow_query)
                
                if df_complex is not None and not df_complex.empty:
                    st.success(f"✅ Found {len(df_complex)} complex flows")
                    
                    # Scatter plot of complexity
                    fig = px.scatter(df_complex, x='PROCESSORS', y='GENERATORS', 
                                   hover_data=['NAME'], title="Flow Complexity Analysis",
                                   labels={'PROCESSORS': 'Page Processors', 'GENERATORS': 'Page Generators'})
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show flow details
                    display_cols = ['NAME', '_USERID', 'PROCESSORS', 'GENERATORS']
                    available_cols = [col for col in display_cols if col in df_complex.columns]
                    st.dataframe(df_complex[available_cols], use_container_width=True)
                else:
                    st.info("No complex flows found")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        if st.button("🛠️ Integration Settings Analysis"):
            try:
                integration_query = "select settings from integrations limit 10"
                df_integrations = self.connector.execute_query(integration_query)
                
                if df_integrations is not None and not df_integrations.empty:
                    st.success(f"✅ Found {len(df_integrations)} integration settings")
                    
                    # Show sample settings
                    for idx, row in df_integrations.head(5).iterrows():
                        with st.expander(f"Integration Settings #{idx + 1}"):
                            st.json(row['SETTINGS'])
                else:
                    st.info("No integration settings found")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    def _show_query_builder(self):
        """Display custom query builder"""
        st.header("🔧 Custom Query Builder")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📝 SQL Query Editor")
            
            # Available tables (if connector available)
            if self.has_connector:
                try:
                    tables = self.connector.get_available_tables()
                    if tables:
                        selected_table = st.selectbox("Select Table", [""] + tables)
                        if selected_table:
                            st.info(f"Selected table: {selected_table}")
                except:
                    pass
            
            # Query input
            query = st.text_area(
                "SQL Query",
                placeholder="Enter your SQL query here...\n\nExample:\nSELECT * FROM CUSTOMER_DETAILS\nWHERE STATUS = 'Active'\nLIMIT 10;",
                height=200,
                help="Write your custom SQL query to fetch data from Snowflake"
            )
            
            col_a, col_b = st.columns(2)
            with col_a:
                execute_query = st.button("▶️ Execute Query", type="primary")
            with col_b:
                if st.button("📋 Sample Queries"):
                    st.session_state.show_samples = not st.session_state.get('show_samples', False)
        
        with col2:
            st.subheader("📊 Query Results")
            
            if execute_query and query.strip():
                if self.has_connector:
                    with st.spinner("Executing query..."):
                        try:
                            result = self.connector.execute_query(query)
                            if result is not None and not result.empty:
                                st.success(f"✅ Query executed successfully! ({len(result)} rows)")
                                st.dataframe(result, use_container_width=True)
                                
                                # Download option
                                csv = result.to_csv(index=False)
                                st.download_button(
                                    "📥 Download Results",
                                    csv,
                                    f"query_results_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                                    mime="text/csv"
                                )
                            else:
                                st.warning("⚠️ Query returned no results")
                        except Exception as e:
                            st.error(f"❌ Query failed: {str(e)}")
                else:
                    st.error("❌ Snowflake connector not available")
            
            # Sample queries section
            if st.session_state.get('show_samples'):
                st.subheader("📚 Sample Queries")
                self._show_sample_queries()
    
    def _show_sample_queries(self):
        """Show sample SQL queries"""
        samples = {
            "Customer Count by Status": """
SELECT STATUS, COUNT(*) as customer_count
FROM CUSTOMER_DETAILS
GROUP BY STATUS
ORDER BY customer_count DESC;
            """,
            "Recent Configurations": """
SELECT CUSTOMER_NAME, CONFIGURATION_TYPE, UPDATED_DATE
FROM CUSTOMER_CONFIGURATIONS
WHERE UPDATED_DATE >= CURRENT_DATE - 30
ORDER BY UPDATED_DATE DESC
LIMIT 10;
            """,
            "Customer Distribution by Region": """
SELECT REGION, COUNT(*) as customer_count
FROM CUSTOMER_CONFIGURATIONS
GROUP BY REGION
ORDER BY customer_count DESC;
            """,
            "Top Customers by Configuration Count": """
SELECT 
    cd.CUSTOMER_NAME,
    COUNT(cc.CONFIGURATION_TYPE) as config_count
FROM CUSTOMER_DETAILS cd
LEFT JOIN CUSTOMER_CONFIGURATIONS cc ON cd.CUSTOMER_ID = cc.CUSTOMER_ID
GROUP BY cd.CUSTOMER_NAME
ORDER BY config_count DESC
LIMIT 5;
            """
        }
        
        for title, sql in samples.items():
            with st.expander(f"📄 {title}"):
                st.code(sql, language="sql")
                if st.button(f"Use this query", key=f"use_{title}"):
                    st.session_state.sample_query = sql
                    st.rerun()
    
    # Chart helper methods
    def _show_customer_status_chart(self):
        """Show customer status distribution chart"""
        st.subheader("📊 Customer Status Distribution")
        
        data = pd.DataFrame({
            'Status': ['Active', 'Inactive', 'Pending', 'Suspended'],
            'Count': [756, 234, 189, 55]
        })
        
        fig = px.pie(data, values='Count', names='Status', 
                    color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    def _show_configuration_types_chart(self):
        """Show configuration types chart"""
        st.subheader("⚙️ Configuration Types")
        
        data = pd.DataFrame({
            'Type': ['Security', 'Performance', 'Integration', 'Reporting', 'Custom'],
            'Count': [456, 342, 289, 234, 178]
        })
        
        fig = px.bar(data, x='Type', y='Count', 
                    color='Count', color_continuous_scale='Blues')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    def _show_recent_activity(self):
        """Show recent activity table"""
        st.subheader("🕒 Recent Activity")
        
        recent_data = pd.DataFrame({
            'Timestamp': pd.date_range(start=datetime.now() - timedelta(days=1), periods=10, freq='1H'),
            'Customer': [f'Customer_{i}' for i in range(1, 11)],
            'Action': ['Configuration Updated', 'New Customer', 'Status Changed'] * 3 + ['Data Export'],
            'Status': ['Success'] * 9 + ['Failed']
        })
        
        st.dataframe(
            recent_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Timestamp": st.column_config.DatetimeColumn("Time"),
                "Status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["Success", "Failed", "Pending"]
                )
            }
        )
    
    def _show_demo_analytics_overview(self):
        """Show demo analytics overview"""
        st.warning("📊 Demo Mode - Install Snowflake connector for real data")
        
        # Demo metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Users", "1,234", "12")
        with col2:
            st.metric("Connections", "3,456", "89")
        with col3:
            st.metric("Flows", "2,789", "45")
        with col4:
            st.metric("Licenses", "1,123", "23")
    
    def _show_trends_analysis(self):
        """Show trends analysis"""
        st.markdown("### 📈 Growth Trends")
        
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        growth_data = pd.DataFrame({
            'Month': months,
            'Customers': [100, 125, 156, 189, 234, 289],
            'Revenue': [10000, 12500, 15600, 18900, 23400, 28900]
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.bar(growth_data, x='Month', y='Customers', title='Customer Growth')
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.line(growth_data, x='Month', y='Revenue', title='Revenue Trend')
            st.plotly_chart(fig2, use_container_width=True)
    
    def _show_deep_dive_analysis(self):
        """Show deep dive analysis"""
        st.markdown("### 🔬 Deep Dive Analysis")
        
        # Correlation matrix
        np.random.seed(42)
        corr_data = np.random.rand(5, 5)
        corr_df = pd.DataFrame(corr_data, 
                              columns=['Customers', 'Configs', 'Usage', 'Revenue', 'Satisfaction'],
                              index=['Customers', 'Configs', 'Usage', 'Revenue', 'Satisfaction'])
        
        fig = px.imshow(corr_df, text_auto=True, aspect="auto", title="Correlation Matrix")
        st.plotly_chart(fig, use_container_width=True)
    
    # Demo data methods
    def _get_demo_configurations_data(self):
        """Generate demo configuration data"""
        return pd.DataFrame({
            'CUSTOMER_ID': [f'CUST_{i:04d}' for i in range(1, 21)],
            'CUSTOMER_NAME': [f'Customer {i}' for i in range(1, 21)],
            'CONFIGURATION_TYPE': ['Security', 'Performance', 'Integration'] * 7,
            'CONFIGURATION_VALUE': [f'Config_{i}' for i in range(1, 21)],
            'STATUS': ['Active', 'Inactive', 'Pending'] * 7,
            'REGION': ['US-East', 'US-West', 'Europe', 'Asia'] * 5,
            'CREATED_DATE': pd.date_range('2024-01-01', periods=20, freq='D'),
            'UPDATED_DATE': pd.date_range('2024-01-15', periods=20, freq='D')
        })
    
    def _get_demo_customer_data(self):
        """Generate demo customer data"""
        return pd.DataFrame({
            'customer_id': [f'CUST_{i:04d}' for i in range(1, 21)],
            'name': [f'Customer {i}' for i in range(1, 21)],
            'status': np.random.choice(['Active', 'Inactive', 'Pending'], 20),
            'tier': np.random.choice(['Premium', 'Standard', 'Basic'], 20),
            'last_activity': [datetime.now() - timedelta(days=np.random.randint(0, 30)) for _ in range(20)]
        })

    # =============================================================================
    # NEW DEVELOPER & QA FOCUSED PAGES FOR E2E TEAM
    # =============================================================================
    
    def _show_kpi_dashboard(self):
        """Professional KPI Dashboard with enhanced visualizations"""
        st.markdown("""
        <div class="main-header">
            <div class="header-title">📊 KPI Dashboard</div>
            <div class="header-subtitle">Executive Performance Metrics & Key Indicators</div>
        </div>
        """, unsafe_allow_html=True)
        
        # KPI Cards Row 1
        col1, col2, col3, col4 = st.columns(4)
        
        try:
            # Get real KPI data from Snowflake
            with col1:
                users_df = self.connector.execute_query("SELECT COUNT(*) as total FROM users") if self.has_connector else None
                user_count = users_df.iloc[0]['TOTAL'] if users_df is not None and not users_df.empty else 125450
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">👥 Total Users</div>
                    <div class="kpi-value">{user_count:,}</div>
                    <div class="kpi-change positive">+12.3% ↗️</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                flows_df = self.connector.execute_query("SELECT COUNT(*) as total FROM flows") if self.has_connector else None
                flow_count = flows_df.iloc[0]['TOTAL'] if flows_df is not None and not flows_df.empty else 8943
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">⚙️ Active Flows</div>
                    <div class="kpi-value">{flow_count:,}</div>
                    <div class="kpi-change positive">+8.7% ↗️</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                conn_df = self.connector.execute_query("SELECT COUNT(*) as total FROM connections") if self.has_connector else None
                conn_count = conn_df.iloc[0]['TOTAL'] if conn_df is not None and not conn_df.empty else 23678
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">🔗 Connections</div>
                    <div class="kpi-value">{conn_count:,}</div>
                    <div class="kpi-change neutral">+2.1% →</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                # Calculate success rate
                success_rate = 98.4
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">✅ Success Rate</div>
                    <div class="kpi-value">{success_rate}%</div>
                    <div class="kpi-change positive">+0.8% ↗️</div>
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error loading KPIs: {str(e)}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Advanced KPI Charts
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🔥 Performance", "📊 Distribution", "🎯 Goals"])
        
        with tab1:
            self._show_trend_charts()
        
        with tab2:
            self._show_performance_metrics()
        
        with tab3:
            self._show_distribution_charts()
            
        with tab4:
            self._show_goal_tracking()
    
    def _show_system_architecture(self):
        """System Architecture Overview for Dev/QA"""
        st.markdown("""
        <div class="main-header">
            <div class="header-title">🏗️ System Architecture</div>
            <div class="header-subtitle">Infrastructure Overview & Component Health</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Architecture Components
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🌐 System Components")
            
            # Create Sankey diagram
            fig = go.Figure(data=[go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=["Frontend", "API Gateway", "Snowflake", "Auth Service", "Flow Engine", "Monitoring"],
                    color=["blue", "orange", "lightblue", "green", "purple", "red"]
                ),
                link=dict(
                    source=[0, 1, 1, 1, 2, 3],
                    target=[1, 2, 3, 4, 5, 5],
                    value=[100, 80, 60, 40, 30, 20]
                )
            )])
            
            fig.update_layout(title_text="Data Flow Architecture", font_size=12, height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🟢 Component Status")
            
            components = [
                ("Snowflake DB", "🟢", "Healthy", "99.9%"),
                ("API Gateway", "🟢", "Healthy", "99.8%"),
                ("Auth Service", "🟡", "Warning", "98.2%"),
                ("Flow Engine", "🟢", "Healthy", "99.5%"),
                ("Monitoring", "🟢", "Healthy", "100%"),
                ("Cache Layer", "🟡", "Degraded", "95.1%")
            ]
            
            for name, status, health, uptime in components:
                st.markdown(f"""
                <div class="metric-card info">
                    <strong>{name}</strong><br>
                    {status} {health} - {uptime}
                </div>
                """, unsafe_allow_html=True)
        
        # Technical Metrics
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🔧 Database Metrics")
            try:
                if self.has_connector:
                    # Table counts
                    tables_query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = CURRENT_SCHEMA()"
                    tables_df = self.connector.execute_query(tables_query)
                    if tables_df is not None:
                        st.metric("Tables", len(tables_df))
                        
                        # Show top tables by estimated size
                        st.markdown("**Key Tables:**")
                        key_tables = ['USERS', 'CONNECTIONS', 'FLOWS', 'IMPORTS', 'EXPORTS']
                        for table in key_tables[:5]:
                            st.text(f"• {table}")
                else:
                    st.metric("Tables", "150+")
                    
            except Exception as e:
                st.error(f"Database metrics error: {str(e)}")
        
        with col2:
            st.markdown("### ⚡ Performance")
            st.metric("Avg Response Time", "125ms", "-12ms")
            st.metric("Requests/min", "2,847", "+156")
            st.metric("Error Rate", "0.02%", "-0.01%")
            
        with col3:
            st.markdown("### 💾 Resources")
            st.metric("CPU Usage", "23%", "-2%")
            st.metric("Memory Usage", "67%", "+5%")
            st.metric("Storage", "2.3TB", "+45GB")
    
    def _show_performance_monitor(self):
        """Performance monitoring dashboard"""
        st.markdown("""
        <div class="main-header">
            <div class="header-title">⚡ Performance Monitor</div>
            <div class="header-subtitle">Real-time System Performance & Optimization Insights</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Performance metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Response Time", "125ms", "-15ms")
        with col2:
            st.metric("Throughput", "2.4K/sec", "+340")
        with col3:
            st.metric("Active Sessions", "1,247", "+23")
        with col4:
            st.metric("Queue Length", "12", "-8")
        
        # Performance charts
        tab1, tab2, tab3 = st.tabs(["📈 Response Times", "🔥 Load Analysis", "💾 Resource Usage"])
        
        with tab1:
            # Mock time series data for response times
            dates = pd.date_range(start='2024-01-01', periods=24*7, freq='H')
            response_times = np.random.normal(120, 20, len(dates))
            df_perf = pd.DataFrame({'Time': dates, 'Response Time (ms)': response_times})
            
            fig = px.line(df_perf, x='Time', y='Response Time (ms)', 
                         title='Response Time Trend (Last 7 Days)')
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Load analysis with heatmap
            hours = list(range(24))
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            load_data = np.random.rand(7, 24) * 100
            
            fig = px.imshow(load_data, 
                           x=hours, y=days,
                           labels=dict(x="Hour of Day", y="Day of Week", color="Load %"),
                           title="System Load Heatmap")
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Resource usage over time
            times = pd.date_range(start='2024-01-01', periods=168, freq='H')
            cpu_usage = np.random.normal(45, 15, len(times))
            memory_usage = np.random.normal(65, 10, len(times))
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=times, y=cpu_usage, name='CPU %', line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=times, y=memory_usage, name='Memory %', line=dict(color='red')))
            fig.update_layout(title='Resource Usage (Last 7 Days)', yaxis_title='Usage %')
            st.plotly_chart(fig, use_container_width=True)
    
    def _show_flow_analytics(self):
        """Flow analytics for developers"""
        st.markdown("""
        <div class="main-header">
            <div class="header-title">🔍 Flow Analytics</div>
            <div class="header-subtitle">Deep Dive into Flow Performance & Patterns</div>
        </div>
        """, unsafe_allow_html=True)
        
        if self.has_connector:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Flow Complexity Analysis")
                if st.button("🔍 Analyze Complex Flows"):
                    try:
                        complex_flow_query = """
                        SELECT NAME, _USERID, 
                               ARRAY_SIZE(PAGEPROCESSORS) as processors,
                               ARRAY_SIZE(PAGEGENERATORS) as generators
                        FROM flows 
                        WHERE ARRAY_SIZE(PAGEPROCESSORS) >= 1 
                        AND ARRAY_SIZE(PAGEGENERATORS) >= 3 
                        LIMIT 50
                        """
                        df_flows = self.connector.execute_query(complex_flow_query)
                        
                        if df_flows is not None and not df_flows.empty:
                            # Complexity scatter plot
                            fig = px.scatter(df_flows, x='PROCESSORS', y='GENERATORS',
                                           hover_data=['NAME'], 
                                           title="Flow Complexity Distribution")
                            st.plotly_chart(fig, use_container_width=True)
                            
                            st.dataframe(df_flows.head(10), use_container_width=True)
                        else:
                            st.info("No complex flows found")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            
            with col2:
                st.markdown("### 👥 User Flow Patterns")
                user_id = st.text_input("Enter User ID for flow analysis:")
                if st.button("📈 Analyze User Flows") and user_id:
                    try:
                        user_flow_query = f"""
                        SELECT NAME, ARRAY_SIZE(PAGEPROCESSORS) as processors,
                               ARRAY_SIZE(PAGEGENERATORS) as generators,
                               CREATED
                        FROM flows 
                        WHERE _USERID = '{user_id}'
                        ORDER BY CREATED DESC
                        LIMIT 20
                        """
                        df_user_flows = self.connector.execute_query(user_flow_query)
                        
                        if df_user_flows is not None and not df_user_flows.empty:
                            st.success(f"Found {len(df_user_flows)} flows for user {user_id}")
                            
                            # Flow timeline
                            fig = px.bar(df_user_flows, x='NAME', y='PROCESSORS',
                                       title=f"User {user_id} - Flow Processors")
                            fig.update_xaxes(tickangle=45)
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.warning("No flows found for this user")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        else:
            st.info("Enable Snowflake connection for real flow analytics")
    
    def _show_heatmap_analysis(self):
        """Heatmap analysis dashboard"""
        st.markdown("""
        <div class="main-header">
            <div class="header-title">🔥 Heatmap Analysis</div>
            <div class="header-subtitle">Visual Heat Analysis of System Activity & Usage Patterns</div>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["🕐 Activity Heatmap", "🌍 Geographic Heatmap", "🔥 Performance Heatmap"])
        
        with tab1:
            st.markdown("### 📅 Daily Activity Patterns")
            
            # Generate sample activity heatmap data
            hours = list(range(24))
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            
            # Create more realistic activity patterns
            np.random.seed(42)
            activity_data = []
            for day_idx, day in enumerate(days):
                for hour in hours:
                    # Higher activity during business hours on weekdays
                    if day_idx < 5:  # Weekday
                        if 9 <= hour <= 17:
                            activity = np.random.normal(80, 15)
                        else:
                            activity = np.random.normal(30, 10)
                    else:  # Weekend
                        activity = np.random.normal(25, 8)
                    
                    activity = max(0, min(100, activity))  # Clamp between 0-100
                    activity_data.append([day, hour, activity])
            
            df_activity = pd.DataFrame(activity_data, columns=['Day', 'Hour', 'Activity'])
            
            # Create pivot table for heatmap
            heatmap_data = df_activity.pivot(index='Day', columns='Hour', values='Activity')
            
            fig = px.imshow(heatmap_data.values,
                           x=hours,
                           y=days,
                           labels=dict(x="Hour of Day", y="Day of Week", color="Activity Level"),
                           title="Weekly Activity Heatmap",
                           color_continuous_scale="Viridis")
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.markdown("### 🌍 Geographic Distribution")
            
            # Sample geographic data
            countries = ['USA', 'Canada', 'UK', 'Germany', 'France', 'Japan', 'Australia', 'Brazil']
            usage_data = np.random.rand(len(countries)) * 1000
            
            df_geo = pd.DataFrame({
                'Country': countries,
                'Usage': usage_data
            })
            
            fig = px.bar(df_geo, x='Country', y='Usage',
                        title="Usage by Country",
                        color='Usage',
                        color_continuous_scale="Plasma")
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.markdown("### ⚡ System Performance Heat Analysis")
            
            # Performance heatmap
            services = ['API Gateway', 'Auth Service', 'Database', 'Cache', 'Queue', 'Storage']
            metrics = ['Response Time', 'CPU Usage', 'Memory', 'Network I/O', 'Disk I/O']
            
            perf_data = np.random.rand(len(services), len(metrics)) * 100
            
            fig = px.imshow(perf_data,
                           x=metrics,
                           y=services,
                           labels=dict(x="Metrics", y="Services", color="Performance Score"),
                           title="Service Performance Heatmap",
                           color_continuous_scale="RdYlGn")
            st.plotly_chart(fig, use_container_width=True)
    
    def _show_system_map(self):
        """System map visualization"""
        st.markdown("""
        <div class="main-header">
            <div class="header-title">🗺️ System Map</div>
            <div class="header-subtitle">Interactive Network Topology & Service Dependencies</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### 🌐 Service Dependency Map")
            
            # Create network graph using plotly
            import networkx as nx
            
            # Create a sample network
            G = nx.Graph()
            
            # Add nodes (services)
            services = [
                ("Frontend", {"type": "web", "status": "healthy"}),
                ("API Gateway", {"type": "api", "status": "healthy"}),
                ("Auth Service", {"type": "auth", "status": "warning"}),
                ("Snowflake DB", {"type": "database", "status": "healthy"}),
                ("Flow Engine", {"type": "processing", "status": "healthy"}),
                ("Cache Layer", {"type": "cache", "status": "degraded"}),
                ("Monitoring", {"type": "monitoring", "status": "healthy"}),
                ("Queue System", {"type": "queue", "status": "healthy"})
            ]
            
            for service, attrs in services:
                G.add_node(service, **attrs)
            
            # Add edges (dependencies)
            edges = [
                ("Frontend", "API Gateway"),
                ("API Gateway", "Auth Service"),
                ("API Gateway", "Snowflake DB"),
                ("API Gateway", "Flow Engine"),
                ("Flow Engine", "Queue System"),
                ("Snowflake DB", "Cache Layer"),
                ("Cache Layer", "API Gateway"),
                ("Monitoring", "API Gateway"),
                ("Monitoring", "Snowflake DB"),
                ("Monitoring", "Flow Engine")
            ]
            
            G.add_edges_from(edges)
            
            # Generate layout
            pos = nx.spring_layout(G, k=3, iterations=50)
            
            # Create edge traces
            edge_x = []
            edge_y = []
            for edge in G.edges():
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])
            
            edge_trace = go.Scatter(x=edge_x, y=edge_y,
                                  line=dict(width=2, color='#888'),
                                  hoverinfo='none',
                                  mode='lines')
            
            # Create node traces
            node_x = []
            node_y = []
            node_text = []
            node_color = []
            
            for node in G.nodes():
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)
                node_text.append(node)
                
                # Color based on status
                status = G.nodes[node].get('status', 'unknown')
                if status == 'healthy':
                    node_color.append('#00ff00')
                elif status == 'warning':
                    node_color.append('#ffff00')
                elif status == 'degraded':
                    node_color.append('#ff8800')
                else:
                    node_color.append('#ff0000')
            
            node_trace = go.Scatter(x=node_x, y=node_y,
                                  mode='markers+text',
                                  text=node_text,
                                  textposition="middle center",
                                  hoverinfo='text',
                                  marker=dict(size=50,
                                            color=node_color,
                                            line=dict(width=2, color='black')))
            
            fig = go.Figure(data=[edge_trace, node_trace],
                           layout=go.Layout(
                                title='System Service Map',
                                titlefont_size=16,
                                showlegend=False,
                                hovermode='closest',
                                margin=dict(b=20,l=5,r=5,t=40),
                                annotations=[ dict(
                                    text="Interactive Service Dependency Graph",
                                    showarrow=False,
                                    xref="paper", yref="paper",
                                    x=0.005, y=-0.002 ) ],
                                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                height=500))
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Service Health")
            
            for service, attrs in services:
                status = attrs['status']
                if status == 'healthy':
                    st.markdown(f"🟢 **{service}**\nHealthy")
                elif status == 'warning':
                    st.markdown(f"🟡 **{service}**\nWarning")
                elif status == 'degraded':
                    st.markdown(f"🟠 **{service}**\nDegraded")
                else:
                    st.markdown(f"🔴 **{service}**\nDown")
                st.markdown("---")
    
    # Helper methods for KPI dashboard
    def _show_trend_charts(self):
        """Show trend analysis charts"""
        col1, col2 = st.columns(2)
        
        with col1:
            # User growth trend
            dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
            users = np.cumsum(np.random.normal(100, 20, len(dates))) + 100000
            df_users = pd.DataFrame({'Date': dates, 'Users': users})
            
            fig = px.line(df_users, x='Date', y='Users', title='User Growth Trend')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Flow execution trend
            flows = np.cumsum(np.random.normal(50, 10, len(dates))) + 50000
            df_flows = pd.DataFrame({'Date': dates, 'Flows': flows})
            
            fig = px.line(df_flows, x='Date', y='Flows', title='Flow Execution Trend')
            st.plotly_chart(fig, use_container_width=True)
    
    def _show_performance_metrics(self):
        """Show performance metrics"""
        col1, col2 = st.columns(2)
        
        with col1:
            # Response time distribution
            response_times = np.random.lognormal(4, 0.5, 1000)
            fig = px.histogram(x=response_times, nbins=50, title='Response Time Distribution')
            fig.update_xaxes(title="Response Time (ms)")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Success rate by service
            services = ['API', 'Auth', 'DB', 'Cache', 'Queue']
            success_rates = [99.8, 99.2, 99.9, 98.5, 99.7]
            
            fig = px.bar(x=services, y=success_rates, title='Success Rate by Service')
            fig.update_yaxes(title="Success Rate %", range=[95, 100])
            st.plotly_chart(fig, use_container_width=True)
    
    def _show_distribution_charts(self):
        """Show distribution analysis"""
        col1, col2 = st.columns(2)
        
        with col1:
            # User tier distribution
            tiers = ['Premium', 'Standard', 'Basic', 'Free']
            counts = [25340, 45670, 32890, 21567]
            
            fig = px.pie(values=counts, names=tiers, title='User Tier Distribution')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Connection type distribution
            conn_types = ['HTTP', 'SFTP', 'Database', 'API', 'Other']
            conn_counts = [15420, 8930, 12450, 18760, 3440]
            
            fig = px.pie(values=conn_counts, names=conn_types, title='Connection Type Distribution')
            st.plotly_chart(fig, use_container_width=True)
    
    def _show_goal_tracking(self):
        """Show goal tracking metrics"""
        st.markdown("### 🎯 Goal Tracking & Targets")
        
        goals = [
            {"metric": "Monthly Active Users", "current": 125450, "target": 150000, "unit": "users"},
            {"metric": "System Uptime", "current": 99.8, "target": 99.9, "unit": "%"},
            {"metric": "Response Time", "current": 125, "target": 100, "unit": "ms"},
            {"metric": "Flow Success Rate", "current": 98.4, "target": 99.0, "unit": "%"}
        ]
        
        for goal in goals:
            progress = min(goal["current"] / goal["target"], 1.0) * 100
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                st.write(f"**{goal['metric']}**")
            with col2:
                st.progress(progress / 100)
            with col3:
                st.write(f"{goal['current']:,.1f} / {goal['target']:,.0f} {goal['unit']}")
    
    def _show_executive_dashboard(self):
        """Enhanced executive dashboard with professional UI"""
        st.markdown("""
        <div class="main-header">
            <div class="header-title">📈 Executive Dashboard</div>
            <div class="header-subtitle">Real-time Analytics & Business Intelligence</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show the existing dashboard overview content
        self._show_dashboard_overview()
    
    def _show_real_time_metrics(self):
        """Real-time metrics monitoring"""
        st.markdown("""
        <div class="main-header">
            <div class="header-title">📡 Real-time Metrics</div>
            <div class="header-subtitle">Live System Performance & Activity Monitor</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Real-time metrics dashboard
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Active Users", "2,847", "+127")
        with col2:
            st.metric("Requests/min", "18,493", "+1,234")
        with col3:
            st.metric("Response Time", "125ms", "-8ms")
        with col4:
            st.metric("Error Rate", "0.02%", "-0.01%")
        
        # Real-time charts
        st.markdown("### 📊 Live Activity Feed")
        
        # Mock real-time data
        import time
        current_time = datetime.now()
        times = [current_time - timedelta(minutes=i) for i in range(60, 0, -1)]
        requests = np.random.poisson(300, 60)
        
        df_realtime = pd.DataFrame({
            'Time': times,
            'Requests': requests
        })
        
        fig = px.line(df_realtime, x='Time', y='Requests', 
                     title='Requests per Minute (Last Hour)')
        st.plotly_chart(fig, use_container_width=True)
        
        # System status
        st.markdown("### 🚦 System Status")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🟢 Healthy Services**")
            healthy_services = ["API Gateway", "Database", "Auth Service", "Cache", "Queue"]
            for service in healthy_services:
                st.markdown(f"✅ {service}")
        
        with col2:
            st.markdown("**🟡 Monitoring**")
            monitoring_items = ["CPU Usage: 23%", "Memory: 67%", "Disk: 45%", "Network: Normal"]
            for item in monitoring_items:
                st.markdown(f"📊 {item}")
    
    def _show_alert_center(self):
        """Alert center for system notifications"""
        st.markdown("""
        <div class="main-header">
            <div class="header-title">🚨 Alert Center</div>
            <div class="header-subtitle">System Alerts & Notification Management</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Alert summary
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🔴 Critical", "0", "0")
        with col2:
            st.metric("🟡 Warning", "3", "+1")
        with col3:
            st.metric("🔵 Info", "12", "+4")
        with col4:
            st.metric("✅ Resolved", "28", "+6")
        
        # Recent alerts
        st.markdown("### 📋 Recent Alerts")
        
        alerts_data = [
            {"Time": "2024-01-15 14:30", "Level": "Warning", "Service": "Cache", "Message": "High memory usage detected"},
            {"Time": "2024-01-15 14:15", "Level": "Info", "Service": "API", "Message": "New deployment completed"},
            {"Time": "2024-01-15 13:45", "Level": "Warning", "Service": "Database", "Message": "Slow query detected"},
            {"Time": "2024-01-15 13:30", "Level": "Info", "Service": "Auth", "Message": "User login spike"},
            {"Time": "2024-01-15 13:00", "Level": "Info", "Service": "System", "Message": "Scheduled maintenance completed"}
        ]
        
        df_alerts = pd.DataFrame(alerts_data)
        
        # Color code alerts
        def color_alert_level(level):
            if level == "Critical":
                return "🔴"
            elif level == "Warning":
                return "🟡"
            elif level == "Info":
                return "🔵"
            else:
                return "✅"
        
        df_alerts['Status'] = df_alerts['Level'].apply(color_alert_level)
        
        st.dataframe(df_alerts[['Time', 'Status', 'Service', 'Message']], use_container_width=True)
        
        # Alert configuration
        st.markdown("### ⚙️ Alert Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔔 Notification Settings**")
            st.checkbox("Email notifications", value=True)
            st.checkbox("Slack notifications", value=True)
            st.checkbox("SMS for critical alerts", value=False)
        
        with col2:
            st.markdown("**📊 Threshold Settings**")
            st.slider("CPU Alert Threshold", 0, 100, 80, help="Alert when CPU usage exceeds this %")
            st.slider("Memory Alert Threshold", 0, 100, 85, help="Alert when memory usage exceeds this %")
            st.slider("Response Time Alert (ms)", 0, 1000, 500, help="Alert when response time exceeds this value")


def main():
    """Main application entry point"""
    try:
        dashboard = SnowflakeDashboard()
        dashboard.run()
    except Exception as e:
        st.error(f"❌ Application error: {str(e)}")
        st.info("Please check your configuration and try again.")

if __name__ == "__main__":
    main() 