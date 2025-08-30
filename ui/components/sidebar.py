"""Sidebar Component for JobSniper AI

Modern, responsive sidebar with navigation using centralized UI constants.
"""

import streamlit as st
from ..core.ui_constants import UIConstants

def sidebar(initial_page: str = None):
    """Create and render the main application sidebar"""
    # Use UI constants for brand information
    st.sidebar.image(
        UIConstants.BRAND['logo_url'],
        width=UIConstants.BRAND['logo_width']
    )

    st.sidebar.markdown(f"""
        <h2 style='
            color:{UIConstants.DESIGN["colors"]["primary"]};
            margin-bottom:1.5rem;
            font-size:{UIConstants.DESIGN["typography"]["brand_size"]};
            font-family:{UIConstants.DESIGN["typography"]["primary_font"]};
        '>{UIConstants.BRAND['short_name']}</h2>
    """, unsafe_allow_html=True)

    # Use UI constants for page list
    pages = UIConstants.get_sidebar_pages()
    if initial_page and initial_page in pages:
        index = pages.index(initial_page)
    else:
        index = 0
    page = st.sidebar.radio("Navigation", pages, index=index, label_visibility="collapsed")

    st.sidebar.markdown(f"""
        <hr style='
            margin:2rem 0 1rem 0;
            border:0;
            border-top:1px solid {UIConstants.DESIGN["colors"]["glass_border"]};
        '>
    """, unsafe_allow_html=True)

    st.sidebar.markdown(f"""
        <small style='color: #888;'>{UIConstants.BRAND['copyright']}</small>
    """, unsafe_allow_html=True)

    return page