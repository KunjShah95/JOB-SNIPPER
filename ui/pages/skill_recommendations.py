"""Skill Recommendations Page for JobSniper AI

Personalized skill development recommendations with learning paths,
course suggestions, and career advancement guidance.
"""

import streamlit as st
from ui.templates.page_template import render_standard_page, render_empty_state
from ui.components.quantum_components import quantum_card
from ui.core.ui_constants import UIConstants

def render():
    """Render the skill recommendations page"""
    
    # Configure single content page
    tabs_config = [
        {"key": "main", "label": "Skill Recommendations"}
    ]
    
    tab_renders = {
        "main": _render_skills_content
    }
    
    # Use standard page template
    render_standard_page(
        title="Skill Recommendations",
        subtitle="Personalized learning paths and skill development guidance powered by AI",
        icon="📚",
        tabs_config=tabs_config,
        tab_renders=tab_renders,
        gradient="sunset"
    )

def _render_skills_content():
    """Render the skill recommendations content"""
    
    # Check if user has analyzed their resume
    if 'resume_analysis' in st.session_state:
        _render_personalized_recommendations()
    else:
        _render_general_recommendations()

def _render_personalized_recommendations():
    """Render personalized skill recommendations based on resume analysis"""
    
    results = st.session_state['resume_analysis']

    quantum_card(
        title="🎯 Personalized Skill Recommendations",
        content="""
        <p style="color: #6B7280; margin-bottom: 1.5rem;">
            Based on your resume analysis, here are skills that could boost your career trajectory.
        </p>
        """,
        card_type="glass"
    )

    # Get suggested skills from analysis
    if 'matched_data' in results and results['matched_data'].get('suggested_skills'):
        suggested_skills = results['matched_data']['suggested_skills']

        skills_content = ""
        for skill in suggested_skills:
            skills_content += f"""
            <div style="
                background: rgba(59, 130, 246, 0.05);
                border: 1px solid rgba(59, 130, 246, 0.2);
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1rem;
            ">
                <h4 style="color: {UIConstants.DESIGN['colors']['primary']}; margin: 0 0 1rem 0;">📖 Learn {skill}</h4>
                
                <div style="margin-bottom: 1rem;">
                    <strong style="color: #374151;">Why learn {skill}?</strong>
                    <ul style="color: #6B7280; margin: 0.5rem 0;">
                        <li>High demand in current job market</li>
                        <li>Complements your existing skills</li>
                        <li>Could increase salary potential</li>
                    </ul>
                </div>
                
                <div>
                    <strong style="color: #374151;">Learning Resources:</strong>
                    <ul style="color: #6B7280; margin: 0.5rem 0;">
                        <li>🎓 Online courses (Coursera, Udemy, Pluralsight)</li>
                        <li>📖 Official documentation and tutorials</li>
                        <li>🛠️ Hands-on projects and practice</li>
                        <li>👥 Community forums and study groups</li>
                    </ul>
                </div>
            </div>
            """
        
        quantum_card(
            title="📚 Priority Skills to Learn",
            content=skills_content,
            card_type="glass"
        )

    # Industry trends
    trending_content = ""
    trending_skills = ["Artificial Intelligence", "Cloud Computing", "DevOps", "Cybersecurity", "Data Analytics"]
    
    for skill in trending_skills:
        trending_content += f"""
        <div style="
            display: flex; 
            align-items: center; 
            margin-bottom: 0.75rem;
            padding: 0.5rem;
            background: rgba(245, 158, 11, 0.05);
            border-radius: 8px;
            border-left: 3px solid {UIConstants.DESIGN['colors']['warning']};
        ">
            <span style="margin-right: 0.75rem; font-size: 1.2rem;">🔥</span>
            <div>
                <strong style="color: {UIConstants.DESIGN['colors']['warning']};">{skill}</strong>
                <div style="color: #6B7280; font-size: 0.9rem;">High growth potential</div>
            </div>
        </div>
        """
    
    quantum_card(
        title="📈 Trending Skills in Your Field",
        content=trending_content,
        card_type="glass"
    )

def _render_general_recommendations():
    """Render general skill recommendations"""
    
    render_empty_state(
        title="Get Personalized Skill Recommendations",
        description="Upload and analyze your resume first to get personalized skill recommendations tailored to your career goals!",
        icon="🎯",
        action_text="Analyze Resume"
    )

    col1, col2 = st.columns(2)

    with col1:
        tech_skills = [
            "Artificial Intelligence", "Machine Learning", "Cloud Computing",
            "DevOps", "Cybersecurity", "Data Science", "React", "Python"
        ]
        
        tech_content = ""
        for skill in tech_skills:
            tech_content += f"""
            <div style="
                display: flex; 
                align-items: center; 
                margin-bottom: 0.5rem;
                color: {UIConstants.DESIGN['colors']['info']};
            ">
                <span style="margin-right: 0.5rem;">💻</span>
                <span>{skill}</span>
            </div>
            """
        
        quantum_card(
            title="🔥 Trending Technical Skills",
            content=tech_content,
            card_type="glass"
        )

    with col2:
        soft_skills = [
            "Leadership", "Communication", "Problem Solving",
            "Project Management", "Adaptability", "Critical Thinking"
        ]
        
        soft_content = ""
        for skill in soft_skills:
            soft_content += f"""
            <div style="
                display: flex; 
                align-items: center; 
                margin-bottom: 0.5rem;
                color: {UIConstants.DESIGN['colors']['success']};
            ">
                <span style="margin-right: 0.5rem;">🧠</span>
                <span>{skill}</span>
            </div>
            """
        
        quantum_card(
            title="🎯 Essential Soft Skills",
            content=soft_content,
            card_type="glass"
        )

    # Call to action
    quantum_card(
        content=f"""
        <div style="text-align: center; padding: 1.5rem;">
            <div style="
                background: linear-gradient(135deg, {UIConstants.DESIGN['colors']['primary']}, {UIConstants.DESIGN['colors']['secondary']});
                color: white;
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1rem;
            ">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">💡</div>
                <div style="font-size: 1.1rem; font-weight: 600;">Ready for Personalized Recommendations?</div>
                <div style="opacity: 0.9; margin-top: 0.5rem;">Analyze your resume in the Resume Analysis section to unlock tailored skill recommendations!</div>
            </div>
        </div>
        """,
        card_type="glass"
    )