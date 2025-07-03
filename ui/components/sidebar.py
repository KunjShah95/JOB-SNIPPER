"""Sidebar component for JobSniper AI

Handles navigation, settings, and configuration in the sidebar.
"""

import streamlit as st
from typing import Dict, Any, Optional
from utils.config import validate_config, load_config
from utils.validators import validate_api_keys, EmailValidator
from utils.error_handler import show_warning, show_success


def create_sidebar() -> Dict[str, Any]:
    """Create and manage the application sidebar"""
    
    with st.sidebar:
        # App header
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <h1>🎯 JobSniper AI</h1>
            <p style='color: #666; font-size: 0.9rem;'>Professional Resume & Career Intelligence</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Navigation
        navigation = get_navigation_choice()
        
        st.divider()
        
        # Configuration status
        show_config_status()
        
        st.divider()
        
        # Quick settings
        show_quick_settings()
        
        return {
            'navigation': navigation,
            'config_valid': st.session_state.get('config_valid', False)
        }


def get_navigation_choice() -> str:
    """Get user's navigation choice"""
    
    st.markdown("### 📋 Navigation")
    
    nav_options = {
        "🏠 Home": "home",
        "📄 Resume Analysis": "resume_analysis", 
        "🎯 Job Matching": "job_matching",
        "📚 Skill Recommendations": "skill_recommendations",
        "🤖 Auto Apply": "auto_apply",
        "👔 HR Dashboard": "hr_dashboard",
        "📊 Analytics": "analytics",
        "⚙️ Settings": "settings"
    }
    
    choice = st.radio(
        "Choose a section:",
        options=list(nav_options.keys()),
        key="navigation_choice",
        label_visibility="collapsed"
    )
    
    return nav_options[choice]


def show_config_status():
    """Show configuration status in sidebar"""
    
    st.markdown("### ⚙️ System Status")
    
    # Load current config
    try:
        config = load_config()
        validation = validate_config(config)
        
        # AI Providers
        if validation['ai_providers']:
            st.success(f"🤖 AI: {', '.join(validation['ai_providers']).title()}")
        else:
            st.error("🤖 AI: Not configured")
        
        # Email
        if 'email_reports' in validation['features_enabled']:
            st.success("📧 Email: Configured")
        else:
            st.warning("📧 Email: Not configured")
        
        # Features
        feature_count = len(validation['features_enabled'])
        st.info(f"🔧 Features: {feature_count} enabled")
        
        # Store validation in session state
        st.session_state['config_valid'] = validation['valid']
        st.session_state['config_validation'] = validation
        
    except Exception as e:
        st.error("❌ Config: Error loading")
        st.session_state['config_valid'] = False


def show_quick_settings():
    """Show quick settings in sidebar"""
    
    st.markdown("### 🔧 Quick Settings")
    
    # Demo mode toggle
    demo_mode = st.checkbox(
        "Demo Mode",
        value=st.session_state.get('demo_mode', False),
        help="Use demo data when AI providers are unavailable"
    )
    st.session_state['demo_mode'] = demo_mode
    
    # Debug mode toggle
    debug_mode = st.checkbox(
        "Debug Mode", 
        value=st.session_state.get('debug_mode', False),
        help="Show detailed error information"
    )
    st.session_state['debug_mode'] = debug_mode
    
    # Auto-save toggle
    auto_save = st.checkbox(
        "Auto-save Results",
        value=st.session_state.get('auto_save', True),
        help="Automatically save analysis results to database"
    )
    st.session_state['auto_save'] = auto_save
    
    # Theme selection
    theme = st.selectbox(
        "Theme",
        options=["Auto", "Light", "Dark"],
        index=0,
        help="Choose UI theme preference"
    )
    st.session_state['theme'] = theme


def show_api_config_form():
    """Show API configuration form in sidebar"""
    
    st.markdown("### 🔑 API Configuration")
    
    with st.form("api_config_form"):
        st.markdown("**AI Providers**")
        
        gemini_key = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="AIza...",
            help="Get your key from Google AI Studio"
        )
        
        mistral_key = st.text_input(
            "Mistral API Key", 
            type="password",
            placeholder="Your Mistral key",
            help="Get your key from Mistral AI Console"
        )
        
        st.markdown("**Optional Services**")
        
        firecrawl_key = st.text_input(
            "Firecrawl API Key",
            type="password", 
            placeholder="Your Firecrawl key",
            help="For web scraping features"
        )
        
        submitted = st.form_submit_button("💾 Save Configuration")
        
        if submitted:
            # Validate keys
            validation = validate_api_keys(gemini_key, mistral_key)
            
            if validation['gemini_valid'] or validation['mistral_valid']:
                # Save to session state (in production, save to .env)
                st.session_state['api_keys'] = {
                    'gemini': gemini_key if validation['gemini_valid'] else None,
                    'mistral': mistral_key if validation['mistral_valid'] else None,
                    'firecrawl': firecrawl_key if firecrawl_key else None
                }
                show_success("API keys saved successfully!")
                st.rerun()
            else:
                show_warning("Please provide at least one valid API key")


def show_email_config_form():
    """Show email configuration form in sidebar"""
    
    st.markdown("### 📧 Email Configuration")
    
    with st.form("email_config_form"):
        email = st.text_input(
            "Email Address",
            placeholder="your.email@gmail.com",
            help="Gmail address for sending reports"
        )
        
        password = st.text_input(
            "App Password",
            type="password",
            placeholder="Your Gmail app password",
            help="Generate an app password in Gmail settings"
        )
        
        submitted = st.form_submit_button("💾 Save Email Config")
        
        if submitted:
            validation = EmailValidator.validate_email_config(email, password)
            
            if validation['valid']:
                # Save to session state (in production, save to .env)
                st.session_state['email_config'] = {
                    'email': email,
                    'password': password
                }
                show_success("Email configuration saved!")
                st.rerun()
            else:
                for error in validation['errors']:
                    show_warning(error)


def show_feature_toggles():
    """Show feature toggle controls"""
    
    st.markdown("### 🎛️ Feature Controls")
    
    features = {
        'resume_builder': 'Resume Builder',
        'company_research': 'Company Research', 
        'advanced_interview_prep': 'Interview Prep',
        'salary_insights': 'Salary Insights',
        'web_scraping': 'Web Scraping',
        'auto_apply': 'Auto Apply',
        'analytics': 'Analytics Dashboard'
    }
    
    for feature_key, feature_name in features.items():
        enabled = st.checkbox(
            feature_name,
            value=st.session_state.get(f'feature_{feature_key}', True),
            key=f'feature_{feature_key}'
        )
        st.session_state[f'feature_{feature_key}'] = enabled


def get_sidebar_state() -> Dict[str, Any]:
    """Get current sidebar state"""
    return {
        'navigation': st.session_state.get('navigation_choice', 'home'),
        'demo_mode': st.session_state.get('demo_mode', False),
        'debug_mode': st.session_state.get('debug_mode', False),
        'auto_save': st.session_state.get('auto_save', True),
        'theme': st.session_state.get('theme', 'Auto'),
        'config_valid': st.session_state.get('config_valid', False)
    }