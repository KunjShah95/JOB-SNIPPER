"""
Standard Page Template for JobSniper AI
======================================

Template for consistent UI/UX across all AI agent sections.
All pages should follow this pattern for unified design.
"""

import streamlit as st
from ui.components.quantum_components import quantum_header, quantum_card
from ui.core.ui_constants import UIConstants
from ui.core.design_system import QuantumDesignSystem


def render_standard_page(
    title: str,
    subtitle: str,
    icon: str,
    tabs_config: list,
    tab_renders: dict,
    gradient: str = "ocean"
):
    """
    Standard page render function for consistent UI across all pages.
    
    Args:
        title: Page title
        subtitle: Page subtitle/description
        icon: Page icon emoji
        tabs_config: List of tab configurations [{"key": "tab1", "label": "🎯 Tab 1"}, ...]
        tab_renders: Dict mapping tab keys to render functions {"tab1": render_tab1_func, ...}
        gradient: Header gradient theme
    """
    # Add content offset for fixed navbar
    st.markdown('<div class="jobsniper-content-offset">', unsafe_allow_html=True)
    
    # Apply global styles
    QuantumDesignSystem.inject_global_styles()
    
    # Render quantum header
    quantum_header(
        title=title,
        subtitle=subtitle,
        icon=icon,
        gradient=gradient
    )
    
    # Create tabs
    if tabs_config and len(tabs_config) > 1:
        tab_objects = st.tabs([tab["label"] for tab in tabs_config])
        
        for i, tab_config in enumerate(tabs_config):
            with tab_objects[i]:
                tab_key = tab_config["key"]
                if tab_key in tab_renders:
                    tab_renders[tab_key]()
                else:
                    render_placeholder_tab(tab_config.get("placeholder", "Coming Soon"))
    else:
        # Single content page
        if tabs_config and len(tabs_config) == 1:
            tab_key = tabs_config[0]["key"]
            if tab_key in tab_renders:
                tab_renders[tab_key]()
    
    # Close content offset
    st.markdown('</div>', unsafe_allow_html=True)


def render_placeholder_tab(message: str = "Coming Soon"):
    """Render a consistent placeholder for tabs under development"""
    quantum_card(
        title="🚧 Under Development",
        content=f"""
        <div style="text-align: center; padding: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">⚙️</div>
            <h3 style="color: {UIConstants.DESIGN['colors']['primary']}; margin-bottom: 1rem;">{message}</h3>
            <p style="color: #6B7280; font-size: 1.1rem; margin-bottom: 2rem;">
                This feature is being built with cutting-edge AI technology.
            </p>
            <div style="
                background: rgba(59, 130, 246, 0.1);
                border: 1px solid rgba(59, 130, 246, 0.2);
                border-radius: 12px;
                padding: 1rem;
                color: #3B82F6;
                font-weight: 600;
            ">
                💡 Stay tuned for revolutionary AI-powered features!
            </div>
        </div>
        """,
        card_type="glass"
    )


def render_error_state(error_message: str):
    """Render consistent error state"""
    quantum_card(
        title="⚠️ Error",
        content=f"""
        <div style="text-align: center; padding: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">❌</div>
            <p style="color: #EF4444; font-size: 1.1rem;">{error_message}</p>
        </div>
        """,
        card_type="glass"
    )


def render_loading_state(message: str = "Loading..."):
    """Render consistent loading state"""
    quantum_card(
        title="🔄 Loading",
        content=f"""
        <div style="text-align: center; padding: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">⏳</div>
            <p style="color: #6B7280; font-size: 1.1rem;">{message}</p>
        </div>
        """,
        card_type="glass"
    )


def render_empty_state(title: str, description: str, icon: str = "📊", action_text: str = ""):
    """Render consistent empty state"""
    action_html = f"""
    <div style="margin-top: 1.5rem;">
        <button style="
            background: linear-gradient(135deg, {UIConstants.DESIGN['colors']['primary']}, {UIConstants.DESIGN['colors']['secondary']});
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            cursor: pointer;
        ">{action_text}</button>
    </div>
    """ if action_text else ""
    
    quantum_card(
        content=f"""
        <div style="text-align: center; padding: 3rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">{icon}</div>
            <h3 style="color: {UIConstants.DESIGN['colors']['primary']}; margin-bottom: 1rem;">{title}</h3>
            <p style="color: #6B7280; font-size: 1.1rem; margin-bottom: 1rem;">{description}</p>
            {action_html}
        </div>
        """,
        card_type="glass"
    )