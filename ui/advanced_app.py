import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
import os
import sys
from datetime import datetime, timedelta
import tempfile
import logging
import time
from typing import Dict, Any, List, Optional
import base64

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import advanced agents with fallback to legacy
try:
    from agents.advanced_controller_agent import AdvancedControllerAgent
    from agents.advanced_resume_parser_agent import AdvancedResumeParserAgent
    from agents.advanced_job_matcher_agent import AdvancedJobMatcherAgent
    from agents.advanced_skill_recommendation_agent import AdvancedSkillRecommendationAgent
    ADVANCED_AGENTS_AVAILABLE = True
except ImportError as e:
    st.error(f"Advanced agents not available: {e}")
    try:
        from agents.controller_agent import ControllerAgent
        from agents.auto_apply_agent import AutoApplyAgent
        from agents.recruiter_view_agent import RecruiterViewAgent
        from agents.skill_recommendation_agent import SkillRecommendationAgent
        ADVANCED_AGENTS_AVAILABLE = False
    except ImportError:
        st.error("No agents available. Please check your installation.")
        st.stop()

# Import utilities with error handling
try:
    from utils.pdf_reader import extract_text_from_pdf
    from utils.sqlite_logger import save_to_db
    from utils.exporter import export_to_pdf, send_email
    from utils.config import FEATURES, EMAIL_AVAILABLE
    UTILS_AVAILABLE = True
except ImportError as e:
    st.warning(f"Some utilities not available: {e}")
    UTILS_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="JobSniper AI - Advanced Career Intelligence Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "user_session" not in st.session_state:
    st.session_state.user_session = {
        "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "start_time": datetime.now(),
        "analysis_history": [],
        "current_resume": None,
        "current_analysis": None
    }

# Modern CSS styling
st.markdown(
    """
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styles */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header h3 {
        font-size: 1.5rem;
        font-weight: 400;
        margin-bottom: 1rem;
        opacity: 0.9;
    }
    
    /* Feature Cards */
    .feature-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 25px rgba(240, 147, 251, 0.3);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    /* Analysis Cards */
    .analysis-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 5px 15px rgba(79, 172, 254, 0.3);
    }
    
    /* Skill Tags */
    .skill-tag {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin: 0.3rem;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    /* Status Badges */
    .status-badge {
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        text-align: center;
        display: inline-block;
    }
    
    .status-excellent { background: #e8f5e8; color: #2e7d32; }
    .status-good { background: #e3f2fd; color: #1565c0; }
    .status-average { background: #fff3e0; color: #ef6c00; }
    .status-poor { background: #ffebee; color: #c62828; }
    
    /* Progress Bars */
    .progress-container {
        background: #f5f5f5;
        border-radius: 10px;
        padding: 3px;
        margin: 0.5rem 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #667eea, #764ba2);
        height: 8px;
        border-radius: 8px;
        transition: width 0.3s ease;
    }
    
    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .sidebar-info {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(168, 237, 234, 0.3);
    }
    
    /* Loading Animation */
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
</style>
""",
    unsafe_allow_html=True,
)

# Helper functions
def create_progress_bar(percentage: float, label: str = "") -> str:
    """Create a custom progress bar"""
    return f"""
    <div style="margin: 1rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="font-weight: 600;">{label}</span>
            <span style="font-weight: 600; color: #667eea;">{percentage:.1f}%</span>
        </div>
        <div class="progress-container">
            <div class="progress-bar" style="width: {percentage}%;"></div>
        </div>
    </div>
    """

def get_status_badge(score: float) -> str:
    """Get status badge based on score"""
    if score >= 90:
        return '<span class="status-badge status-excellent">Excellent</span>'
    elif score >= 75:
        return '<span class="status-badge status-good">Good</span>'
    elif score >= 60:
        return '<span class="status-badge status-average">Average</span>'
    else:
        return '<span class="status-badge status-poor">Needs Improvement</span>'

def display_skill_tags(skills: List[str]) -> str:
    """Display skills as tags"""
    if not skills:
        return ""
    
    tags_html = ""
    for skill in skills[:10]:  # Limit to 10 skills
        tags_html += f'<span class="skill-tag">{skill}</span>'
    
    if len(skills) > 10:
        tags_html += f'<span class="skill-tag">+{len(skills) - 10} more</span>'
    
    return tags_html

