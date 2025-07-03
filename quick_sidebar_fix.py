#!/usr/bin/env python3
"""
Quick Sidebar Visibility Fix for Streamlit Apps

This is a standalone fix that can be imported into any Streamlit app
to resolve white text on white background issues in the sidebar.

Usage:
    from quick_sidebar_fix import apply_sidebar_fix
    apply_sidebar_fix()
"""

import streamlit as st

def apply_sidebar_fix():
    """Apply CSS fix for sidebar text visibility"""
    
    st.markdown("""
    <style>
    /* Sidebar Background - Dark Blue Gradient */
    .css-1d391kg, .css-1lcbmhc, .css-17eq0hr, 
    .st-emotion-cache-16txtl3, .st-emotion-cache-1y4p8pa,
    section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%) !important;
        border-right: 1px solid #e5e7eb !important;
    }
    
    /* All Sidebar Text - White */
    .css-1d391kg *, .css-1lcbmhc *, .css-17eq0hr *,
    .st-emotion-cache-16txtl3 *, .st-emotion-cache-1y4p8pa *,
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Sidebar Headers */
    .css-1d391kg h1, .css-1lcbmhc h1, .css-17eq0hr h1,
    .st-emotion-cache-16txtl3 h1, .st-emotion-cache-1y4p8pa h1,
    section[data-testid="stSidebar"] h1,
    .css-1d391kg h2, .css-1lcbmhc h2, .css-17eq0hr h2,
    .st-emotion-cache-16txtl3 h2, .st-emotion-cache-1y4p8pa h2,
    section[data-testid="stSidebar"] h2,
    .css-1d391kg h3, .css-1lcbmhc h3, .css-17eq0hr h3,
    .st-emotion-cache-16txtl3 h3, .st-emotion-cache-1y4p8pa h3,
    section[data-testid="stSidebar"] h3 {
        color: white !important;
    }
    
    /* Sidebar Form Labels */
    .css-1d391kg label, .css-1lcbmhc label, .css-17eq0hr label,
    .st-emotion-cache-16txtl3 label, .st-emotion-cache-1y4p8pa label,
    section[data-testid="stSidebar"] label {
        color: white !important;
    }
    
    /* Sidebar Radio Button Labels */
    .css-1d391kg .stRadio label, .css-1lcbmhc .stRadio label, .css-17eq0hr .stRadio label,
    .st-emotion-cache-16txtl3 .stRadio label, .st-emotion-cache-1y4p8pa .stRadio label,
    section[data-testid="stSidebar"] .stRadio label {
        color: white !important;
    }
    
    /* Sidebar Checkbox Labels */
    .css-1d391kg .stCheckbox label, .css-1lcbmhc .stCheckbox label, .css-17eq0hr .stCheckbox label,
    .st-emotion-cache-16txtl3 .stCheckbox label, .st-emotion-cache-1y4p8pa .stCheckbox label,
    section[data-testid="stSidebar"] .stCheckbox label {
        color: white !important;
    }
    
    /* Sidebar Selectbox Labels */
    .css-1d391kg .stSelectbox label, .css-1lcbmhc .stSelectbox label, .css-17eq0hr .stSelectbox label,
    .st-emotion-cache-16txtl3 .stSelectbox label, .st-emotion-cache-1y4p8pa .stSelectbox label,
    section[data-testid="stSidebar"] .stSelectbox label {
        color: white !important;
    }
    
    /* Sidebar Text Input Labels */
    .css-1d391kg .stTextInput label, .css-1lcbmhc .stTextInput label, .css-17eq0hr .stTextInput label,
    .st-emotion-cache-16txtl3 .stTextInput label, .st-emotion-cache-1y4p8pa .stTextInput label,
    section[data-testid="stSidebar"] .stTextInput label {
        color: white !important;
    }
    
    /* Sidebar Dividers */
    .css-1d391kg hr, .css-1lcbmhc hr, .css-17eq0hr hr,
    .st-emotion-cache-16txtl3 hr, .st-emotion-cache-1y4p8pa hr,
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Sidebar Success Messages */
    .css-1d391kg .stSuccess, .css-1lcbmhc .stSuccess, .css-17eq0hr .stSuccess,
    .st-emotion-cache-16txtl3 .stSuccess, .st-emotion-cache-1y4p8pa .stSuccess,
    section[data-testid="stSidebar"] .stSuccess {
        background-color: rgba(40, 167, 69, 0.2) !important;
        border: 1px solid rgba(40, 167, 69, 0.5) !important;
        color: #90EE90 !important;
    }
    
    /* Sidebar Warning Messages */
    .css-1d391kg .stWarning, .css-1lcbmhc .stWarning, .css-17eq0hr .stWarning,
    .st-emotion-cache-16txtl3 .stWarning, .st-emotion-cache-1y4p8pa .stWarning,
    section[data-testid="stSidebar"] .stWarning {
        background-color: rgba(255, 193, 7, 0.2) !important;
        border: 1px solid rgba(255, 193, 7, 0.5) !important;
        color: #FFE066 !important;
    }
    
    /* Sidebar Error Messages */
    .css-1d391kg .stError, .css-1lcbmhc .stError, .css-17eq0hr .stError,
    .st-emotion-cache-16txtl3 .stError, .st-emotion-cache-1y4p8pa .stError,
    section[data-testid="stSidebar"] .stError {
        background-color: rgba(220, 53, 69, 0.2) !important;
        border: 1px solid rgba(220, 53, 69, 0.5) !important;
        color: #FFB3BA !important;
    }
    
    /* Sidebar Info Messages */
    .css-1d391kg .stInfo, .css-1lcbmhc .stInfo, .css-17eq0hr .stInfo,
    .st-emotion-cache-16txtl3 .stInfo, .st-emotion-cache-1y4p8pa .stInfo,
    section[data-testid="stSidebar"] .stInfo {
        background-color: rgba(23, 162, 184, 0.2) !important;
        border: 1px solid rgba(23, 162, 184, 0.5) !important;
        color: #87CEEB !important;
    }
    
    /* Sidebar Markdown Text */
    .css-1d391kg .stMarkdown, .css-1lcbmhc .stMarkdown, .css-17eq0hr .stMarkdown,
    .st-emotion-cache-16txtl3 .stMarkdown, .st-emotion-cache-1y4p8pa .stMarkdown,
    section[data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }
    
    /* Additional Modern Streamlit Selectors */
    section[data-testid="stSidebar"] .element-container,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown div {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Example usage
if __name__ == "__main__":
    st.set_page_config(
        page_title="Sidebar Fix Demo",
        page_icon="🔧",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply the fix
    apply_sidebar_fix()
    
    st.title("🔧 Quick Sidebar Fix Demo")
    st.write("This demonstrates the quick sidebar visibility fix.")
    
    with st.sidebar:
        st.title("🎯 Test Sidebar")
        st.write("This text should now be visible!")
        
        st.radio("Choose option:", ["Option 1", "Option 2", "Option 3"])
        st.checkbox("Test checkbox")
        st.selectbox("Test selectbox", ["A", "B", "C"])
        
        st.success("Success message")
        st.warning("Warning message")
        st.error("Error message")
        st.info("Info message")