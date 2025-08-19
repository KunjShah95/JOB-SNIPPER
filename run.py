#!/usr/bin/env python3
"""
JobSniper AI - Main Entry Point
Run this file to start the application
"""

import sys
import logging
import streamlit as st
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_environment():
    """Check if environment is properly configured"""
    from utils.config import validate_config
    
    config_status = validate_config()
    
    if not config_status["valid"]:
        st.error("⚠️ Configuration Issues Found:")
        for issue in config_status["issues"]:
            st.error(f"• {issue}")
        
        st.info("📝 Please check your .env file and ensure all required variables are set.")
        st.info("📋 See .env.example for reference.")
        return False
    
    st.success(f"✅ Configuration valid! Using {config_status['ai_provider']} as AI provider")
    st.info(f"🚀 {config_status['features_enabled']} features enabled")
    return True

def main():
    """Main application entry point"""
    try:
        # Check environment first
        if not check_environment():
            st.stop()
        
        # Import and run the main app
        from ui.app import main as app_main
        app_main()
        
    except ImportError as e:
        st.error(f"❌ Import Error: {e}")
        st.error("Please ensure all dependencies are installed: `pip install -r requirements.txt`")
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"❌ Application Error: {e}")
        st.error("Please check the logs for more details.")

if __name__ == "__main__":
    main()