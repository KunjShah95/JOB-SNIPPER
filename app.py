#!/usr/bin/env python3
"""
JobSniper AI - Main Application Launcher
========================================

This is the main entry point for the JobSniper AI application.
It automatically detects available components and launches the appropriate UI.
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Page configuration
st.set_page_config(
    page_title="JobSniper AI - Career Intelligence Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

def check_advanced_agents():
    """Check if advanced agents are available"""
    try:
        from agents.advanced_controller_agent import AdvancedControllerAgent
        return True
    except ImportError:
        return False

def check_legacy_agents():
    """Check if legacy agents are available"""
    try:
        from agents.controller_agent import ControllerAgent
        return True
    except ImportError:
        return False

def main():
    """Main application launcher"""
    
    # Header
    st.markdown(
        """
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white; margin-bottom: 2rem;">
            <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">🚀 JobSniper AI</h1>
            <h3 style="font-size: 1.5rem; margin-bottom: 1rem;">Career Intelligence Platform</h3>
            <p style="font-size: 1.1rem; opacity: 0.9;">Powered by Advanced AI • Multi-Agent Analysis • Real-time Insights</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Check system status
    advanced_available = check_advanced_agents()
    legacy_available = check_legacy_agents()
    
    # Display system status
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if advanced_available:
            st.success("✅ Advanced Agents Available")
        else:
            st.warning("⚠️ Advanced Agents Not Found")
    
    with col2:
        if legacy_available:
            st.info("ℹ️ Legacy Agents Available")
        else:
            st.error("❌ Legacy Agents Not Found")
    
    with col3:
        if advanced_available or legacy_available:
            st.success("🚀 System Ready")
        else:
            st.error("💥 System Error")
    
    # Launch options
    st.markdown("## 🎯 Launch Options")
    
    if advanced_available:
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 1.5rem; border-radius: 12px; margin: 1rem 0;">
                <h4 style="color: #2c3e50; margin-bottom: 1rem;">🚀 Advanced UI (Recommended)</h4>
                <p style="color: #34495e; margin-bottom: 1rem;">Experience the full power of JobSniper AI with our advanced agent system featuring sophisticated prompt engineering, multi-agent orchestration, and comprehensive analysis.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if st.button("🚀 Launch Advanced UI", type="primary", use_container_width=True):
            st.markdown("### 🔄 Redirecting to Advanced UI...")
            st.markdown(
                """
                <script>
                window.open('/ui/advanced_app.py', '_self');
                </script>
                """,
                unsafe_allow_html=True
            )
            st.info("If automatic redirect doesn't work, please navigate to: `/ui/advanced_app.py`")
    
    if legacy_available:
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); padding: 1.5rem; border-radius: 12px; margin: 1rem 0;">
                <h4 style="color: #2c3e50; margin-bottom: 1rem;">📱 Legacy UI</h4>
                <p style="color: #34495e; margin-bottom: 1rem;">Use the original JobSniper interface with basic agent functionality. Suitable for systems without advanced agent support.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if st.button("📱 Launch Legacy UI", use_container_width=True):
            st.markdown("### 🔄 Redirecting to Legacy UI...")
            st.info("If automatic redirect doesn't work, please navigate to: `/ui/app.py`")
    
    # Manual navigation
    st.markdown("## 🧭 Manual Navigation")
    
    st.markdown(
        """
        If the automatic launch doesn't work, you can manually navigate to:
        
        **Advanced UI:** `streamlit run ui/advanced_app.py`
        
        **Legacy UI:** `streamlit run ui/app.py`
        """
    )
    
    # System information
    if not (advanced_available or legacy_available):
        st.markdown("## ⚠️ System Setup Required")
        
        st.error(
            """
            **No agents found!** Please ensure you have properly installed the JobSniper AI system.
            
            **Quick Setup:**
            1. Install dependencies: `pip install -r requirements.txt`
            2. Configure API keys in `.env` file
            3. Restart the application
            
            **For Advanced Agents:**
            - Ensure you're on the `advanced-agents-rebuild` branch
            - Check that all advanced agent files are present in the `agents/` directory
            
            **For Legacy Support:**
            - Ensure legacy agent files are available
            - Check import paths and dependencies
            """
        )
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #666; padding: 1rem;">
            <p><strong>JobSniper AI</strong> - Transforming Career Intelligence Through Advanced AI</p>
            <p>Built with ❤️ by the JobSniper Team</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()