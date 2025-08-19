"""Home Page for JobSniper AI (Modernized)

Modern, engaging home page with feature overview, quick actions,
and system status. Provides an intuitive entry point for users.
"""

import streamlit as st
from datetime import datetime
from utils.config import load_config, validate_config

def render():
    """Render the modern home page using glassmorphic design system"""
    # Welcome Header
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
    <div style='display:flex;align-items:center;gap:1.2rem;margin-bottom:2.5rem;'>
        <div style='font-size:2.5rem'>{icon}</div>
        <div>
            <h1 style='margin-bottom:0;color:#2D6A4F;font-family:Inter,sans-serif;'>{greeting}!</h1>
            <div style='color:#555;font-size:1.2rem;'>Welcome back to JobSniper AI. Ready to advance your career today?</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick Stats - Dynamic based on actual usage
    stats = [
        {"icon": "📄", "value": "0", "label": "Resumes Analyzed", "trend": "Start analyzing", "color": "#3B82F6"},
        {"icon": "🎯", "value": "0", "label": "Job Matches Found", "trend": "Upload resume first", "color": "#10B981"},
        {"icon": "📚", "value": "0", "label": "Skills Recommended", "trend": "Get started", "color": "#8B5CF6"},
        {"icon": "🏆", "value": "0%", "label": "Success Rate", "trend": "Track your progress", "color": "#F59E0B"},
    ]
    st.markdown("""
    <div style='display:flex;gap:1.5rem;margin-bottom:2.5rem;'>
    """ +
    "".join([
        f"<div style='flex:1;background:rgba(59,130,246,0.07);border-radius:16px;padding:1.2rem 1rem;text-align:center;box-shadow:0 2px 8px 0 rgba(31,38,135,0.07);'>"
        f"<div style='font-size:2rem'>{s['icon']}</div>"
        f"<div style='font-size:1.7rem;font-weight:700;color:{s['color']}'>{s['value']}</div>"
        f"<div style='color:#6B7280;font-size:1.1rem;margin-bottom:0.2rem'>{s['label']}</div>"
        f"<div style='color:#3B82F6;font-size:0.95rem'>{s['trend']}</div>"
        f"</div>" for s in stats
    ]) + "</div>", unsafe_allow_html=True)

    # Feature Overview
    features = [
        {"icon": "📄", "title": "Resume Analysis", "description": "AI-powered resume parsing and optimization with detailed feedback."},
        {"icon": "🎯", "title": "Job Matching", "description": "Smart job recommendations based on skills, experience, and career goals."},
        {"icon": "📚", "title": "Skill Development", "description": "Personalized learning paths and skill gap analysis."},
        {"icon": "🤖", "title": "Auto Apply", "description": "Automated job application generation and form filling."},
        {"icon": "👔", "title": "HR Dashboard", "description": "Comprehensive recruiter tools for candidate evaluation."},
        {"icon": "📊", "title": "Analytics", "description": "Detailed insights and performance metrics for career tracking."},
    ]
    st.markdown("""
    <div style='display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1.5rem;margin-bottom:2.5rem;'>
    """ +
    "".join([
        f"<div style='background:rgba(255,255,255,0.7);backdrop-filter:blur(8px);border-radius:16px;box-shadow:0 2px 8px 0 rgba(31,38,135,0.07);padding:1.2rem 1rem;'>"
        f"<div style='font-size:2rem;margin-bottom:0.5rem'>{f['icon']}</div>"
        f"<div style='font-size:1.2rem;font-weight:700;color:#2D6A4F;margin-bottom:0.2rem'>{f['title']}</div>"
        f"<div style='color:#6B7280;font-size:1rem'>{f['description']}</div>"
        f"</div>" for f in features
    ]) + "</div>", unsafe_allow_html=True)

    # System Status
    try:
        config = load_config()
        validation = validate_config()  # Remove the config argument
        ai_status = "online" if validation.get('ai_provider') else "offline"
        ai_providers = validation.get('ai_provider', 'Demo Mode')
        feature_count = validation.get('features_enabled', 0)
        feature_status = "online" if feature_count > 0 else "warning"
        st.markdown(f"""
        <div style='display:flex;gap:1.5rem;margin-bottom:2rem;'>
            <div style='flex:1;background:rgba(59,130,246,0.07);border-radius:16px;padding:1.2rem 1rem;'>
                <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;'><span>🤖 AI Services Status:</span><span style='font-weight:600;color:#3B82F6'>{ai_status.upper()}</span></div>
                <div style='color:#6B7280;font-size:1rem;'>Providers: {ai_providers}</div>
            </div>
            <div style='flex:1;background:rgba(16,185,129,0.07);border-radius:16px;padding:1.2rem 1rem;'>
                <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;'><span>🔧 Features Status:</span><span style='font-weight:600;color:#10B981'>{feature_status.upper()}</span></div>
                <div style='color:#6B7280;font-size:1rem;'>{feature_count} Active</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        # Configuration issues are handled in settings page
    except Exception:
        # Handle system status errors silently
        pass

    # Recent Activity - Show only if there's actual activity
    activity_data = []  # Will be populated from actual user activity

    st.markdown("""
    <div style='margin-top:2rem;'>
        <div style='font-size:1.3rem;font-weight:700;color:#2D6A4F;margin-bottom:1rem;'>Recent Activity</div>
    """, unsafe_allow_html=True)

    if activity_data:
        st.markdown("""
        <div style='display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1.2rem;'>
        """ +
        "".join([
            f"<div style='background:rgba(255,255,255,0.7);backdrop-filter:blur(8px);border-radius:16px;box-shadow:0 2px 8px 0 rgba(31,38,135,0.07);padding:1.2rem 1rem;'>"
            f"<div style='font-size:1.5rem;margin-bottom:0.3rem'>{a['icon']}</div>"
            f"<div style='font-size:1.1rem;font-weight:600;color:#2D6A4F;margin-bottom:0.2rem'>{a['title']}</div>"
            f"<div style='color:#6B7280;font-size:0.98rem'>{a['description']}</div>"
            f"<div style='color:#3B82F6;font-size:0.95rem;margin-top:0.5rem'>{a['time']}</div>"
            f"</div>" for a in activity_data
        ]) + "</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='text-align:center;padding:2rem;color:#666;background:rgba(255,255,255,0.5);border-radius:16px;'>
            <div style='font-size:3rem;margin-bottom:1rem;'>📊</div>
            <div style='font-size:1.1rem;'>No recent activity</div>
            <div style='font-size:0.9rem;margin-top:0.5rem;'>Start using JobSniper AI to see your activity here</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)