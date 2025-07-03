#!/usr/bin/env python3
"""
ONE-LINE Sidebar Fix for Streamlit

The simplest possible fix - just copy and paste this into your Streamlit app.
"""

import streamlit as st

def fix_sidebar():
    """One-line sidebar fix - copy this function to your app"""
    st.markdown('<style>section[data-testid="stSidebar"]{background:linear-gradient(180deg,#1a365d 0%,#2d3748 50%,#1a202c 100%)!important}section[data-testid="stSidebar"] *{color:white!important}</style>', unsafe_allow_html=True)

# Example usage
if __name__ == "__main__":
    st.set_page_config(page_title="One-Line Fix", layout="wide")
    
    # THE FIX - Just add this line to your app!
    fix_sidebar()
    
    st.title("🔧 One-Line Sidebar Fix")
    
    with st.sidebar:
        st.title("Test Sidebar")
        st.write("This text should be visible!")
        st.radio("Test:", ["Option 1", "Option 2"])
        st.success("Success!")
        st.warning("Warning!")
        st.error("Error!")
        st.info("Info!")
    
    st.write("✅ If you can see the sidebar text, the fix works!")