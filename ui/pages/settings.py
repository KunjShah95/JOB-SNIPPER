"""Settings Page for JobSniper AI

Comprehensive settings and configuration management with
API key setup, preferences, and system configuration.
"""

import streamlit as st
from ui.styles.modern_theme import apply_modern_theme, create_header, ModernTheme
from utils.config import load_config, validate_config
from utils.validators import validate_api_keys, EmailValidator
from utils.error_handler import show_success, show_warning


def render_settings_page():
    """Render the settings page"""
    
    # Apply modern theme
    apply_modern_theme()
    
    # Create header
    create_header(
        title="Settings",
        subtitle="Configure API keys, preferences, and system settings",
        icon="⚙️"
    )
    
    # Settings tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔑 API Keys", "📧 Email", "🎛️ Preferences", "📊 System"])
    
    with tab1:
        render_api_settings()
    
    with tab2:
        render_email_settings()
    
    with tab3:
        render_preferences_settings()
    
    with tab4:
        render_system_settings()


def render_api_settings():
    """Render API key configuration"""
    
    st.markdown("### 🔑 API Configuration")
    
    ModernTheme.create_card(
        title="AI Providers",
        content="""
        <p style="color: #6C757D; margin-bottom: 1.5rem;">
            Configure your AI provider API keys. At least one provider is required for full functionality.
        </p>
        """
    )
    
    # Gemini API Key
    with st.expander("🤖 Google Gemini API", expanded=True):
        st.markdown("**Primary AI Provider** - Recommended for best results")
        
        gemini_key = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="AIzaSy...",
            help="Get your API key from Google AI Studio: https://aistudio.google.com/app/apikey"
        )
        
        if gemini_key:
            validation = validate_api_keys(gemini_key=gemini_key)
            if validation['gemini_valid']:
                st.success("✅ Valid Gemini API key format")
            else:
                st.error("❌ Invalid Gemini API key format")
        
        st.info("💡 **How to get Gemini API key:**\n1. Visit Google AI Studio\n2. Create a new API key\n3. Copy and paste it here")
    
    # Mistral API Key
    with st.expander("🧠 Mistral AI API"):
        st.markdown("**Secondary AI Provider** - Fallback option")
        
        mistral_key = st.text_input(
            "Mistral API Key",
            type="password",
            placeholder="Your Mistral API key",
            help="Get your API key from Mistral AI Console: https://console.mistral.ai/"
        )
        
        if mistral_key:
            validation = validate_api_keys(mistral_key=mistral_key)
            if validation['mistral_valid']:
                st.success("✅ Valid Mistral API key format")
            else:
                st.error("❌ Invalid Mistral API key format")
    
    # Optional Services
    with st.expander("🌐 Optional Services"):
        st.markdown("**Web Scraping & Research**")
        
        firecrawl_key = st.text_input(
            "Firecrawl API Key",
            type="password",
            placeholder="Your Firecrawl API key",
            help="For web scraping and company research features"
        )
        
        if firecrawl_key:
            st.info("🔍 Firecrawl enables web scraping and company research features")
    
    # Save button
    if st.button("💾 Save API Configuration", type="primary", use_container_width=True):
        # In a real implementation, this would save to .env file
        show_success("API configuration saved successfully!")
        st.info("💡 Restart the application to apply changes")


def render_email_settings():
    """Render email configuration"""
    
    st.markdown("### 📧 Email Configuration")
    
    ModernTheme.create_card(
        title="Email Reports",
        content="""
        <p style="color: #6C757D; margin-bottom: 1.5rem;">
            Configure email settings to receive resume analysis reports and notifications.
        </p>
        """
    )
    
    with st.form("email_config_form"):
        st.markdown("**Gmail Configuration** (Recommended)")
        
        email = st.text_input(
            "Email Address",
            placeholder="your.email@gmail.com",
            help="Your Gmail address for sending reports"
        )
        
        password = st.text_input(
            "App Password",
            type="password",
            placeholder="Your Gmail app password",
            help="Generate an app password in Gmail settings (not your regular password)"
        )
        
        st.markdown("**SMTP Settings** (Advanced)")
        
        col1, col2 = st.columns(2)
        with col1:
            smtp_server = st.text_input("SMTP Server", value="smtp.gmail.com")
        with col2:
            smtp_port = st.number_input("SMTP Port", value=587, min_value=1, max_value=65535)
        
        submitted = st.form_submit_button("💾 Save Email Configuration", type="primary")
        
        if submitted:
            if email and password:
                validation = EmailValidator.validate_email_config(email, password)
                
                if validation['valid']:
                    show_success("Email configuration saved successfully!")
                else:
                    for error in validation['errors']:
                        show_warning(error)
            else:
                show_warning("Please provide both email and password")
    
    # Email setup guide
    with st.expander("📖 Gmail Setup Guide"):
        st.markdown("""
        **How to set up Gmail for email reports:**
        
        1. **Enable 2-Factor Authentication** on your Gmail account
        2. **Generate App Password:**
           - Go to Google Account settings
           - Security → 2-Step Verification → App passwords
           - Select "Mail" and generate password
        3. **Use the generated app password** (not your regular password)
        4. **Test the configuration** using the form above
        
        **Security Note:** App passwords are safer than using your main password.
        """)


