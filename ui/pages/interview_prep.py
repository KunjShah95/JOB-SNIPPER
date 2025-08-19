"""Interview Preparation Page for JobSniper AI

Comprehensive interview preparation with AI-powered practice, company research, and tips.
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List, Any
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ui.core.design_system import apply_global_styles
from ui.styles.modern_theme import set_modern_theme
from agents.advanced_interview_prep_agent import AdvancedInterviewPrepAgent
from agents.web_scraper_agent import WebScraperAgent
from utils.error_handler import global_error_handler, safe_execute


def render():
    """Main interview preparation page"""
    
    set_modern_theme()
    apply_global_styles()
    st.markdown("""
        <div style='display:flex;align-items:center;gap:1rem;margin-bottom:2rem;'>
            <img src='https://img.icons8.com/ios-filled/100/2D6A4F/ai.png' width='44' style='margin-bottom:0;'>
            <div>
                <h1 style='margin-bottom:0;color:#2D6A4F;font-family:Inter,sans-serif;'>Interview Preparation</h1>
                <div style='color:#555;font-size:1.1rem;'>Practice and prepare for interviews with AI-powered assistance</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    if "interview_sessions" not in st.session_state:
        st.session_state.interview_sessions = []
    if "practice_questions" not in st.session_state:
        st.session_state.practice_questions = []
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Quick Prep", 
        "🎤 Mock Interview", 
        "🏢 Company Research", 
        "📚 Question Bank", 
        "📊 Progress"
    ])
    with tab1:
        _render_quick_prep_tab()
    with tab2:
        _render_mock_interview_tab()
    with tab3:
        _render_company_research_tab()
    with tab4:
        _render_question_bank_tab()
    with tab5:
        _render_progress_tab()


def _render_quick_prep_tab():
    """Render quick preparation tab"""
    
    st.markdown("""
    <div style='backdrop-filter: blur(8px); background: rgba(255,255,255,0.7); border-radius: 18px; box-shadow: 0 8px 32px 0 rgba(31,38,135,0.10); padding: 2rem 1.5rem; margin-bottom: 2rem;'>
        <h3 style='margin-top:0;'>⚡ Quick Interview Prep</h3>
        <p>Fill in your interview details to get a personalized preparation plan.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Interview details form
    with st.form("interview_prep_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input(
                "Company Name *",
                placeholder="e.g., Google, Microsoft",
                help="Enter the company you're interviewing with"
            )
            
            job_title = st.text_input(
                "Job Title *",
                placeholder="e.g., Software Engineer, Data Scientist",
                help="Enter the position you're applying for"
            )
            
            interview_type = st.selectbox(
                "Interview Type",
                ["Phone Screen", "Technical Interview", "Behavioral Interview", 
                 "System Design", "Final Round", "Panel Interview"],
                help="Select the type of interview"
            )
        
        with col2:
            interview_date = st.date_input(
                "Interview Date",
                value=datetime.now(),
                help="When is your interview scheduled?"
            )
            
            experience_level = st.selectbox(
                "Your Experience Level",
                ["Entry Level (0-2 years)", "Mid Level (3-5 years)", 
                 "Senior Level (6-10 years)", "Lead/Principal (10+ years)"],
                help="Your current experience level"
            )
            
            preparation_time = st.selectbox(
                "Available Prep Time",
                ["30 minutes", "1 hour", "2 hours", "Half day", "Full day", "Multiple days"],
                help="How much time do you have to prepare?"
            )
        
        # Additional details
        specific_topics = st.text_area(
            "Specific Topics/Technologies",
            placeholder="e.g., Python, React, Machine Learning, System Design...",
            help="Enter specific topics or technologies mentioned in the job description"
        )
        
        concerns = st.text_area(
            "Areas of Concern",
            placeholder="e.g., Coding challenges, behavioral questions, system design...",
            help="What aspects of the interview are you most concerned about?"
        )
        
        submitted = st.form_submit_button("🚀 Generate Prep Plan", use_container_width=True)
        
        if submitted and company_name and job_title:
            _generate_prep_plan({
                "company_name": company_name,
                "job_title": job_title,
                "interview_type": interview_type,
                "interview_date": interview_date,
                "experience_level": experience_level,
                "preparation_time": preparation_time,
                "specific_topics": specific_topics,
                "concerns": concerns
            })

def _render_mock_interview_tab():
    """Render mock interview tab"""
    st.markdown("""
    <div style="text-align: center; padding: 3rem; color: #666;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🎤</div>
        <h3>Mock Interview</h3>
        <p>AI-powered mock interviews coming soon! Practice with realistic scenarios and get instant feedback.</p>
    </div>
    """, unsafe_allow_html=True)

def _render_company_research_tab():
    """Render company research tab"""
    st.markdown("""
    <div style="text-align: center; padding: 3rem; color: #666;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🏢</div>
        <h3>Company Research</h3>
        <p>Get comprehensive company insights, culture information, and interview tips for your target companies.</p>
    </div>
    """, unsafe_allow_html=True)

def _render_question_bank_tab():
    """Render question bank tab"""
    st.markdown("""
    <div style="text-align: center; padding: 3rem; color: #666;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">📚</div>
        <h3>Question Bank</h3>
        <p>Access thousands of interview questions categorized by role, company, and difficulty level.</p>
    </div>
    """, unsafe_allow_html=True)

def _render_progress_tab():
    """Render progress tab"""
    st.markdown("""
    <div style="text-align: center; padding: 3rem; color: #666;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">📊</div>
        <h3>Progress Tracking</h3>
        <p>Track your interview preparation progress and see your improvement over time.</p>
    </div>
    """, unsafe_allow_html=True)

def _generate_prep_plan(data):
    """Generate preparation plan"""
    st.info("🚧 Preparation plan generation feature coming soon! Your personalized prep plan will be generated based on your inputs.")