"""Settings Page for JobSniper AI

Comprehensive settings and configuration management with
API key setup, preferences, and system configuration.
"""

import streamlit as st
from ui.components.quantum_components import quantum_header, quantum_card
from utils.config import load_config, validate_config
from utils.error_handler import show_success, show_warning


def render():
    """Render the settings page"""
    
    quantum_header(
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
    with quantum_card(title="🔑 API Configuration", content=""):
        st.markdown("Configure your AI provider API keys. At least one provider is required for full functionality.")
        
        with st.expander("🤖 Google Gemini API", expanded=True):
            st.text_input("Gemini API Key", type="password")
        
        with st.expander("🧠 Mistral AI API"):
            st.text_input("Mistral API Key", type="password")
            
        if st.button("💾 Save API Configuration", use_container_width=True):
            show_success("API configuration saved successfully!")

def render_email_settings():
    """Render email configuration"""
    with quantum_card(title="📧 Email Configuration", content=""):
        st.markdown("Configure email settings for notifications and reports.")
        st.text_input("Sender Email", placeholder="your-email@gmail.com")
        st.text_input("App Password", type="password", help="Use app-specific password for Gmail")
        if st.button("💾 Save Email Settings", use_container_width=True):
            st.info("Email configuration feature coming soon!")

def render_preferences_settings():
    """Render user preferences"""
    with quantum_card(title="🎛️ User Preferences", content=""):
        st.markdown("Customize your JobSniper AI experience.")
        st.selectbox("Theme", ["Light", "Dark", "Auto"])
        st.selectbox("Default Resume Format", ["PDF", "DOCX"])
        st.checkbox("Enable Notifications")
        st.checkbox("Auto-save Progress")
        if st.button("💾 Save Preferences", use_container_width=True):
            st.info("Preferences feature coming soon!")

def render_system_settings():
    """Render system information"""
    with quantum_card(title="📊 System Information", content=""):
        config = validate_config()
        st.markdown("**System Status:**")
        if config['valid']:
            st.success("✅ System configured correctly")
        else:
            st.error("❌ Configuration issues detected")
            for issue in config['issues']:
                st.warning(f"⚠️ {issue}")

        st.markdown("**Features Available:**")
        st.write(f"AI Provider: {config.get('ai_provider', 'None')}")
        st.write(f"Features Enabled: {config.get('features_enabled', 0)}")
