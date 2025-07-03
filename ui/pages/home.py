"""Home Page for JobSniper AI

Modern, engaging home page with feature overview, quick actions,
and system status. Provides an intuitive entry point for users.
"""

import streamlit as st
from typing import Dict, Any
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

from ui.styles.modern_theme import ModernTheme, apply_modern_theme, create_header, create_feature_grid
from utils.config import load_config, validate_config
from utils.error_handler import show_success, show_warning


def render_home_page():
    """Render the modern home page"""
    
    # Apply modern theme
    apply_modern_theme()
    
    # Create header
    create_header(
        title="JobSniper AI",
        subtitle="Professional Resume & Career Intelligence Platform",
        icon="🎯"
    )
    
    # Quick stats row
    render_quick_stats()
    
    # Feature overview
    render_feature_overview()
    
    # Quick actions
    render_quick_actions()
    
    # System status
    render_system_status()
    
    # Recent activity (if available)
    render_recent_activity()


def render_quick_stats():
    """Render quick statistics cards"""
    
    st.markdown("### 📊 Quick Stats")
    
    # Create metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        ModernTheme.create_metric_card(
            title="Resumes Analyzed",
            value="1,247",
            delta="+12% this week"
        )
    
    with col2:
        ModernTheme.create_metric_card(
            title="Job Matches Found",
            value="3,891",
            delta="+8% this week"
        )
    
    with col3:
        ModernTheme.create_metric_card(
            title="Skills Recommended",
            value="567",
            delta="+15% this week"
        )
    
    with col4:
        ModernTheme.create_metric_card(
            title="Success Rate",
            value="94.2%",
            delta="+2.1% improvement"
        )


def render_feature_overview():
    """Render feature overview grid"""
    
    st.markdown("### 🚀 Platform Features")
    
    features = [
        {
            "icon": "📄",
            "title": "Resume Analysis",
            "description": "AI-powered resume parsing and optimization with detailed feedback and improvement suggestions."
        },
        {
            "icon": "🎯",
            "title": "Job Matching",
            "description": "Smart job recommendations based on skills, experience, and career goals with compatibility scoring."
        },
        {
            "icon": "📚",
            "title": "Skill Development",
            "description": "Personalized learning paths and skill gap analysis with course recommendations."
        },
        {
            "icon": "🤖",
            "title": "Auto Apply",
            "description": "Automated job application generation and form filling for multiple platforms."
        },
        {
            "icon": "👔",
            "title": "HR Dashboard",
            "description": "Comprehensive recruiter tools for candidate evaluation and bulk resume processing."
        },
        {
            "icon": "📊",
            "title": "Analytics",
            "description": "Detailed insights and performance metrics for career progression tracking."
        }
    ]
    
    create_feature_grid(features)


def render_quick_actions():
    """Render quick action buttons"""
    
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ModernTheme.create_card(
            title="📄 Analyze Resume",
            content="""
            <p>Upload your resume for instant AI-powered analysis and feedback.</p>
            <div style="text-align: center; margin-top: 1rem;">
                <a href="#" style="background: #2E86AB; color: white; padding: 0.5rem 1rem; border-radius: 8px; text-decoration: none; font-weight: 500;">Start Analysis</a>
            </div>
            """
        )
    
    with col2:
        ModernTheme.create_card(
            title="🎯 Find Jobs",
            content="""
            <p>Discover job opportunities that match your skills and experience.</p>
            <div style="text-align: center; margin-top: 1rem;">
                <a href="#" style="background: #A23B72; color: white; padding: 0.5rem 1rem; border-radius: 8px; text-decoration: none; font-weight: 500;">Browse Jobs</a>
            </div>
            """
        )
    
    with col3:
        ModernTheme.create_card(
            title="📚 Learn Skills",
            content="""
            <p>Get personalized skill recommendations and learning paths.</p>
            <div style="text-align: center; margin-top: 1rem;">
                <a href="#" style="background: #F18F01; color: white; padding: 0.5rem 1rem; border-radius: 8px; text-decoration: none; font-weight: 500;">Explore Skills</a>
            </div>
            """
        )


