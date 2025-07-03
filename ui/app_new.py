"""Modern JobSniper AI Application

Completely refactored, modular application with modern UI/UX,
replacing the monolithic 4,276-line app.py with clean,
maintainable components.
"""

import streamlit as st
import sys
import os
from datetime import datetime
import logging

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import UI components
from ui.styles.modern_theme import apply_modern_theme
from ui.components.sidebar import create_sidebar
from ui.pages import (
    render_home_page,
    render_resume_analysis_page,
    render_job_matching_page,
    render_skill_recommendations_page,
    render_hr_dashboard_page,
    render_settings_page
)

# Import utilities
from utils.config import load_config, validate_config
from utils.error_handler import global_error_handler, show_warning
from utils.sqlite_logger import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class JobSniperApp:
    """Main application class for JobSniper AI"""
    
    def __init__(self):
        self.setup_page_config()
        self.initialize_session_state()
        self.setup_database()
        
    def setup_page_config(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="JobSniper AI - Professional Resume & Career Intelligence",
            page_icon="🎯",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'https://github.com/KunjShah95/JOB-SNIPPER',
                'Report a bug': 'https://github.com/KunjShah95/JOB-SNIPPER/issues',
                'About': """
                # JobSniper AI
                
                Professional Resume & Career Intelligence Platform
                
                **Version:** 2.0.0  
                **Built with:** Streamlit, Python, AI
                
                Transform your career with AI-powered insights!
                """
            }
        )
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if "app_initialized" not in st.session_state:
            st.session_state.app_initialized = True
            st.session_state.user_session = {
                "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
                "start_time": datetime.now(),
                "page_views": 0
            }
            
        # Initialize page-specific state
        if "current_page" not in st.session_state:
            st.session_state.current_page = "home"
            
        # Track page views
        st.session_state.user_session["page_views"] += 1
    
    def setup_database(self):
        """Initialize database if needed"""
        try:
            init_db()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            show_warning("Database initialization failed. Some features may not work properly.")
    
    def validate_configuration(self):
        """Validate application configuration"""
        try:
            config = load_config()
            validation = validate_config(config)
            
            if not validation['valid'] and not st.session_state.get('config_warning_shown', False):
                st.session_state.config_warning_shown = True
                
                with st.sidebar:
                    st.warning("⚠️ Configuration Issues")
                    with st.expander("View Details"):
                        for issue in validation['issues']:
                            st.write(f"• {issue}")
                        st.info("💡 Go to Settings to configure missing services")
            
            return validation
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            return {'valid': False, 'issues': ['Configuration error'], 'ai_providers': [], 'features_enabled': []}
    
    def render_sidebar(self):
        """Render the application sidebar"""
        try:
            sidebar_state = create_sidebar()
            return sidebar_state['navigation']
        except Exception as e:
            logger.error(f"Sidebar rendering failed: {e}")
            st.sidebar.error("❌ Sidebar error")
            return "home"
    
    def render_main_content(self, current_page: str):
        """Render the main content area based on current page"""
        
        # Apply modern theme
        apply_modern_theme()
        
        # Page routing
        try:
            if current_page == "home":
                render_home_page()
                
            elif current_page == "resume_analysis":
                render_resume_analysis_page()
                
            elif current_page == "job_matching":
                render_job_matching_page()
                
            elif current_page == "skill_recommendations":
                render_skill_recommendations_page()
                
            elif current_page == "auto_apply":
                self.render_auto_apply_page()
                
            elif current_page == "hr_dashboard":
                render_hr_dashboard_page()
                
            elif current_page == "analytics":
                self.render_analytics_page()
                
            elif current_page == "settings":
                render_settings_page()
                
            else:
                st.error(f"❌ Unknown page: {current_page}")
                render_home_page()
                
        except Exception as e:
            error_result = global_error_handler.log_error(
                error=e,
                context=f"Rendering page: {current_page}",
                show_user=True
            )
            
            # Fallback to home page
            if current_page != "home":
                st.info("🏠 Redirecting to home page...")
                st.session_state.current_page = "home"
                st.rerun()
    
    def render_auto_apply_page(self):
        """Render auto apply page (placeholder)"""
        from ui.styles.modern_theme import create_header
        
        create_header(
            title="Auto Apply",
            subtitle="Automated job application system (Coming Soon)",
            icon="🤖"
        )
        
        st.info("🚧 This feature is under development. Stay tuned for automated job applications!")
    
    def render_analytics_page(self):
        """Render analytics page (placeholder)"""
        from ui.styles.modern_theme import create_header
        
        create_header(
            title="Analytics",
            subtitle="Career progression insights and performance metrics",
            icon="📊"
        )
        
        st.info("📈 Analytics dashboard coming soon with detailed career insights!")
    
    def render_footer(self):
        """Render application footer"""
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🎯 JobSniper AI**")
            st.markdown("Professional Resume & Career Intelligence")
        
        with col2:
            st.markdown("**📊 Session Stats**")
            session = st.session_state.user_session
            st.markdown(f"Page Views: {session['page_views']}")
            st.markdown(f"Session: {session['session_id']}")
        
        with col3:
            st.markdown("**🔗 Quick Links**")
            st.markdown("[GitHub](https://github.com/KunjShah95/JOB-SNIPPER) | [Issues](https://github.com/KunjShah95/JOB-SNIPPER/issues)")
    
    def run(self):
        """Main application entry point"""
        try:
            # Validate configuration
            self.validate_configuration()
            
            # Render sidebar and get navigation choice
            current_page = self.render_sidebar()
            
            # Update current page in session state
            st.session_state.current_page = current_page
            
            # Render main content
            self.render_main_content(current_page)
            
            # Render footer
            self.render_footer()
            
        except Exception as e:
            # Global error handling
            global_error_handler.log_error(
                error=e,
                context="Main application",
                show_user=True
            )
            
            # Show fallback UI
            st.error("❌ Application error occurred")
            st.info("🔄 Please refresh the page or contact support")


def main():
    """Application entry point"""
    try:
        # Create and run the application
        app = JobSniperApp()
        app.run()
        
    except Exception as e:
        # Last resort error handling
        st.error("❌ Critical application error")
        st.exception(e)
        
        # Show basic recovery options
        st.markdown("### 🔧 Recovery Options")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Refresh Page"):
                st.rerun()
        
        with col2:
            if st.button("🏠 Go to Home"):
                st.session_state.clear()
                st.rerun()


if __name__ == "__main__":
    main()