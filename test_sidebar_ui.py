#!/usr/bin/env python3
"""
Test script to verify sidebar UI visibility fix
Run with: streamlit run test_sidebar_ui.py
"""

import streamlit as st
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the theme
from ui.styles.modern_theme import apply_modern_theme

def main():
    """Test the sidebar UI with the fixed styling"""
    
    # Apply the modern theme with sidebar fixes
    apply_modern_theme()
    
    # Set page config
    st.set_page_config(
        page_title="Sidebar UI Test",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Main content
    st.title("🎯 Sidebar UI Test")
    st.write("This is a test to verify that the sidebar text is now visible with the dark background.")
    
    # Sidebar content
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <h1>🎯 JobSniper AI</h1>
            <p style='color: white; font-size: 0.9rem;'>Professional Resume & Career Intelligence</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        st.markdown("### 📋 Navigation")
        
        nav_options = [
            "🏠 Home",
            "📄 Resume Analysis", 
            "🎯 Job Matching",
            "📚 Skill Recommendations",
            "🤖 Auto Apply",
            "👔 HR Dashboard",
            "📊 Analytics",
            "⚙️ Settings"
        ]
        
        choice = st.radio(
            "Choose a section:",
            options=nav_options,
            key="navigation_choice",
            label_visibility="collapsed"
        )
        
        st.divider()
        
        st.markdown("### ⚙️ System Status")
        
        st.success("🤖 AI: Gemini, Mistral")
        st.warning("📧 Email: Not configured")
        st.info("🔧 Features: 5 enabled")
        st.error("❌ Config: Missing API keys")
        
        st.divider()
        
        st.markdown("### 🔧 Quick Settings")
        
        demo_mode = st.checkbox("Demo Mode", value=False)
        debug_mode = st.checkbox("Debug Mode", value=False)
        auto_save = st.checkbox("Auto-save Results", value=True)
        
        theme = st.selectbox(
            "Theme",
            options=["Auto", "Light", "Dark"],
            index=0
        )
        
        st.divider()
        
        if st.button("💾 Save Settings"):
            st.success("Settings saved!")
    
    # Show the selected navigation
    st.write(f"**Selected:** {choice}")
    
    # Test different message types in main area
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("✅ This is a success message")
        st.info("ℹ️ This is an info message")
    
    with col2:
        st.warning("⚠️ This is a warning message")
        st.error("❌ This is an error message")
    
    st.markdown("""
    ## Sidebar Visibility Test Results
    
    **Expected behavior:**
    - ✅ Sidebar should have a dark blue gradient background
    - ✅ All text in sidebar should be white and clearly visible
    - ✅ Navigation radio buttons should be white text
    - ✅ Checkboxes and selectbox labels should be white
    - ✅ Status messages should have colored backgrounds with light text
    - ✅ Dividers should be subtle white lines
    
    **If you can see all the sidebar text clearly, the fix is working! 🎉**
    """)

if __name__ == "__main__":
    main()