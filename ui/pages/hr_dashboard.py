"""HR Dashboard Page for JobSniper AI

Comprehensive recruiter tools for candidate evaluation,
bulk resume processing, and hiring analytics.
"""

import streamlit as st
from ui.templates.page_template import render_standard_page
from ui.components.quantum_components import quantum_card
from ui.core.ui_constants import UIConstants

def render():
    """Render the HR dashboard page"""
    
    # Configure single content page
    tabs_config = [
        {"key": "main", "label": "HR Dashboard"}
    ]
    
    tab_renders = {
        "main": _render_hr_content
    }
    
    # Use standard page template
    render_standard_page(
        title="HR Dashboard",
        subtitle="Comprehensive recruiter tools for candidate evaluation and hiring analytics",
        icon="👔",
        tabs_config=tabs_config,
        tab_renders=tab_renders,
        gradient="cosmic"
    )

def _render_hr_content():
    """Render the main HR dashboard content"""
    
    quantum_card(
        title="🚧 Professional HR Dashboard Coming Soon!",
        content=f"""
        <div style="text-align: center; padding: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1.5rem;">👔</div>
            <p style="color: #6B7280; font-size: 1.1rem; margin-bottom: 2rem;">
                We're building a comprehensive HR platform that will revolutionize your recruitment process.
            </p>
            
            <div style="text-align: left; max-width: 600px; margin: 0 auto;">
                <h4 style="color: {UIConstants.DESIGN['colors']['primary']}; margin-bottom: 1rem;">🎯 Upcoming Features:</h4>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
                    <div style="
                        background: rgba(59, 130, 246, 0.05);
                        border: 1px solid rgba(59, 130, 246, 0.2);
                        border-radius: 12px;
                        padding: 1rem;
                    ">
                        <div style="color: {UIConstants.DESIGN['colors']['info']}; font-weight: 600; margin-bottom: 0.5rem;">📊 Bulk Resume Analysis</div>
                        <div style="color: #6B7280; font-size: 0.9rem;">Process hundreds of resumes simultaneously with AI-powered analysis</div>
                    </div>
                    
                    <div style="
                        background: rgba(16, 185, 129, 0.05);
                        border: 1px solid rgba(16, 185, 129, 0.2);
                        border-radius: 12px;
                        padding: 1rem;
                    ">
                        <div style="color: {UIConstants.DESIGN['colors']['success']}; font-weight: 600; margin-bottom: 0.5rem;">🎯 Candidate Ranking</div>
                        <div style="color: #6B7280; font-size: 0.9rem;">Intelligent scoring and ranking based on job requirements</div>
                    </div>
                    
                    <div style="
                        background: rgba(245, 158, 11, 0.05);
                        border: 1px solid rgba(245, 158, 11, 0.2);
                        border-radius: 12px;
                        padding: 1rem;
                    ">
                        <div style="color: {UIConstants.DESIGN['colors']['warning']}; font-weight: 600; margin-bottom: 0.5rem;">📈 Hiring Analytics</div>
                        <div style="color: #6B7280; font-size: 0.9rem;">Comprehensive insights and performance metrics</div>
                    </div>
                    
                    <div style="
                        background: rgba(139, 92, 246, 0.05);
                        border: 1px solid rgba(139, 92, 246, 0.2);
                        border-radius: 12px;
                        padding: 1rem;
                    ">
                        <div style="color: {UIConstants.DESIGN['colors']['secondary']}; font-weight: 600; margin-bottom: 0.5rem;">🔍 Advanced Search</div>
                        <div style="color: #6B7280; font-size: 0.9rem;">Smart filtering and candidate discovery tools</div>
                    </div>
                    
                    <div style="
                        background: rgba(99, 102, 241, 0.05);
                        border: 1px solid rgba(99, 102, 241, 0.2);
                        border-radius: 12px;
                        padding: 1rem;
                    ">
                        <div style="color: {UIConstants.DESIGN['colors']['primary']}; font-weight: 600; margin-bottom: 0.5rem;">📋 Interview Management</div>
                        <div style="color: #6B7280; font-size: 0.9rem;">Scheduling and collaboration tools for your team</div>
                    </div>
                    
                    <div style="
                        background: rgba(236, 72, 153, 0.05);
                        border: 1px solid rgba(236, 72, 153, 0.2);
                        border-radius: 12px;
                        padding: 1rem;
                    ">
                        <div style="color: #EC4899; font-weight: 600; margin-bottom: 0.5rem;">👥 Team Collaboration</div>
                        <div style="color: #6B7280; font-size: 0.9rem;">Share insights and collaborate on hiring decisions</div>
                    </div>
                </div>
                
                <div style="
                    background: linear-gradient(135deg, {UIConstants.DESIGN['colors']['primary']}, {UIConstants.DESIGN['colors']['secondary']});
                    border-radius: 12px;
                    padding: 1.5rem;
                    text-align: center;
                    color: white;
                ">
                    <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">💼 For Recruiters & HR Teams</div>
                    <div style="opacity: 0.9;">This dashboard will streamline your entire hiring process with cutting-edge AI technology!</div>
                </div>
            </div>
        </div>
        """,
        card_type="glass"
    )