def render_system_status():
    """Render system status information"""
    
    st.markdown("### 🔧 System Status")
    
    try:
        config = load_config()
        validation = validate_config(config)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # AI Providers Status
            ai_status = "🟢 Online" if validation['ai_providers'] else "🔴 Offline"
            ai_providers = ", ".join(validation['ai_providers']).title() if validation['ai_providers'] else "Demo Mode"
            
            ModernTheme.create_card(
                title="🤖 AI Services",
                content=f"""
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span><strong>Status:</strong> {ai_status}</span>
                    <span>{ModernTheme.create_status_badge(ai_providers, 'success' if validation['ai_providers'] else 'warning')}</span>
                </div>
                <p style="margin-top: 1rem; color: #6C757D;">
                    {len(validation['ai_providers'])} provider(s) available
                </p>
                """
            )
        
        with col2:
            # Features Status
            feature_count = len(validation['features_enabled'])
            feature_status = "🟢 Active" if feature_count > 0 else "🟡 Limited"
            
            ModernTheme.create_card(
                title="🔧 Features",
                content=f"""
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span><strong>Status:</strong> {feature_status}</span>
                    <span>{ModernTheme.create_status_badge(f"{feature_count} Features", 'success' if feature_count > 2 else 'warning')}</span>
                </div>
                <p style="margin-top: 1rem; color: #6C757D;">
                    {', '.join(validation['features_enabled']) if validation['features_enabled'] else 'Basic features only'}
                </p>
                """
            )
        
        # Configuration warnings
        if validation['issues']:
            st.warning("⚠️ Configuration Issues Detected")
            with st.expander("View Issues"):
                for issue in validation['issues']:
                    st.write(f"• {issue}")
                st.info("💡 Go to Settings to configure missing services")
    
    except Exception as e:
        st.error(f"❌ Error loading system status: {str(e)}")


def render_recent_activity():
    """Render recent activity section"""
    
    st.markdown("### 📈 Recent Activity")
    
    # Sample activity data (in production, this would come from database)
    activity_data = [
        {"time": "2 minutes ago", "action": "Resume analyzed", "user": "John Doe", "status": "success"},
        {"time": "5 minutes ago", "action": "Job match found", "user": "Jane Smith", "status": "success"},
        {"time": "10 minutes ago", "action": "Skill recommendation", "user": "Mike Johnson", "status": "info"},
        {"time": "15 minutes ago", "action": "Auto-apply submitted", "user": "Sarah Wilson", "status": "success"},
        {"time": "20 minutes ago", "action": "HR evaluation", "user": "David Brown", "status": "info"},
    ]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        ModernTheme.create_card(
            title="Recent Actions",
            content="""
            <div style="max-height: 300px; overflow-y: auto;">
            """ + "".join([
                f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid #E9ECEF;">
                    <div>
                        <strong>{activity['action']}</strong>
                        <br><small style="color: #6C757D;">{activity['user']}</small>
                    </div>
                    <div style="text-align: right;">
                        {ModernTheme.create_status_badge(activity['status'], activity['status'])}
                        <br><small style="color: #6C757D;">{activity['time']}</small>
                    </div>
                </div>
                """ for activity in activity_data
            ]) + "</div>"
        )
    
    with col2:
        # Activity chart
        render_activity_chart()


def render_activity_chart():
    """Render activity trend chart"""
    
    # Sample data for the last 7 days
    dates = [(datetime.now() - timedelta(days=i)).strftime("%m/%d") for i in range(6, -1, -1)]
    activities = [45, 52, 48, 61, 58, 67, 73]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=activities,
        mode='lines+markers',
        line=dict(color='#2E86AB', width=3),
        marker=dict(size=8, color='#2E86AB'),
        fill='tonexty',
        fillcolor='rgba(46, 134, 171, 0.1)'
    ))
    
    fig.update_layout(
        title="Activity Trend (7 days)",
        xaxis_title="Date",
        yaxis_title="Activities",
        height=250,
        margin=dict(l=0, r=0, t=40, b=0),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    
    st.plotly_chart(fig, use_container_width=True)


def render_welcome_message():
    """Render personalized welcome message"""
    
    current_hour = datetime.now().hour
    
    if current_hour < 12:
        greeting = "Good morning"
        icon = "🌅"
    elif current_hour < 17:
        greeting = "Good afternoon"
        icon = "☀️"
    else:
        greeting = "Good evening"
        icon = "🌙"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                padding: 1.5rem; 
                border-radius: 12px; 
                margin-bottom: 2rem;
                text-align: center;">
        <h2 style="margin: 0; color: white;">{icon} {greeting}!</h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
            Welcome back to JobSniper AI. Ready to advance your career today?
        </p>
    </div>
    """, unsafe_allow_html=True)


# Additional helper functions for the home page
def get_user_stats() -> Dict[str, Any]:
    """Get user statistics (placeholder for real implementation)"""
    return {
        'resumes_analyzed': 1247,
        'jobs_matched': 3891,
        'skills_recommended': 567,
        'success_rate': 94.2
    }


def get_system_health() -> Dict[str, Any]:
    """Get system health status"""
    try:
        config = load_config()
        validation = validate_config(config)
        
        return {
            'ai_providers': validation['ai_providers'],
            'features_enabled': validation['features_enabled'],
            'issues': validation['issues'],
            'overall_health': 'healthy' if validation['valid'] else 'warning'
        }
    except Exception:
        return {
            'ai_providers': [],
            'features_enabled': [],
            'issues': ['Configuration error'],
            'overall_health': 'error'
        }