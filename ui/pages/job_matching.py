"""Job Matching Page for JobSniper AI

Modern job matching interface with smart recommendations,
compatibility scoring, and personalized job discovery.
"""

import streamlit as st
import sys
import os
from typing import Dict, List, Any
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ui.templates.page_template import render_standard_page, render_empty_state
from ui.components.quantum_components import quantum_card
from ui.core.ui_constants import UIConstants
from agents.job_matcher_agent import JobMatcherAgent
from agents.message_protocol import AgentMessage
from utils.error_handler import global_error_handler, safe_execute


def render():
    """Render the job matching page"""
    
    # Initialize session state
    if "job_matches" not in st.session_state:
        st.session_state.job_matches = None
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {}
    
    # Configure tabs
    tabs_config = [
        {"key": "find_matches", "label": "🎯 Find Matches"},
        {"key": "match_results", "label": "📊 Match Results"},
        {"key": "preferences", "label": "⚙️ Preferences"}
    ]
    
    tab_renders = {
        "find_matches": _render_matching_form,
        "match_results": _render_match_results,
        "preferences": _render_preferences_tab
    }
    
    # Use standard page template
    render_standard_page(
        title="Job Matching",
        subtitle="AI-powered job recommendations based on your skills and experience",
        icon="🎯",
        tabs_config=tabs_config,
        tab_renders=tab_renders,
        gradient="ocean"
    )

def _render_matching_form():
    """Render job matching form"""
    
    quantum_card(
        title="🎯 Find Your Perfect Job Match",
        content="""
        <p style="color: #6B7280; margin-bottom: 1.5rem;">
            Fill in your details to get AI-powered job recommendations tailored to your skills and preferences.
        </p>
        """,
        card_type="glass"
    )

    with st.form("job_matching_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Your Skills** <span style='color: {UIConstants.DESIGN['colors']['primary']};'>*</span>", unsafe_allow_html=True)
            skills_input = st.text_area(
                "Enter your skills (comma-separated)",
                placeholder="Python, JavaScript, SQL, Machine Learning, React...",
                help="List your technical and soft skills",
                label_visibility="collapsed"
            )

            experience_level = st.selectbox(
                "Experience Level",
                ["Entry Level (0-2 years)", "Mid Level (3-5 years)",
                 "Senior Level (6-10 years)", "Lead/Principal (10+ years)"]
            )

        with col2:
            st.markdown("**Job Preferences:**")
            preferred_roles = st.text_area(
                "Preferred Job Roles",
                placeholder="Software Engineer, Data Scientist, Product Manager...",
                help="What roles are you interested in?",
                label_visibility="collapsed"
            )

            location_pref = st.text_input(
                "Preferred Location",
                placeholder="San Francisco, Remote, New York...",
                label_visibility="collapsed"
            )

        salary_min = st.number_input("Minimum Salary ($)", min_value=0, value=50000, step=5000)

        submitted = st.form_submit_button("🔍 Find Job Matches", use_container_width=True, type="primary")

        if submitted and skills_input:
            # Process the matching
            skills_list = [skill.strip() for skill in skills_input.split(',') if skill.strip()]

            # Use the job matcher agent
            from agents.job_matcher_agent import JobMatcherAgent
            from agents.message_protocol import AgentMessage

            try:
                matcher = JobMatcherAgent()

                # Create message for the agent
                user_data = {
                    'skills': skills_list,
                    'experience_level': experience_level,
                    'preferred_roles': preferred_roles,
                    'location': location_pref,
                    'salary_min': salary_min
                }

                msg = AgentMessage("UI", "JobMatcherAgent", user_data).to_json()
                result_json = matcher.run(msg)
                result_msg = AgentMessage.from_json(result_json)
                match_results = result_msg.data

                # Store results
                st.session_state.job_matches = match_results
                st.success("✅ Job matching completed! Check the Match Results tab.")

            except Exception as e:
                st.error(f"Error in job matching: {str(e)}")
                # Fallback results
                st.session_state.job_matches = {
                    'matched_skills': skills_list[:3],
                    'match_percent': 65,
                    'suggested_skills': ['AWS', 'Docker', 'React'],
                    'job_roles': ['Software Developer', 'Full Stack Developer']
                }
                st.info("Using fallback matching results for demo.")

        elif submitted:
            st.error("Please enter your skills to find job matches.")