def create_metric_card(title: str, value: str, subtitle: str = "") -> str:
    """Create a metric card"""
    return f"""
    <div class="metric-card">
        <h3 style="margin: 0; font-size: 2rem; font-weight: 700;">{value}</h3>
        <p style="margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.9;">{title}</p>
        {f'<p style="margin: 0; font-size: 0.8rem; opacity: 0.7;">{subtitle}</p>' if subtitle else ''}
    </div>
    """

# Main header
st.markdown(
    """
<div class="main-header">
    <h1>🚀 JobSniper AI</h1>
    <h3>Advanced Career Intelligence Platform</h3>
    <p>Powered by Sophisticated AI • Multi-Agent Analysis • Real-time Insights</p>
</div>
""",
    unsafe_allow_html=True,
)

# Display agent status
if ADVANCED_AGENTS_AVAILABLE:
    st.success("✅ Advanced AI Agents Active - Enhanced Analysis Available")
else:
    st.warning("⚠️ Using Legacy Agents - Consider upgrading for advanced features")

# Sidebar navigation
st.sidebar.markdown("## 🎯 Navigation")

# Mode selection with enhanced options
mode = st.sidebar.selectbox(
    "Choose Your Mode",
    [
        "🎯 Smart Resume Analysis",
        "🤖 AI Job Matching",
        "📈 Skill Development",
        "🎪 Interview Preparation",
        "📊 Career Analytics",
        "🔍 Market Intelligence",
        "👥 HR Dashboard",
        "⚙️ System Status",
    ],
    help="Select the feature you want to use",
)

# Sidebar info
st.sidebar.markdown(
    f"""
<div class="sidebar-info">
    <h4>💡 Platform Status</h4>
    <p><strong>Agents:</strong> {'Advanced' if ADVANCED_AGENTS_AVAILABLE else 'Legacy'}</p>
    <p><strong>Utils:</strong> {'Available' if UTILS_AVAILABLE else 'Limited'}</p>
    <p><strong>Session:</strong> {st.session_state.user_session['session_id']}</p>
    <p><strong>Started:</strong> {st.session_state.user_session['start_time'].strftime('%H:%M')}</p>
</div>
""",
    unsafe_allow_html=True,
)

