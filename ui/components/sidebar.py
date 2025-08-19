"""Sidebar Component for JobSniper AI

Modern, responsive sidebar with navigation.
"""

import streamlit as st

def sidebar():
    """Create and render the main application sidebar"""
    st.sidebar.image('https://img.icons8.com/ios-filled/100/2D6A4F/ai.png', width=60)
    st.sidebar.markdown("""
        <h2 style='color:#2D6A4F;margin-bottom:1.5rem;font-size:1.6rem;font-family:Inter,sans-serif;'>Menu</h2>
    """, unsafe_allow_html=True)
    
    pages = [
        "Home",
        "Application Tracker",
        "Resume Builder",
        "Resume Analysis",
        "Job Finder",
        "Job Matching",
        "HR Dashboard",
        "Interview Prep",
        "Skill Recommendations",
        "Settings",
    ]
    
    page = st.sidebar.radio("", pages, index=0, label_visibility="collapsed")
    
    st.sidebar.markdown("<hr style='margin:2rem 0 1rem 0;border:0;border-top:1px solid #e0e0e0;'>", unsafe_allow_html=True)
    st.sidebar.markdown("<small style='color: #888;'>Job Snipper &copy; 2025</small>", unsafe_allow_html=True)
    
    return page