def _render_match_results():
    """Render match results"""
    if 'job_matches' not in st.session_state or st.session_state.job_matches is None:
        render_empty_state(
            title="No Match Results",
            description="Run a job search first to see your personalized job matches here.",
            icon="📊",
            action_text="Find Job Matches"
        )
        return

    results = st.session_state.job_matches

    # Overall match score with quantum card
    match_percent = results.get('match_percent', 0)
    
    quantum_card(
        title="📊 Your Job Match Results",
        content=f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="
                font-size: 3rem; 
                font-weight: 800; 
                color: {UIConstants.DESIGN['colors']['primary']};
                margin-bottom: 0.5rem;
            ">{match_percent}%</div>
            <div style="color: #6B7280; font-size: 1.1rem;">Overall Match Score</div>
        </div>
        """,
        card_type="glass"
    )

    col1, col2 = st.columns(2)

    with col1:
        matched_skills = results.get('matched_skills', [])
        skills_content = ""
        if matched_skills:
            for skill in matched_skills:
                skills_content += f"""
                <div style="
                    display: flex; 
                    align-items: center; 
                    margin-bottom: 0.5rem;
                    color: {UIConstants.DESIGN['colors']['success']};
                ">
                    <span style="margin-right: 0.5rem;">✅</span>
                    <span>{skill}</span>
                </div>
                """
        else:
            skills_content = "<p style='color: #6B7280;'>No matching skills found</p>"
        
        quantum_card(
            title="🎯 Your Matching Skills",
            content=skills_content,
            card_type="glass"
        )

    with col2:
        suggested_skills = results.get('suggested_skills', [])
        skills_content = ""
        if suggested_skills:
            for skill in suggested_skills:
                skills_content += f"""
                <div style="
                    display: flex; 
                    align-items: center; 
                    margin-bottom: 0.5rem;
                    color: {UIConstants.DESIGN['colors']['info']};
                ">
                    <span style="margin-right: 0.5rem;">📚</span>
                    <span>{skill}</span>
                </div>
                """
        else:
            skills_content = "<p style='color: #6B7280;'>No skill suggestions available</p>"
        
        quantum_card(
            title="📚 Skills to Learn",
            content=skills_content,
            card_type="glass"
        )

    # Recommended job roles
    job_roles = results.get('job_roles', [])
    if job_roles:
        roles_content = ""
        for role in job_roles:
            roles_content += f"""
            <div style="
                background: rgba(59, 130, 246, 0.05);
                border: 1px solid rgba(59, 130, 246, 0.2);
                border-radius: 12px;
                padding: 1rem;
                margin-bottom: 1rem;
            ">
                <h4 style="color: {UIConstants.DESIGN['colors']['primary']}; margin: 0 0 0.5rem 0;">🎯 {role}</h4>
                <p style="color: #6B7280; margin: 0;">Based on your skills, you're a good match for {role} positions.</p>
                <div style="margin-top: 0.5rem; font-size: 0.9rem; color: #6B7280;">
                    <strong>Why this role fits:</strong><br>
                    • Your skills align with typical requirements<br>
                    • Good career progression opportunity<br>
                    • Market demand is strong
                </div>
            </div>
            """
        
        quantum_card(
            title="🎯 Recommended Job Roles",
            content=roles_content,
            card_type="glass"
        )
    else:
        quantum_card(
            title="🎯 Recommended Job Roles",
            content="<p style='color: #6B7280; text-align: center;'>No specific role recommendations available</p>",
            card_type="glass"
        )

def _render_preferences_tab():
    """Render preferences tab"""
    render_empty_state(
        title="Matching Preferences",
        description="Set your job search preferences and filters here when the feature becomes available.",
        icon="⚙️"
    )