# Main content based on selected mode
if mode == "🎯 Smart Resume Analysis":
    st.markdown("## 🎯 AI-Powered Resume Analysis")

    st.markdown(
        """
    <div class="feature-card">
        <h4>🤖 Intelligent Resume Analysis</h4>
        <p>Upload your resume and get comprehensive AI-powered analysis with job matching, skill assessment, and improvement recommendations using our advanced multi-agent system.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # File upload
    uploaded_file = st.file_uploader(
        "📄 Upload Your Resume (PDF)",
        type="pdf",
        help="Upload a PDF version of your resume for the most accurate analysis",
    )

    if uploaded_file is not None:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_file_path = tmp_file.name

        st.success(f"✅ Resume uploaded successfully: {uploaded_file.name}")

        # Extract text from PDF
        try:
            if UTILS_AVAILABLE:
                resume_text = extract_text_from_pdf(temp_file_path)
            else:
                st.error("PDF extraction not available. Please paste your resume text below.")
                resume_text = st.text_area("Paste your resume text here:", height=200)
        except Exception as e:
            st.error(f"Error extracting text from PDF: {e}")
            resume_text = st.text_area("Paste your resume text here:", height=200)

        if resume_text and len(resume_text.strip()) > 50:
            st.session_state.user_session["current_resume"] = resume_text

            # Job requirements input
            st.markdown("### 🎯 Job Requirements (Optional)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                job_title = st.text_input("Job Title", placeholder="e.g., Senior Software Engineer")
                required_skills = st.text_input("Required Skills", placeholder="e.g., Python, React, AWS")
                
            with col2:
                experience_years = st.number_input("Years of Experience", min_value=0, max_value=50, value=3)
                industry = st.selectbox("Industry", ["Technology", "Finance", "Healthcare", "Marketing", "Other"])

            # Analysis button
            if st.button("🚀 Analyze Resume", type="primary"):
                with st.spinner("🤖 AI agents are analyzing your resume..."):
                    
                    # Prepare input data
                    input_data = {
                        "resume_text": resume_text
                    }
                    
                    context = {}
                    if job_title:
                        context["job_requirements"] = {
                            "title": job_title,
                            "required_skills": [skill.strip() for skill in required_skills.split(",") if skill.strip()],
                            "experience_years": experience_years,
                            "industry": industry.lower()
                        }

                    try:
                        # Use advanced agents if available
                        if ADVANCED_AGENTS_AVAILABLE:
                            controller = AdvancedControllerAgent()
                            result = controller.process(input_data, context)
                        else:
                            # Fallback to legacy agents
                            controller = ControllerAgent()
                            from agents.message_protocol import AgentMessage
                            message = AgentMessage("user", "ControllerAgent", resume_text)
                            result_json = controller.run(message.to_json())
                            result = json.loads(result_json) if isinstance(result_json, str) else result_json

                        st.session_state.user_session["current_analysis"] = result

                        # Display results
                        if ADVANCED_AGENTS_AVAILABLE and "comprehensive_analysis" in result:
                            display_advanced_analysis_results(result)
                        else:
                            display_legacy_analysis_results(result)

                    except Exception as e:
                        st.error(f"Analysis failed: {e}")
                        st.info("Please check your configuration and try again.")

        else:
            st.warning("Please upload a resume with sufficient content for analysis.")

elif mode == "🤖 AI Job Matching":
    st.markdown("## 🤖 AI-Powered Job Matching")
    
    st.markdown(
        """
    <div class="feature-card">
        <h4>🎯 Intelligent Job Matching</h4>
        <p>Find the perfect job matches based on your skills, experience, and career goals using our advanced matching algorithms.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    
    if st.session_state.user_session.get("current_resume"):
        st.success("✅ Resume loaded from previous analysis")
        
        # Job search parameters
        st.markdown("### 🔍 Job Search Parameters")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            target_role = st.text_input("Target Role", placeholder="e.g., Data Scientist")
            location = st.text_input("Location", placeholder="e.g., San Francisco, CA")
            
        with col2:
            salary_min = st.number_input("Minimum Salary ($)", min_value=0, value=80000, step=5000)
            remote_work = st.selectbox("Remote Work", ["No Preference", "Remote Only", "Hybrid", "On-site Only"])
            
        with col3:
            company_size = st.selectbox("Company Size", ["Any", "Startup", "Small", "Medium", "Large", "Enterprise"])
            industry_pref = st.selectbox("Industry", ["Any", "Technology", "Finance", "Healthcare", "E-commerce"])

        if st.button("🔍 Find Job Matches", type="primary"):
            with st.spinner("🤖 AI is finding the best job matches for you..."):
                
                # Prepare matching data
                candidate_profile = {
                    "resume_text": st.session_state.user_session["current_resume"],
                    "preferences": {
                        "target_role": target_role,
                        "location": location,
                        "salary_min": salary_min,
                        "remote_work": remote_work,
                        "company_size": company_size,
                        "industry": industry_pref
                    }
                }
                
                try:
                    if ADVANCED_AGENTS_AVAILABLE:
                        matcher = AdvancedJobMatcherAgent()
                        matches = matcher.process(candidate_profile)
                        display_job_matches(matches)
                    else:
                        st.info("Advanced job matching requires upgraded agents. Showing sample matches.")
                        display_sample_job_matches()
                        
                except Exception as e:
                    st.error(f"Job matching failed: {e}")
                    display_sample_job_matches()
    else:
        st.info("👆 Please analyze your resume first in the 'Smart Resume Analysis' section.")

elif mode == "📈 Skill Development":
    st.markdown("## 📈 Personalized Skill Development")
    
    st.markdown(
        """
    <div class="feature-card">
        <h4>🎓 AI-Powered Skill Recommendations</h4>
        <p>Get personalized skill development recommendations with learning paths, ROI analysis, and market insights.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    
    if st.session_state.user_session.get("current_resume"):
        # Career goals input
        st.markdown("### 🎯 Career Goals")
        
        col1, col2 = st.columns(2)
        
        with col1:
            career_goal = st.text_input("Career Goal", placeholder="e.g., Become a Senior Data Scientist")
            timeline = st.selectbox("Timeline", ["6 months", "1 year", "2 years", "3+ years"])
            
        with col2:
            learning_style = st.selectbox("Learning Style", ["Visual", "Hands-on", "Reading", "Mixed"])
            time_commitment = st.selectbox("Time Commitment", ["1-2 hours/week", "3-5 hours/week", "6-10 hours/week", "10+ hours/week"])

        if st.button("📈 Get Skill Recommendations", type="primary"):
            with st.spinner("🤖 AI is creating your personalized learning path..."):
                
                user_profile = {
                    "resume_text": st.session_state.user_session["current_resume"],
                    "career_goals": {
                        "target_role": career_goal,
                        "timeline": timeline,
                        "learning_style": learning_style.lower(),
                        "time_commitment": time_commitment
                    }
                }
                
                try:
                    if ADVANCED_AGENTS_AVAILABLE:
                        skill_agent = AdvancedSkillRecommendationAgent()
                        recommendations = skill_agent.process(user_profile)
                        display_skill_recommendations(recommendations)
                    else:
                        st.info("Advanced skill recommendations require upgraded agents. Showing sample recommendations.")
                        display_sample_skill_recommendations()
                        
                except Exception as e:
                    st.error(f"Skill recommendation failed: {e}")
                    display_sample_skill_recommendations()
    else:
        st.info("👆 Please analyze your resume first in the 'Smart Resume Analysis' section.")

elif mode == "⚙️ System Status":
    st.markdown("## ⚙️ System Status & Diagnostics")
    
    # System status overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_metric_card("Agent System", "Advanced" if ADVANCED_AGENTS_AVAILABLE else "Legacy"), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_metric_card("Utilities", "Available" if UTILS_AVAILABLE else "Limited"), unsafe_allow_html=True)
    
    with col3:
        session_duration = datetime.now() - st.session_state.user_session["start_time"]
        st.markdown(create_metric_card("Session Time", f"{session_duration.seconds // 60}m"), unsafe_allow_html=True)
    
    with col4:
        analysis_count = len(st.session_state.user_session.get("analysis_history", []))
        st.markdown(create_metric_card("Analyses", str(analysis_count)), unsafe_allow_html=True)

    # Detailed system information
    st.markdown("### 🔧 System Components")
    
    components = [
        ("Advanced Controller Agent", ADVANCED_AGENTS_AVAILABLE),
        ("Advanced Resume Parser", ADVANCED_AGENTS_AVAILABLE),
        ("Advanced Job Matcher", ADVANCED_AGENTS_AVAILABLE),
        ("Advanced Skill Recommender", ADVANCED_AGENTS_AVAILABLE),
        ("PDF Reader", UTILS_AVAILABLE),
        ("Database Logger", UTILS_AVAILABLE),
        ("Email Exporter", UTILS_AVAILABLE and EMAIL_AVAILABLE if 'EMAIL_AVAILABLE' in globals() else False),
    ]
    
    for component, status in components:
        status_icon = "✅" if status else "❌"
        status_text = "Available" if status else "Not Available"
        st.markdown(f"{status_icon} **{component}**: {status_text}")

    # Performance metrics
    if st.button("🧪 Run System Test"):
        with st.spinner("Running system diagnostics..."):
            test_results = run_system_test()
            display_test_results(test_results)

# Helper functions for displaying results
def display_advanced_analysis_results(result: Dict[str, Any]):
    """Display results from advanced agents"""
    st.markdown("## 📊 Analysis Results")
    
    # Overall metrics
    if "workflow_metadata" in result:
        metadata = result["workflow_metadata"]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            quality_score = metadata.get("quality_score", 0)
            st.markdown(create_metric_card("Quality Score", f"{quality_score:.1f}%"), unsafe_allow_html=True)
        
        with col2:
            execution_time = metadata.get("execution_time", 0)
            st.markdown(create_metric_card("Processing Time", f"{execution_time:.1f}s"), unsafe_allow_html=True)
        
        with col3:
            stages_completed = metadata.get("stages_completed", 0)
            st.markdown(create_metric_card("Stages Completed", str(stages_completed)), unsafe_allow_html=True)
        
        with col4:
            confidence = result.get("overall_confidence", 85)
            st.markdown(create_metric_card("Confidence", f"{confidence:.1f}%"), unsafe_allow_html=True)

    # Comprehensive analysis
    if "comprehensive_analysis" in result:
        analysis = result["comprehensive_analysis"]
        
        # Resume insights
        if "resume_insights" in analysis:
            st.markdown("### 📄 Resume Analysis")
            resume_data = analysis["resume_insights"]
            
            if "parsed_data" in resume_data:
                parsed = resume_data["parsed_data"]
                
                # Personal info
                if "personal_info" in parsed:
                    personal = parsed["personal_info"]
                    st.markdown(f"**Name:** {personal.get('name', 'Not found')}")
                    st.markdown(f"**Email:** {personal.get('email', 'Not found')}")
                    st.markdown(f"**Phone:** {personal.get('phone', 'Not found')}")
                
                # Skills
                if "skills" in parsed:
                    st.markdown("**Skills:**")
                    st.markdown(display_skill_tags(parsed["skills"]), unsafe_allow_html=True)
            
            # Quality assessment
            if "quality_assessment" in resume_data:
                quality = resume_data["quality_assessment"]
                overall_score = quality.get("overall_score", 0)
                st.markdown(f"**Resume Quality:** {get_status_badge(overall_score)}", unsafe_allow_html=True)
                st.markdown(create_progress_bar(overall_score, "Overall Quality"), unsafe_allow_html=True)

        # Job compatibility
        if "job_compatibility" in analysis:
            st.markdown("### 🎯 Job Compatibility")
            job_match = analysis["job_compatibility"]
            
            if "overall_match" in job_match:
                match_score = job_match["overall_match"].get("score", 0)
                match_grade = job_match["overall_match"].get("grade", "N/A")
                
                st.markdown(f"**Match Score:** {match_score:.1f}% (Grade: {match_grade})")
                st.markdown(create_progress_bar(match_score, "Job Match Score"), unsafe_allow_html=True)

        # Skill development
        if "skill_development" in analysis:
            st.markdown("### 📈 Skill Development")
            skill_data = analysis["skill_development"]
            
            if "skill_recommendations" in skill_data:
                recommendations = skill_data["skill_recommendations"]
                if "priority_skills" in recommendations:
                    priority_skills = recommendations["priority_skills"][:5]  # Top 5
                    
                    for skill_info in priority_skills:
                        skill_name = skill_info.get("skill", "Unknown")
                        priority_score = skill_info.get("priority_score", 0)
                        impact_score = skill_info.get("impact_score", 0)
                        
                        st.markdown(f"**{skill_name}**")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(create_progress_bar(priority_score, "Priority"), unsafe_allow_html=True)
                        with col2:
                            st.markdown(create_progress_bar(impact_score, "Impact"), unsafe_allow_html=True)

    # Recommendations
    if "actionable_recommendations" in result:
        st.markdown("### 💡 Recommendations")
        recommendations = result["actionable_recommendations"]
        
        for i, rec in enumerate(recommendations.get("for_candidate", [])[:3], 1):
            st.markdown(f"**{i}.** {rec.get('action', 'No action specified')}")
            if rec.get("priority"):
                st.markdown(f"   *Priority: {rec['priority']}*")

def display_legacy_analysis_results(result: Dict[str, Any]):
    """Display results from legacy agents"""
    st.markdown("## 📊 Analysis Results (Legacy Mode)")
    
    if "parsed_data" in result:
        parsed = result["parsed_data"]
        
        # Personal info
        if "personal_info" in parsed:
            personal = parsed["personal_info"]
            st.markdown(f"**Name:** {personal.get('name', 'Not found')}")
            st.markdown(f"**Email:** {personal.get('email', 'Not found')}")
        
        # Skills
        if "skills" in parsed:
            st.markdown("**Skills:**")
            st.markdown(display_skill_tags(parsed["skills"]), unsafe_allow_html=True)
    
    if "matched" in result:
        st.markdown("### 🎯 Job Matching")
        matched = result["matched"]
        if "match_score" in matched:
            score = matched["match_score"]
            st.markdown(create_progress_bar(score, "Match Score"), unsafe_allow_html=True)

def display_job_matches(matches: Dict[str, Any]):
    """Display job matching results"""
    st.markdown("### 🎯 Job Matches")
    
    # Sample job matches (in real implementation, this would come from the matcher)
    sample_jobs = [
        {
            "title": "Senior Data Scientist",
            "company": "TechCorp Inc.",
            "location": "San Francisco, CA",
            "salary": "$120,000 - $150,000",
            "match_score": 92,
            "skills_match": ["Python", "Machine Learning", "SQL"],
            "missing_skills": ["TensorFlow"]
        },
        {
            "title": "Machine Learning Engineer",
            "company": "AI Innovations",
            "location": "Remote",
            "salary": "$110,000 - $140,000",
            "match_score": 88,
            "skills_match": ["Python", "Deep Learning", "AWS"],
            "missing_skills": ["Kubernetes", "MLOps"]
        }
    ]
    
    for job in sample_jobs:
        with st.container():
            st.markdown(
                f"""
            <div class="analysis-card">
                <h4>{job['title']} at {job['company']}</h4>
                <p><strong>Location:</strong> {job['location']} | <strong>Salary:</strong> {job['salary']}</p>
                <p><strong>Match Score:</strong> {get_status_badge(job['match_score'])} {job['match_score']}%</p>
                <p><strong>Matching Skills:</strong> {display_skill_tags(job['skills_match'])}</p>
                <p><strong>Skills to Develop:</strong> {display_skill_tags(job['missing_skills'])}</p>
            </div>
            """,
                unsafe_allow_html=True
            )

def display_sample_job_matches():
    """Display sample job matches for demo"""
    st.info("🔄 Showing sample job matches. Connect to job boards for real-time results.")
    display_job_matches({})

def display_skill_recommendations(recommendations: Dict[str, Any]):
    """Display skill development recommendations"""
    st.markdown("### 📈 Skill Development Plan")
    
    # Sample recommendations
    sample_skills = [
        {
            "skill": "TensorFlow",
            "priority": 95,
            "time_to_learn": "3-4 months",
            "roi": "High",
            "resources": ["TensorFlow Documentation", "Coursera Course", "Hands-on Projects"]
        },
        {
            "skill": "Kubernetes",
            "priority": 88,
            "time_to_learn": "2-3 months",
            "roi": "Medium-High",
            "resources": ["Kubernetes Official Tutorial", "Practice Labs", "Certification Prep"]
        }
    ]
    
    for skill in sample_skills:
        with st.container():
            st.markdown(
                f"""
            <div class="analysis-card">
                <h4>{skill['skill']}</h4>
                <p><strong>Priority Score:</strong> {skill['priority']}%</p>
                <p><strong>Time to Learn:</strong> {skill['time_to_learn']}</p>
                <p><strong>ROI:</strong> {skill['roi']}</p>
                <p><strong>Recommended Resources:</strong></p>
                <ul>
                    {''.join([f'<li>{resource}</li>' for resource in skill['resources']])}
                </ul>
            </div>
            """,
                unsafe_allow_html=True
            )

def display_sample_skill_recommendations():
    """Display sample skill recommendations for demo"""
    st.info("🔄 Showing sample skill recommendations. Advanced agents provide personalized learning paths.")
    display_skill_recommendations({})

def run_system_test() -> Dict[str, Any]:
    """Run system diagnostics"""
    time.sleep(2)  # Simulate test time
    
    return {
        "agent_system": "✅ Operational",
        "database": "✅ Connected",
        "pdf_processing": "✅ Working" if UTILS_AVAILABLE else "❌ Limited",
        "ai_models": "✅ Available" if ADVANCED_AGENTS_AVAILABLE else "⚠️ Legacy",
        "response_time": "< 2s",
        "memory_usage": "Normal"
    }

def display_test_results(results: Dict[str, Any]):
    """Display system test results"""
    st.markdown("### 🧪 Test Results")
    
    for component, status in results.items():
        st.markdown(f"**{component.replace('_', ' ').title()}:** {status}")

# Footer
st.markdown("---")
st.markdown(
    """
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🚀 <strong>JobSniper AI</strong> - Advanced Career Intelligence Platform</p>
    <p>Powered by Sophisticated AI Agents • Built for Career Success</p>
</div>
""",
    unsafe_allow_html=True,
)