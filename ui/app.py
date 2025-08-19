"""Modern JobSniper AI Application

Completely refactored, modular application with modern UI/UX,
"""
import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.components.sidebar import sidebar
from ui.core.design_system import QuantumDesignSystem
from ui.pages import (
    home, application_tracker, resume_builder, resume_analysis, job_finder, job_matching,
    hr_dashboard, interview_prep, skill_recommendations, settings
)
from utils.config import load_config, validate_config
from utils.sqlite_logger import init_db

def main():
    st.set_page_config(page_title="JobSniper AI", layout="wide", initial_sidebar_state="expanded")
    
    QuantumDesignSystem.inject_global_styles()

    init_db()
    _ = load_config()
    # Validate config silently - don't display errors on main UI
    try:
        _ = validate_config()
    except Exception:
        pass  # Handle config validation silently

    page = sidebar()

    page_map = {
        "Home": home.render,
        "Application Tracker": application_tracker.render,
        "Resume Builder": resume_builder.render,
        "Resume Analysis": resume_analysis.render,
        "Job Finder": job_finder.render,
        "Job Matching": job_matching.render,
        "HR Dashboard": hr_dashboard.render,
        "Interview Prep": interview_prep.render,
        "Skill Recommendations": skill_recommendations.render,
        "Settings": settings.render,
    }
    
    if page in page_map:
        page_map[page]()
    else:
        home.render()

if __name__ == "__main__":
    main()