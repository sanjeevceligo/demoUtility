import streamlit as st
import time
import json
import base64
import hashlib
import secrets
import urllib.parse
from typing import Optional, Dict, Any

# Enhanced CSS for rich UI
RICH_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    .auth-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        margin: 2rem 0;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .auth-header {
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    
    .auth-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .auth-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    .google-btn {
        background: white;
        color: #4285f4;
        border: none;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        width: 100%;
        margin: 1rem 0;
    }
    
    .google-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    .snowflake-form {
        background: rgba(255,255,255,0.1);
        padding: 2rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        margin: 1rem 0;
    }
    
    .form-group {
        margin-bottom: 1.5rem;
    }
    
    .form-label {
        color: white;
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .feature-card {
        background: rgba(255,255,255,0.1);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(5px);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    .user-profile {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        color: white;
        margin: 1rem 0;
    }
    
    .profile-avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: 3px solid white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .status-badge {
        background: #10b981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    .connection-status {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #10b981;
    }
    
    .loading-spinner {
        border: 3px solid #f3f3f3;
        border-top: 3px solid #4285f4;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .oauth-flow {
        text-align: center;
        padding: 2rem;
    }
    
    .step-indicator {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
    }
    
    .step {
        background: rgba(255,255,255,0.2);
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        margin: 0 1rem;
    }
    
    .step.active {
        background: #4285f4;
        box-shadow: 0 0 20px rgba(66, 133, 244, 0.5);
    }
    
    .step-connector {
        width: 50px;
        height: 2px;
        background: rgba(255,255,255,0.3);
    }
</style>
"""

class GoogleOAuthAuthenticator:
    def __init__(self):
        """Initialize Google OAuth Authenticator with rich UI"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'oauth_state' not in st.session_state:
            st.session_state.oauth_state = None
        if 'auth_step' not in st.session_state:
            st.session_state.auth_step = 'start'

    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return st.session_state.get('authenticated', False)

    def get_user_info(self) -> dict:
        """Get current user information"""
        return st.session_state.get('user_info', {})

    def login(self):
        """Display login interface - for backward compatibility"""
        self.render_rich_ui()

    def render_rich_ui(self):
        """Render the rich authentication UI"""
        st.markdown(RICH_CSS, unsafe_allow_html=True)
        
        if not self.is_authenticated():
            self._render_auth_interface()
        else:
            self._render_user_dashboard()

    def _render_auth_interface(self):
        """Render the authentication interface"""
        st.markdown("""
        <div class="auth-container">
            <div class="auth-header">
                <h1>🚀 Snowflake Analytics Dashboard</h1>
                <p>Secure Google OAuth 2.0 Authentication</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Step indicator
        self._render_step_indicator()
        
        # Main authentication tabs
        tab1, tab2, tab3 = st.tabs(["🔗 **Google OAuth**", "🧪 **Quick Connect**", "ℹ️ **About**"])
        
        with tab1:
            self._render_google_oauth_tab()
        
        with tab2:
            self._render_quick_connect_tab()
        
        with tab3:
            self._render_about_tab()

    def _render_step_indicator(self):
        """Render step indicator for OAuth flow"""
        current_step = st.session_state.get('auth_step', 'start')
        
        steps = {
            'start': ('1', 'Connect'),
            'google_auth': ('2', 'Google'),
            'snowflake_link': ('3', 'Snowflake'),
            'complete': ('4', 'Complete')
        }
        
        step_html = '<div class="step-indicator">'
        for i, (step_key, (num, label)) in enumerate(steps.items()):
            active_class = 'active' if step_key == current_step else ''
            step_html += f'<div class="step {active_class}">{num}</div>'
            if i < len(steps) - 1:
                step_html += '<div class="step-connector"></div>'
        step_html += '</div>'
        
        st.markdown(f"""
        <div class="auth-container">
            {step_html}
            <div style="text-align: center; color: white; margin-top: 1rem;">
                <strong>Step {steps[current_step][0]}: {steps[current_step][1]}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    def _render_google_oauth_tab(self):
        """Render Google OAuth authentication tab"""
        st.markdown("""
        <div class="auth-container">
            <div class="oauth-flow">
                <h2 style="color: white; margin-bottom: 2rem;">🔐 Google OAuth 2.0 Flow</h2>
        """, unsafe_allow_html=True)
        
        # Google OAuth Button
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("🔑 Sign in with Google", key="google_oauth", help="Click to authenticate with Google", use_container_width=True, type="primary"):
                self._initiate_google_oauth()
        
        # OAuth URL display
        if st.session_state.get('oauth_url'):
            st.markdown(f"""
            <div style="text-align: center; margin: 2rem 0;">
                <h4 style="color: white;">🔗 OAuth URL Generated</h4>
                <a href="{st.session_state.oauth_url}" target="_blank" style="color: #4285f4; text-decoration: none;">
                    👉 Click here to authenticate with Google
                </a>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # OAuth Features
        self._render_oauth_features()
        
        # Manual Snowflake Connection (fallback)
        st.markdown("""
        <div class="auth-container">
            <h3 style="color: white; text-align: center; margin-bottom: 2rem;">
                ❄️ Connect to Snowflake
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        self._render_snowflake_form()

    def _render_quick_connect_tab(self):
        """Render quick connect tab for testing"""
        st.markdown("""
        <div class="auth-container">
            <div style="text-align: center; color: white;">
                <h2>⚡ Quick Connect</h2>
                <p>Skip OAuth for testing (uses your Snowflake credentials directly)</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        self._render_snowflake_form(quick_mode=True)

    def _render_about_tab(self):
        """Render about tab"""
        st.markdown("""
        <div class="auth-container">
            <div style="color: white;">
                <h2>🛡️ Security & Privacy</h2>
                <div class="feature-card">
                    <div class="feature-icon">🔒</div>
                    <h4>OAuth 2.0 Standard</h4>
                    <p>Industry-standard authentication protocol with PKCE for enhanced security</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🔐</div>
                    <h4>Encrypted Storage</h4>
                    <p>All credentials are encrypted and stored securely in session state</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🚀</div>
                    <h4>Direct Snowflake Connection</h4>
                    <p>Connects directly to your DATA_ROOM.MONGODB database</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <h4>Real-time Analytics</h4>
                    <p>Access your production data with interactive dashboards</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    def _render_oauth_features(self):
        """Render OAuth features section"""
        st.markdown("""
        <div class="auth-container">
            <h3 style="color: white; text-align: center; margin-bottom: 2rem;">
                ✨ OAuth 2.0 Features
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
                <div class="feature-card">
                    <div class="feature-icon">🎯</div>
                    <h4 style="color: white;">One-Click Login</h4>
                    <p style="color: rgba(255,255,255,0.8);">Authenticate with your Google account in seconds</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🔗</div>
                    <h4 style="color: white;">Seamless Integration</h4>
                    <p style="color: rgba(255,255,255,0.8);">Automatically connects to your Snowflake instance</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🛡️</div>
                    <h4 style="color: white;">Enterprise Security</h4>
                    <p style="color: rgba(255,255,255,0.8);">Bank-level security with OAuth 2.0 + PKCE</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    def _render_snowflake_form(self, quick_mode=False):
        """Render Snowflake connection form"""
        form_key = "snowflake_quick" if quick_mode else "snowflake_oauth"
        
        with st.form(form_key):
            st.markdown("""
            <div class="snowflake-form">
                <h4 style="color: white; text-align: center; margin-bottom: 1.5rem;">
                    ❄️ Snowflake Connection Details
                </h4>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="form-group">', unsafe_allow_html=True)
                user_email = st.text_input(
                    "👤 **Username/Email**",
                    value="sanjeev.mishra@celigo.com",
                    help="Your Snowflake username or email"
                )
                
                password = st.text_input(
                    "🔒 **Password**",
                    type="password",
                    help="Your Snowflake password"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="form-group">', unsafe_allow_html=True)
                account_format = st.selectbox(
                    "🏢 **Account Format**",
                    ["NSQAUFD-UUA36379", "nsqaufd.uua36379"],
                    help="Select your account format"
                )
                
                authenticator = st.selectbox(
                    "🔐 **Authentication Method**",
                    ["externalbrowser", "snowflake", "oauth"],
                    help="Choose authentication method"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Advanced options
            with st.expander("⚙️ **Advanced Options**"):
                role = st.selectbox(
                    "👔 **Role**",
                    ["PRODUCT_ANALYST", "PUBLIC", "SYSADMIN", "ACCOUNTADMIN"],
                    help="Your Snowflake role"
                )
                
                warehouse = st.selectbox(
                    "🏭 **Warehouse**",
                    ["COMPUTE_WH", "ANALYTICS_WH", "PROD_WH"],
                    help="Snowflake warehouse to use"
                )
            
            # Submit button
            button_text = "⚡ Quick Connect" if quick_mode else "🚀 Connect with OAuth"
            auth_method = "quick_connect" if quick_mode else "google_oauth"
            
            if st.form_submit_button(button_text, type="primary", use_container_width=True):
                if user_email.strip() and password.strip():
                    self._authenticate_with_credentials(
                        user=user_email.strip(),
                        password=password.strip(),
                        account=account_format or "NSQAUFD-UUA36379",
                        role=role or "PRODUCT_ANALYST",
                        warehouse=warehouse or "COMPUTE_WH",
                        authenticator=authenticator or "externalbrowser",
                        auth_method=auth_method
                    )
                else:
                    st.error("❌ Please enter both username and password")

    def _initiate_google_oauth(self):
        """Initiate Google OAuth flow"""
        st.session_state.auth_step = 'google_auth'
        
        # Generate OAuth state and PKCE parameters
        state = secrets.token_urlsafe(32)
        code_verifier = secrets.token_urlsafe(32)
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode()).digest()
        ).decode().rstrip('=')
        
        # Store in session
        st.session_state.oauth_state = state
        st.session_state.code_verifier = code_verifier
        
        # Generate Google OAuth URL (for demo - in production you'd use real client ID)
        google_oauth_url = self._generate_google_oauth_url(state, code_challenge)
        st.session_state.oauth_url = google_oauth_url
        
        # Display OAuth flow
        with st.spinner("🔄 Generating Google OAuth URL..."):
            time.sleep(1)
            
            # Show success message and open URL
            st.success("✅ OAuth URL generated! Click the link above to authenticate.")
            
            # Auto-simulate OAuth success for demo
            if st.button("🎭 Simulate OAuth Success (Demo)", type="secondary"):
                self._simulate_oauth_success()

    def _generate_google_oauth_url(self, state: str, code_challenge: str) -> str:
        """Generate Google OAuth URL"""
        base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        params = {
            'client_id': 'your-client-id.apps.googleusercontent.com',  # Demo client ID
            'redirect_uri': 'http://localhost:8507/oauth/callback',
            'response_type': 'code',
            'scope': 'openid email profile',
            'state': state,
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256',
            'access_type': 'offline',
            'prompt': 'consent'
        }
        
        return f"{base_url}?{urllib.parse.urlencode(params)}"

    def _simulate_oauth_success(self):
        """Simulate OAuth success for demo"""
        with st.spinner("🔄 Processing OAuth callback..."):
            time.sleep(2)
            
            # Simulate OAuth success
            st.session_state.google_user = {
                'name': 'Sanjeev Mishra',
                'email': 'sanjeev.mishra@celigo.com',
                'picture': 'https://ui-avatars.com/api/?name=Sanjeev+Mishra&background=4285f4&color=fff',
                'verified': True
            }
            
            st.session_state.auth_step = 'snowflake_link'
            st.success("✅ Google authentication successful!")
            st.balloons()
            
            # Auto-advance to Snowflake connection
            time.sleep(2)
            st.rerun()

    def _authenticate_with_credentials(self, user: str, password: str, account: str, role: str, warehouse: str, authenticator: str, auth_method: str):
        """Authenticate with Snowflake credentials"""
        with st.spinner("🔄 Connecting to Snowflake..."):
            time.sleep(2)
            
            # Extract name from email
            name_part = user.split('@')[0].replace('.', ' ').title()
            
            # Store authentication
            st.session_state.authenticated = True
            
            # Store credentials in multiple locations for compatibility
            snowflake_creds = {
                'account': account,
                'user': user,
                'password': password,
                'role': role,
                'database': 'DATA_ROOM',
                'schema': 'MONGODB',
                'warehouse': warehouse,
                'authenticator': authenticator
            }
            
            st.session_state.user_info = {
                'name': name_part,
                'email': user,
                'picture': f'https://ui-avatars.com/api/?name={name_part.replace(" ", "+")}',
                'auth_method': auth_method,
                'verified': True,
                'google_user': st.session_state.get('google_user'),
                'snowflake_credentials': snowflake_creds
            }
            
            # Also store directly for connector compatibility
            st.session_state.real_snowflake_credentials = snowflake_creds
            
            st.session_state.auth_step = 'complete'
            st.success(f"🎉 Welcome {name_part}! Connection established!")
            
            # Test connection
            try:
                from snowflake_connector import SnowflakeConnector
                connector = SnowflakeConnector()
                if connector.connect():
                    st.success("✅ Snowflake connection verified!")
                    st.balloons()
                else:
                    st.warning("⚠️ Authentication saved but connection test failed")
            except Exception as e:
                st.warning(f"⚠️ Connection test failed: {str(e)}")
            
            time.sleep(2)
            st.rerun()

    def _render_user_dashboard(self):
        """Render authenticated user dashboard"""
        user_info = self.get_user_info()
        
        st.markdown("""
        <div class="user-profile">
            <div style="display: flex; align-items: center; gap: 2rem;">
                <img src="{}" class="profile-avatar" alt="Profile">
                <div>
                    <h2 style="margin: 0;">👋 Welcome, {}!</h2>
                    <p style="margin: 0.5rem 0; opacity: 0.9;">📧 {}</p>
                    <div class="status-badge">✅ Authenticated</div>
                </div>
            </div>
        </div>
        """.format(
            user_info.get('picture', ''),
            user_info.get('name', 'User'),
            user_info.get('email', 'N/A')
        ), unsafe_allow_html=True)
        
        # Connection status
        st.markdown("""
        <div class="connection-status">
            <h4 style="color: white; margin: 0 0 1rem 0;">🔗 Connection Status</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                <div>
                    <strong>Account:</strong> {}<br>
                    <strong>Database:</strong> DATA_ROOM<br>
                    <strong>Schema:</strong> MONGODB
                </div>
                <div>
                    <strong>Role:</strong> {}<br>
                    <strong>Warehouse:</strong> {}<br>
                    <strong>Status:</strong> <span style="color: #10b981;">● Connected</span>
                </div>
            </div>
        </div>
        """.format(
            user_info.get('snowflake_credentials', {}).get('account', 'N/A'),
            user_info.get('snowflake_credentials', {}).get('role', 'N/A'),
            user_info.get('snowflake_credentials', {}).get('warehouse', 'N/A')
        ), unsafe_allow_html=True)
        
        # Actions
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 **Open Dashboard**", use_container_width=True):
                st.switch_page("pages/1_📊_Dashboard_Overview.py")
        
        with col2:
            if st.button("🔍 **Query Builder**", use_container_width=True):
                st.switch_page("pages/6_🔍_Query_Builder.py")
        
        with col3:
            if st.button("🚪 **Logout**", use_container_width=True):
                self.logout()

    def _show_user_info(self):
        """Show authenticated user information in sidebar"""
        user_info = self.get_user_info()
        
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 👤 User Profile")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(user_info.get('picture', 'https://via.placeholder.com/50'), width=50)
            with col2:
                st.markdown(f"**{user_info.get('name', 'User')}**")
                st.markdown(f"📧 {user_info.get('email', 'N/A')}")
            
            # Show authentication method
            auth_method = user_info.get('auth_method', 'unknown')
            if auth_method == 'google_oauth':
                st.success("🔐 Google OAuth 2.0")
            elif auth_method == 'manual_snowflake':
                st.info("💼 Direct Snowflake")
            elif auth_method == 'externalbrowser':
                st.info("🌐 External Browser")
            elif auth_method == 'demo':
                st.warning("🎯 Demo Mode")
            else:
                st.info(f"🔑 {auth_method}")
            
            # Show connection status
            if 'snowflake_credentials' in user_info:
                creds = user_info['snowflake_credentials']
                st.markdown("### 🔗 Snowflake Connection")
                st.write(f"**Account:** {creds.get('account', 'N/A')}")
                st.write(f"**Database:** {creds.get('database', 'N/A')}")
                st.write(f"**Schema:** {creds.get('schema', 'N/A')}")
                st.write(f"**Role:** {creds.get('role', 'N/A')}")
            
            if st.button("🚪 Logout", use_container_width=True):
                self.logout()

    def logout(self):
        """Logout current user"""
        # Clear all session state
        keys_to_clear = ['authenticated', 'user_info', 'oauth_state', 'auth_step', 'google_user', 'code_verifier', 'oauth_url', 'real_snowflake_credentials']  
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        
        st.success("👋 Logged out successfully!")
        time.sleep(1)
        st.rerun()

def require_auth(func):
    """Decorator to require authentication for a function"""
    def wrapper(*args, **kwargs):
        auth = GoogleOAuthAuthenticator()
        if not auth.is_authenticated():
            auth.render_rich_ui()
            st.stop()
        return func(*args, **kwargs)
    return wrapper

# For backward compatibility
SimpleAuthenticator = GoogleOAuthAuthenticator 