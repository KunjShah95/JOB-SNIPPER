"""Modern JobSniper AI Application

Completely refactored, modular application with modern UI/UX,
"""
import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.components.sidebar import sidebar
from ui.components.navbar import navbar
from ui.core.design_system import QuantumDesignSystem
from ui.core.ui_constants import UIConstants
from ui.pages import (
    home, application_tracker, resume_builder, resume_analysis, job_finder, job_matching,
    hr_dashboard, interview_prep, skill_recommendations, settings, resume_scoring,
    resume_qa_search, analytics_dashboard
)
from utils.config import load_config, validate_config
from utils.sqlite_logger import init_db

def main():
    st.set_page_config(
        page_title=UIConstants.BRAND['name'],
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    QuantumDesignSystem.inject_global_styles()

    # Handle query params for navbar navigation
    query_params = st.query_params
    initial_page = query_params.get('page', UIConstants.get_default_page())

    init_db()
    _ = load_config()
    # Validate config silently - don't display errors on main UI
    try:
        _ = validate_config()
    except Exception:
        pass  # Handle config validation silently

    page = sidebar(initial_page)

    # Render the top navigation bar
    navbar(active_page=page)

    page_map = {
        UIConstants.PAGES['home']['title']: home.render,
        UIConstants.PAGES['application_tracker']['title']: application_tracker.render,
        UIConstants.PAGES['resume_builder']['title']: resume_builder.render,
        UIConstants.PAGES['resume_analysis']['title']: resume_analysis.render,
        UIConstants.PAGES['resume_scoring']['title']: resume_scoring.render,
        UIConstants.PAGES['job_finder']['title']: job_finder.render,
        UIConstants.PAGES['job_matching']['title']: job_matching.render,
        UIConstants.PAGES['resume_qa_search']['title']: resume_qa_search.render,
        UIConstants.PAGES['analytics_dashboard']['title']: analytics_dashboard.render,
        UIConstants.PAGES['hr_dashboard']['title']: hr_dashboard.render,
        UIConstants.PAGES['interview_prep']['title']: interview_prep.render,
        UIConstants.PAGES['skill_recommendations']['title']: skill_recommendations.render,
        UIConstants.PAGES['settings']['title']: settings.render,
    }
    
    if page in page_map:
        page_map[page]()
    else:
        home.render()

if __name__ == "__main__":
    main()