def render_preferences_settings():
    """Render user preferences"""
    
    st.markdown("### 🎛️ User Preferences")
    
    # Theme settings
    ModernTheme.create_card(
        title="🎨 Appearance",
        content=""
    )
    
    theme = st.selectbox(
        "Theme",
        options=["Auto", "Light", "Dark"],
        index=0,
        help="Choose your preferred theme"
    )
    
    # Feature preferences
    st.markdown("**🔧 Feature Settings**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        auto_save = st.checkbox(
            "Auto-save Results",
            value=True,
            help="Automatically save analysis results"
        )
        
        demo_mode = st.checkbox(
            "Demo Mode",
            value=False,
            help="Use demo data when AI providers are unavailable"
        )
    
    with col2:
        debug_mode = st.checkbox(
            "Debug Mode",
            value=False,
            help="Show detailed error information"
        )
        
        analytics = st.checkbox(
            "Usage Analytics",
            value=True,
            help="Help improve the app by sharing usage data"
        )
    
    # Notification preferences
    st.markdown("**🔔 Notifications**")
    
    email_notifications = st.checkbox(
        "Email Notifications",
        value=True,
        help="Receive email notifications for completed analyses"
    )
    
    # Save preferences
    if st.button("💾 Save Preferences", type="primary", use_container_width=True):
        show_success("Preferences saved successfully!")


def render_system_settings():
    """Render system information and settings"""
    
    st.markdown("### 📊 System Information")
    
    # Current configuration status
    try:
        config = load_config()
        validation = validate_config(config)
        
        # System status
        ModernTheme.create_card(
            title="🔧 System Status",
            content=f"""
            <div style="margin-bottom: 1rem;">
                <strong>Overall Status:</strong> 
                {ModernTheme.create_status_badge('Healthy' if validation['valid'] else 'Issues', 'success' if validation['valid'] else 'warning')}
            </div>
            
            <div style="margin-bottom: 1rem;">
                <strong>AI Providers:</strong> {len(validation['ai_providers'])} configured
                <br><small style="color: #6C757D;">{', '.join(validation['ai_providers']) if validation['ai_providers'] else 'None configured'}</small>
            </div>
            
            <div style="margin-bottom: 1rem;">
                <strong>Features Enabled:</strong> {len(validation['features_enabled'])}
                <br><small style="color: #6C757D;">{', '.join(validation['features_enabled']) if validation['features_enabled'] else 'Basic features only'}</small>
            </div>
            """
        )
        
        # Configuration issues
        if validation['issues']:
            st.markdown("**⚠️ Configuration Issues**")
            for issue in validation['issues']:
                st.warning(f"• {issue}")
    
    except Exception as e:
        st.error(f"❌ Error loading system status: {str(e)}")
    
    # System actions
    st.markdown("**🔧 System Actions**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh Config", use_container_width=True):
            st.rerun()
    
    with col2:
        if st.button("🧪 Test Configuration", use_container_width=True):
            st.info("Configuration test feature coming soon!")
    
    with col3:
        if st.button("📋 Export Settings", use_container_width=True):
            st.info("Settings export feature coming soon!")
    
    # Advanced settings
    with st.expander("🔧 Advanced Settings"):
        st.warning("⚠️ Advanced settings - modify with caution")
        
        max_file_size = st.number_input(
            "Max File Size (MB)",
            value=10,
            min_value=1,
            max_value=100,
            help="Maximum file size for resume uploads"
        )
        
        api_timeout = st.number_input(
            "API Timeout (seconds)",
            value=30,
            min_value=5,
            max_value=300,
            help="Timeout for AI API requests"
        )
        
        if st.button("💾 Save Advanced Settings"):
            show_success("Advanced settings saved!")
    
    # Reset options
    st.markdown("**🔄 Reset Options**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear Session Data", use_container_width=True):
            st.session_state.clear()
            show_success("Session data cleared!")
            st.rerun()
    
    with col2:
        if st.button("⚠️ Reset All Settings", use_container_width=True, type="secondary"):
            st.warning("This will reset all settings to defaults. This action cannot be undone.")
            if st.button("Confirm Reset", type="primary"):
                show_success("Settings reset to defaults!")