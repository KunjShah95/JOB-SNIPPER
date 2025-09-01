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

from ui.templates.page_template import render_standard_page, render_placeholder_tab
from ui.components.quantum_components import quantum_card
from ui.core.ui_constants import UIConstants
from agents.advanced_interview_prep_agent import AdvancedInterviewPrepAgent
from agents.web_scraper_agent import WebScraperAgent
from utils.error_handler import global_error_handler, safe_execute


def render():
    """Main interview preparation page"""
    
    # Initialize session state
    if "interview_sessions" not in st.session_state:
        st.session_state.interview_sessions = []
    if "practice_questions" not in st.session_state:
        st.session_state.practice_questions = []
    
    # Configure tabs
    tabs_config = [
        {"key": "quick_prep", "label": "🎯 Quick Prep"},
        {"key": "mock_interview", "label": "🎤 Mock Interview"},
        {"key": "company_research", "label": "🏢 Company Research"},
        {"key": "question_bank", "label": "📚 Question Bank"},
        {"key": "progress", "label": "📊 Progress"}
    ]
    
    tab_renders = {
        "quick_prep": _render_quick_prep_tab,
        "mock_interview": _render_mock_interview_tab,
        "company_research": _render_company_research_tab,
        "question_bank": _render_question_bank_tab,
        "progress": _render_progress_tab
    }
    
    # Use standard page template
    render_standard_page(
        title="Interview Preparation",
        subtitle="Practice and prepare for interviews with AI-powered assistance",
        icon="🎤",
        tabs_config=tabs_config,
        tab_renders=tab_renders,
        gradient="sunset"
    )


def _render_quick_prep_tab():
    """Render quick preparation tab"""
    
    quantum_card(
        title="⚡ Quick Interview Prep",
        content="""
        <p style="color: #6B7280; margin-bottom: 1.5rem;">
            Fill in your interview details to get a personalized preparation plan tailored to your role and company.
        </p>
        """,
        card_type="glass"
    )
    
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
    render_placeholder_tab("AI-powered mock interviews coming soon! Practice with realistic scenarios and get instant feedback.")

def _render_company_research_tab():
    """Render company research tab"""
    render_placeholder_tab("Get comprehensive company insights, culture information, and interview tips for your target companies.")

def _render_question_bank_tab():
    """Render question bank tab"""
    render_placeholder_tab("Access thousands of interview questions categorized by role, company, and difficulty level.")

def _render_progress_tab():
    """Render progress tab"""
    render_placeholder_tab("Track your interview preparation progress and see your improvement over time.")

def _generate_prep_plan(data):
    """Generate preparation plan"""
    st.info("🚧 Preparation plan generation feature coming soon! Your personalized prep plan will be generated based on your inputs.")