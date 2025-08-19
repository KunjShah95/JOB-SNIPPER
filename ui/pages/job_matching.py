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

from ui.core.design_system import apply_global_styles
from ui.styles.modern_theme import set_modern_theme
from agents.job_matcher_agent import JobMatcherAgent
from agents.message_protocol import AgentMessage
from utils.error_handler import global_error_handler, safe_execute


def render():
    """Render the job matching page"""

    set_modern_theme()
    apply_global_styles()
    st.markdown("""
        <div style='display:flex;align-items:center;gap:1rem;margin-bottom:2rem;'>
            <img src='https://img.icons8.com/ios-filled/100/2D6A4F/ai.png' width='44' style='margin-bottom:0;'>
            <div>
                <h1 style='margin-bottom:0;color:#2D6A4F;font-family:Inter,sans-serif;'>Job Matching</h1>
                <div style='color:#555;font-size:1.1rem;'>AI-powered job recommendations based on your skills and experience</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    if "job_matches" not in st.session_state:
        st.session_state.job_matches = None
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {}
    tab1, tab2, tab3 = st.tabs(["🎯 Find Matches", "📊 Match Results", "⚙️ Preferences"])
    with tab1:
        _render_matching_form()
    with tab2:
        _render_match_results()
    with tab3:
        _render_preferences_tab()

def _render_matching_form():
    """Render job matching form"""
    st.subheader("🎯 Find Your Perfect Job Match")

    with st.form("job_matching_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Your Skills:**")
            skills_input = st.text_area(
                "Enter your skills (comma-separated)",
                placeholder="Python, JavaScript, SQL, Machine Learning, React...",
                help="List your technical and soft skills"
            )

            experience_level = st.selectbox(
                "Experience Level",
                ["Entry Level (0-2 years)", "Mid Level (3-5 years)",
                 "Senior Level (6-10 years)", "Lead/Principal (10+ years)"]
            )

        with col2:
            st.write("**Job Preferences:**")
            preferred_roles = st.text_area(
                "Preferred Job Roles",
                placeholder="Software Engineer, Data Scientist, Product Manager...",
                help="What roles are you interested in?"
            )

            location_pref = st.text_input(
                "Preferred Location",
                placeholder="San Francisco, Remote, New York..."
            )

        salary_min = st.number_input("Minimum Salary ($)", min_value=0, value=50000, step=5000)

        submitted = st.form_submit_button("🔍 Find Job Matches", use_container_width=True)

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
    if 'job_matches' not in st.session_state:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #666;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📊</div>
            <h3>No Match Results</h3>
            <p>Run a job search first to see your personalized job matches here.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    results = st.session_state.job_matches

    st.subheader("📊 Your Job Match Results")

    # Overall match score
    match_percent = results.get('match_percent', 0)
    st.metric("Overall Match Score", f"{match_percent}%")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### ✅ Your Matching Skills")
        matched_skills = results.get('matched_skills', [])
        if matched_skills:
            for skill in matched_skills:
                st.write(f"• {skill}")
        else:
            st.write("No matching skills found")

    with col2:
        st.write("### 📚 Skills to Learn")
        suggested_skills = results.get('suggested_skills', [])
        if suggested_skills:
            for skill in suggested_skills:
                st.write(f"• {skill}")
        else:
            st.write("No skill suggestions available")

    # Recommended job roles
    st.write("### 🎯 Recommended Job Roles")
    job_roles = results.get('job_roles', [])
    if job_roles:
        for role in job_roles:
            with st.expander(f"🎯 {role}"):
                st.write(f"Based on your skills, you're a good match for {role} positions.")
                st.write("**Why this role fits:**")
                st.write("- Your skills align with typical requirements")
                st.write("- Good career progression opportunity")
                st.write("- Market demand is strong")
    else:
        st.write("No specific role recommendations available")

def _render_preferences_tab():
    """Render preferences tab"""
    st.markdown("""
    <div style="text-align: center; padding: 3rem; color: #666;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">⚙️</div>
        <h3>Matching Preferences</h3>
        <p>Set your job search preferences and filters here when the feature becomes available.</p>
    </div>
    """, unsafe_allow_html=True)
