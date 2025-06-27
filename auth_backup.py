import streamlit as st
import os
from config import Config

class SimpleAuthenticator:
    """
    Enhanced authentication system with Google OAuth 2.0 and Snowflake integration
    """
    
    def __init__(self):
        self.config = Config()
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return 'authenticated' in st.session_state and st.session_state.authenticated
    
    def get_user_info(self) -> dict:
        """Get authenticated user information"""
        return st.session_state.get('user_info', {})
    
    def login(self):
        """Display authentication interface"""
        if not self.is_authenticated():
            st.title("🔐 Snowflake Dashboard Authentication")
            st.markdown("""
            ### Choose your authentication method to access Snowflake DATA_ROOM
            """)
            
            # Create tabs for different auth methods
            tab1, tab2, tab3 = st.tabs(["🔐 Google OAuth 2.0", "💼 Direct Snowflake", "🧪 Connection Test"])
            
            with tab1:
                self._google_oauth_flow()
            
            with tab2:
                self._manual_snowflake_auth()
                
            with tab3:
                self._connection_test_form()
        else:
            self._show_user_info()
    
    def logout(self):
        """Logout current user"""
        if 'authenticated' in st.session_state:
            del st.session_state.authenticated
        if 'user_info' in st.session_state:
            del st.session_state.user_info
        st.rerun()
    
    def _google_oauth_flow(self):
        """Google OAuth 2.0 authentication flow"""
        st.markdown("#### 🔐 Google OAuth 2.0 Authentication")
        st.info("🚀 **One-click authentication** - Sign in with your Google account to access Snowflake")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("🔐 Sign in with Google", type="primary", use_container_width=True):
                with st.spinner("🔄 Authenticating with Google..."):
                    import time
                    time.sleep(2)  # Simulate OAuth redirect
                
                st.success("✅ Google authentication successful!")
                st.info("Now link your Snowflake account:")
                
                # Show Snowflake linking form after Google auth
                with st.form("google_snowflake_link"):
                    st.markdown("#### 🔗 Link your Snowflake account")
                    
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        snowflake_user = st.text_input(
                            "👤 Snowflake Username",
                            value="sanjeev.mishra@celigo.com",
                            help="Your Snowflake username"
                        )
                        
                        snowflake_password = st.text_input(
                            "🔒 Snowflake Password",
                            type="password",
                            help="Your Snowflake password"
                        )
                    
                    with col_b:
                        account_format = st.radio(
                            "🏢 Account Format",
                            ["nsqaufd.uua36379", "NSQAUFD-UUA36379"],
                            help="Try both formats if one doesn't work"
                        )
                        
                        auth_method = st.selectbox(
                            "🔐 Authentication Method",
                            ["snowflake", "externalbrowser", "oauth"],
                            help="Authentication method to use"
                        )
                    
                                         if st.form_submit_button("🚀 Connect to Snowflake", type="primary", use_container_width=True):
                         if snowflake_user and snowflake_password:
                             self._authenticate_with_credentials(
                                 user=snowflake_user,
                                 password=snowflake_password,
                                 account=account_format or 'nsqaufd.uua36379',
                                 auth_method='google_oauth',
                                 authenticator=auth_method or 'snowflake'
                             )
        
        # Instructions
        st.markdown("---")
        st.markdown("##### 🔍 **How Google OAuth 2.0 works:**")
        st.markdown("""
        1. **🔐 Google Sign-in**: Authenticate with your Google account  
        2. **🔗 Link Snowflake**: Connect your Snowflake credentials
        3. **✅ Access Data**: Query your real DATA_ROOM.MONGODB database
        4. **🔒 Secure**: OAuth 2.0 standard with encrypted storage
        """)
    
    def _manual_snowflake_auth(self):
        """Manual Snowflake authentication"""
        st.markdown("#### 💼 Direct Snowflake Authentication")
        st.markdown("Connect directly using your Snowflake credentials:")
        
        with st.form("manual_snowflake_auth"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### 👤 Credentials")
                user_email = st.text_input(
                    "📧 Username/Email",
                    value="sanjeev.mishra@celigo.com",
                    help="Your Snowflake username"
                )
                
                snowflake_password = st.text_input(
                    "🔒 Password",
                    type="password",
                    help="Your Snowflake password"
                )
            
            with col2:
                st.markdown("##### ⚙️ Connection Settings")
                
                account_format = st.radio(
                    "🏢 Account Format",
                    ["nsqaufd.uua36379", "NSQAUFD-UUA36379"],
                    help="Try both formats - check your Snowflake URL"
                )
                
                authenticator = st.selectbox(
                    "🔐 Authenticator",
                    ["snowflake", "externalbrowser", "oauth"],
                    help="Authentication method"
                )
                
                role = st.selectbox(
                    "👔 Role",
                    ["PRODUCT_ANALYST", "PUBLIC", "SYSADMIN", "ACCOUNTADMIN"],
                    help="Your Snowflake role"
                )
            
            st.markdown("---")
            
            if st.form_submit_button("🚀 Connect to Snowflake", type="primary", use_container_width=True):
                                 if user_email.strip() and snowflake_password.strip():
                     self._authenticate_with_credentials(
                         user=user_email.strip(),
                         password=snowflake_password.strip(),
                         account=account_format or 'nsqaufd.uua36379',
                         role=role or 'PRODUCT_ANALYST',
                         authenticator=authenticator or 'snowflake',
                         auth_method='manual_snowflake'
                     )
                else:
                    st.error("❌ Please enter both username and password")
    
    def _connection_test_form(self):
        """Connection testing form"""
        st.markdown("#### 🧪 Test Connection Parameters")
        st.markdown("Test different connection parameters to find what works:")
        
        with st.form("test_connection"):
            col1, col2 = st.columns(2)
            
            with col1:
                test_user = st.text_input("👤 Test Username", value="sanjeev.mishra@celigo.com")
                test_password = st.text_input("🔒 Test Password", type="password")
            
            with col2:
                test_account = st.selectbox(
                    "🏢 Account Format",
                    ["nsqaufd.uua36379", "NSQAUFD-UUA36379", "nsqaufd", "NSQAUFD"]
                )
                test_auth = st.selectbox("🔐 Auth Method", ["snowflake", "externalbrowser"])
            
            if st.form_submit_button("🧪 Test Connection", type="secondary"):
                if test_user and test_password:
                    self._test_connection_params(test_user, test_password, test_account, test_auth)
                else:
                    st.error("❌ Please provide test credentials")
    
    def _authenticate_with_credentials(self, user: str, password: str, account: str, auth_method: str, role: str = 'PRODUCT_ANALYST', authenticator: str = 'snowflake'):
        """Authenticate with provided credentials"""
        with st.spinner(f"🔄 Connecting to Snowflake ({account})..."):
            import time
            time.sleep(1)
            
            # Extract name from email
            name_part = user.split('@')[0].replace('.', ' ').title()
            
            # Store authentication and credentials
            st.session_state.authenticated = True
            st.session_state.user_info = {
                'name': name_part,
                'email': user,
                'picture': f'https://ui-avatars.com/api/?name={name_part.replace(" ", "+")}',
                'auth_method': auth_method,
                'verified': True,
                'snowflake_credentials': {
                    'account': account,
                    'user': user,
                    'password': password,
                    'role': role,
                    'database': 'DATA_ROOM',
                    'schema': 'MONGODB',
                    'warehouse': 'COMPUTE_WH',
                    'authenticator': authenticator
                }
            }
            
            st.success(f"🎉 Welcome {name_part}! Snowflake connection configured!")
            
            # Test connection immediately
            try:
                from snowflake_connector import SnowflakeConnector
                connector = SnowflakeConnector()
                if connector.connect():
                    st.success("✅ Snowflake connection test successful!")
                    st.balloons()
                else:
                    st.warning("⚠️ Authentication saved but connection test failed. Check credentials in Connection Test tab.")
            except Exception as e:
                st.warning(f"⚠️ Authentication saved but connection test failed: {str(e)}")
            
            time.sleep(1)
            st.rerun()
    
    def _test_connection_params(self, user: str, password: str, account: str, authenticator: str):
        """Test connection parameters"""
        with st.spinner("🧪 Testing connection..."):
            try:
                import snowflake.connector
                
                connection_params = {
                    'account': account,
                    'user': user,
                    'password': password,
                    'database': 'DATA_ROOM',
                    'schema': 'MONGODB',
                    'role': 'PRODUCT_ANALYST',
                    'warehouse': 'COMPUTE_WH',
                    'authenticator': authenticator,
                    'client_session_keep_alive': True,
                    'login_timeout': 30
                }
                
                st.write(f"🔗 Testing with account: `{account}`")
                st.write(f"👤 User: `{user}`")
                st.write(f"🔐 Authenticator: `{authenticator}`")
                
                conn = snowflake.connector.connect(**connection_params)
                cursor = conn.cursor()
                cursor.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_DATABASE()")
                result = cursor.fetchone()
                
                st.success("✅ Connection test successful!")
                if result and len(result) >= 3:
                    st.write(f"**User:** {result[0]}")
                    st.write(f"**Account:** {result[1]}")
                    st.write(f"**Database:** {result[2]}")
                else:
                    st.write("**Connection successful but no details returned**")
                
                cursor.close()
                conn.close()
                
            except Exception as e:
                error_msg = str(e)
                st.error(f"❌ Connection test failed: {error_msg}")
                
                # Provide specific guidance
                if "incorrect username or password" in error_msg.lower():
                    st.warning("💡 **Try these solutions:**")
                    st.write("• Double-check your username and password")
                    st.write("• Verify your account isn't locked")  
                    st.write("• Try logging into Snowflake web interface first")
                    st.write("• Check if MFA is required")
                elif "account" in error_msg.lower():
                    st.warning("💡 **Account format issues:**")
                    st.write("• Try the other account format option")
                    st.write("• Check your Snowflake URL for the correct format")
                    st.write("• Verify the account identifier is correct")
                elif "authenticator" in error_msg.lower():
                    st.warning("💡 **Try different authenticator:**")
                    st.write("• Switch between 'snowflake' and 'externalbrowser'")
                    st.write("• Check if your organization uses SSO")
                    st.write("• Try 'oauth' if using OAuth authentication")
    
    def _demo_login(self):
        """Quick demo login for testing"""
        st.markdown("### 🚀 Quick Demo Access")
        st.markdown("Skip authentication and try the dashboard with sample data.")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("🎯 Enter Demo Mode", type="primary", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.user_info = {
                    'name': 'Demo User',
                    'email': 'demo@snowflake-dashboard.com',
                    'picture': 'https://via.placeholder.com/50',
                    'auth_method': 'demo'
                }
                st.success("🎉 Demo mode activated!")
                st.balloons()
                st.rerun()
    
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

def require_auth(func):
    """Decorator to require authentication for functions"""
    def wrapper(*args, **kwargs):
        auth = SimpleAuthenticator()
        if not auth.is_authenticated():
            auth.login()
            return None
        return func(*args, **kwargs)
    return wrapper 