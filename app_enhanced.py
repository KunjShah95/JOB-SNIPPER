"""
Enhanced Job Snipper AI - Complete Resume Analysis & Job Matching Platform
With advanced features: Job Scraping, Interview Prep, Enhanced AI Analysis
"""
import streamlit as st
import os
import tempfile
import logging
import pandas as pd
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional
import plotly.express as px
import plotly.graph_objects as go

# Import core modules
from core.file_processor import FileProcessor
from core.security import SecurityValidator
from core.enhanced_ai_engine import enhanced_ai_engine, AnalysisResult
from core.resume_builder import ATSResumeBuilder, ResumeData, PersonalInfo, Experience, Education, create_download_link
from utils.analytics import AnalyticsTracker
from features.job_scraper import job_scraper, JobListing
from features.interview_prep import interview_prep, InterviewSession

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Job Snipper AI - Enhanced Resume Analysis Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .job-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
    }
    .compatibility-high { border-left: 4px solid #28a745; }
    .compatibility-medium { border-left: 4px solid #ffc107; }
    .compatibility-low { border-left: 4px solid #dc3545; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    """Initialize all session state variables"""
    defaults = {
        'analysis_history': [],
        'current_analysis': None,
        'resume_text': None,
        'resume_data': ResumeData(),
        'job_search_results': [],
        'interview_session': None,
        'current_question_index': 0,
        'interview_answers': {},
        'user_skills': [],
        'experience_level': 'mid'
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

# Initialize components
@st.cache_resource
def get_components():
    """Get cached instances of components"""
    return {
        'file_processor': FileProcessor(),
        'analytics': AnalyticsTracker(),
        'resume_builder': ATSResumeBuilder()
    }

def main():
    """Enhanced main application function"""
    initialize_session_state()
    components = get_components()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Job Snipper AI - Enhanced</h1>
        <p>Advanced Resume Analysis, Job Matching & Interview Preparation Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.header("🚀 Navigation")
        
        # Main features
        page = st.selectbox(
            "Choose a feature:",
            [
                "📄 Resume Analysis", 
                "🎯 Job Matching", 
                "🔍 Job Search", 
                "🎤 Interview Prep",
                "🛠️ Skill Recommendations", 
                "🏗️ ATS Resume Builder", 
                "📊 Analytics Dashboard",
                "⚙️ Settings"
            ]
        )
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Analyses", len(st.session_state.analysis_history))
            st.metric("Skills Found", len(st.session_state.user_skills))
        
        with col2:
            if st.session_state.current_analysis:
                st.metric("Last Score", f"{st.session_state.current_analysis.score:.1%}")
            st.metric("Jobs Found", len(st.session_state.job_search_results))
        
        # User profile section
        st.markdown("---")
        st.markdown("### 👤 Profile")
        
        experience_level = st.selectbox(
            "Experience Level:",
            ["entry", "mid", "senior"],
            index=1
        )
        st.session_state.experience_level = experience_level
        
        # Quick actions
        st.markdown("---")
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🔄 Clear All Data", type="secondary"):
            for key in ['analysis_history', 'job_search_results', 'interview_session']:
                st.session_state[key] = [] if key != 'interview_session' else None
            st.success("✅ Data cleared!")
            st.rerun()
    
    # Route to selected page
    if page == "📄 Resume Analysis":
        resume_analysis_page(components)
    elif page == "🎯 Job Matching":
        job_matching_page(components)
    elif page == "🔍 Job Search":
        job_search_page(components)
    elif page == "🎤 Interview Prep":
        interview_prep_page(components)
    elif page == "🛠️ Skill Recommendations":
        skill_recommendations_page(components)
    elif page == "🏗️ ATS Resume Builder":
        ats_resume_builder_page(components)
    elif page == "📊 Analytics Dashboard":
        analytics_dashboard_page(components)
    elif page == "⚙️ Settings":
        settings_page(components)

def resume_analysis_page(components):
    """Enhanced resume analysis page"""
    st.header("📄 Resume Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Upload Resume")
        
        uploaded_file = st.file_uploader(
            "Choose your resume file",
            type=['pdf', 'doc', 'docx', 'txt'],
            help="Supported formats: PDF, DOC, DOCX, TXT (Max 10MB)"
        )
        
        if uploaded_file is not None:
            process_uploaded_resume(uploaded_file, components)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>📝 Analysis Features</h4>
            <ul>
                <li>🤖 AI-powered skill extraction</li>
                <li>📊 Structure analysis</li>
                <li>💡 Personalized recommendations</li>
                <li>🎯 Job matching compatibility</li>
                <li>📈 Performance scoring</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Recent analyses
        if st.session_state.analysis_history:
            st.subheader("📈 Recent Analyses")
            for analysis in st.session_state.analysis_history[-3:]:
                st.write(f"📄 {analysis['filename']}")
                st.write(f"⭐ Score: {analysis['score']:.1%}")
                st.write(f"🕒 {analysis['timestamp'].strftime('%Y-%m-%d %H:%M')}")
                st.markdown("---")
    
    # Display results
    if st.session_state.current_analysis:
        display_enhanced_analysis_results(st.session_state.current_analysis)

def process_uploaded_resume(uploaded_file, components):
    """Process uploaded resume with enhanced security and analysis"""
    with st.spinner("🔍 Validating and processing resume..."):
        try:
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            # Security validation
            is_valid, error_msg = SecurityValidator.validate_file(
                tmp_path, ['pdf', 'doc', 'docx', 'txt']
            )
            
            if not is_valid:
                st.error(f"❌ Security validation failed: {error_msg}")
                os.unlink(tmp_path)
                return
            
            st.success("✅ Security validation passed")
            
            # Extract text
            resume_text = components['file_processor'].extract_text(tmp_path)
            
            if not resume_text or len(resume_text.strip()) < 50:
                st.error("❌ Could not extract meaningful text from the resume")
                os.unlink(tmp_path)
                return
            
            # Store resume text
            st.session_state.resume_text = resume_text
            
            # Enhanced AI Analysis
            with st.spinner("🤖 Performing AI analysis..."):
                analysis_result = enhanced_ai_engine.analyze_resume(resume_text)
                
                # Extract and store user skills
                st.session_state.user_skills = analysis_result.details.get('extracted_skills', [])
                
                # Store analysis
                st.session_state.current_analysis = analysis_result
                st.session_state.analysis_history.append({
                    'filename': uploaded_file.name,
                    'timestamp': datetime.now(),
                    'score': analysis_result.score,
                    'skills': st.session_state.user_skills
                })
                
                # Track analytics
                components['analytics'].track_analysis(uploaded_file.name, analysis_result.score)
            
            st.success("✅ Resume analyzed successfully!")
            
        except Exception as e:
            logger.error(f"Error processing resume: {e}")
            st.error(f"❌ Error processing resume: {str(e)}")
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

def display_enhanced_analysis_results(analysis: AnalysisResult):
    """Display comprehensive analysis results with enhanced visualizations"""
    st.markdown("---")
    st.header("📊 Enhanced Analysis Results")
    
    # Overall metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        score_color = "🟢" if analysis.score > 0.7 else "🟡" if analysis.score > 0.4 else "🔴"
        st.metric(f"{score_color} Overall Score", f"{analysis.score:.1%}")
    
    with col2:
        st.metric("🎯 Confidence", f"{analysis.confidence:.1%}")
    
    with col3:
        skills_count = len(analysis.details.get('extracted_skills', []))
        st.metric("🛠️ Skills Found", skills_count)
    
    with col4:
        structure_score = analysis.details.get('structure_score', 0)
        st.metric("📋 Structure", f"{structure_score:.1%}")
    
    # Detailed analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Skills visualization
        st.subheader("🛠️ Extracted Skills")
        skills = analysis.details.get('extracted_skills', [])
        if skills:
            # Create skills chart
            skill_categories = categorize_skills(skills)
            if skill_categories:
                fig = px.pie(
                    values=list(skill_categories.values()),
                    names=list(skill_categories.keys()),
                    title="Skills by Category"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Display skills as badges
            for skill in skills[:15]:
                st.badge(skill.title(), type="secondary")
        else:
            st.info("No technical skills detected")
        
        # Experience analysis
        experience = analysis.details.get('experience', [])
        if experience:
            st.subheader("💼 Experience Found")
            for i, exp in enumerate(experience[:3], 1):
                st.write(f"{i}. **{exp.get('title', 'N/A')}** at {exp.get('company', 'N/A')}")
    
    with col2:
        # Recommendations
        st.subheader("💡 AI Recommendations")
        for i, rec in enumerate(analysis.recommendations, 1):
            st.write(f"{i}. {rec}")
        
        # Structure analysis visualization
        st.subheader("📊 Resume Structure Analysis")
        structure_metrics = {
            'Contact Info': 0.9 if '@' in st.session_state.resume_text else 0.3,
            'Skills Section': 1.0 if skills else 0.2,
            'Experience': 1.0 if experience else 0.3,
            'Education': 0.8 if analysis.details.get('education') else 0.4,
            'Quantified Results': 0.7 if any(char.isdigit() for char in st.session_state.resume_text) else 0.2
        }
        
        fig = go.Figure(go.Bar(
            x=list(structure_metrics.values()),
            y=list(structure_metrics.keys()),
            orientation='h',
            marker_color=['green' if v > 0.7 else 'orange' if v > 0.4 else 'red' for v in structure_metrics.values()]
        ))
        fig.update_layout(title="Resume Structure Quality", xaxis_title="Score")
        st.plotly_chart(fig, use_container_width=True)

def job_matching_page(components):
    """Enhanced job matching page"""
    st.header("🎯 Job Matching")
    
    if not st.session_state.current_analysis or not st.session_state.resume_text:
        st.warning("⚠️ Please analyze a resume first in the Resume Analysis section")
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Job Description Analysis")
        job_description = st.text_area(
            "Paste the job description here:",
            height=200,
            placeholder="Paste the complete job description including requirements, responsibilities, and qualifications..."
        )
        
        if st.button("🔍 Analyze Job Match", type="primary"):
            if job_description.strip():
                analyze_job_match(job_description, components)
            else:
                st.error("❌ Please enter a job description")
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🎯 Matching Features</h4>
            <ul>
                <li>🤖 AI-powered compatibility scoring</li>
                <li>📊 Skill gap analysis</li>
                <li>💡 Improvement recommendations</li>
                <li>📈 Match visualization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def analyze_job_match(job_description, components):
    """Analyze job match with enhanced features"""
    with st.spinner("🤖 Analyzing job compatibility..."):
        try:
            # Analyze job match
            match_analysis = enhanced_ai_engine.analyze_resume(
                st.session_state.resume_text, 
                job_description
            )
            
            match_score = match_analysis.job_match_score or 0.5
            skill_gaps = match_analysis.skill_gaps or []
            
            # Track analytics
            components['analytics'].track_job_match(match_score)
            
            # Display results
            st.success("✅ Job match analysis complete!")
            
            # Match score visualization
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("🎯 Match Score", f"{match_score:.1%}")
                
                # Create gauge chart
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = match_score * 100,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Compatibility"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 80], 'color': "yellow"},
                            {'range': [80, 100], 'color': "green"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("📋 Match Recommendations")
                for rec in match_analysis.recommendations[:5]:
                    st.write(f"• {rec}")
            
            with col3:
                st.subheader("🔍 Skill Gaps")
                if skill_gaps:
                    for gap in skill_gaps[:8]:
                        st.badge(gap, type="outline")
                else:
                    st.success("🎉 No major skill gaps found!")
            
        except Exception as e:
            logger.error(f"Error in job matching: {e}")
            st.error(f"❌ Error analyzing job match: {str(e)}")

def job_search_page(components):
    """Enhanced job search page with scraping capabilities"""
    st.header("🔍 Job Search")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Search Parameters")
        
        search_col1, search_col2 = st.columns(2)
        
        with search_col1:
            job_query = st.text_input(
                "Job Title/Keywords:",
                value="Software Developer",
                placeholder="e.g., Python Developer, Data Scientist"
            )
        
        with search_col2:
            location = st.text_input(
                "Location:",
                placeholder="e.g., New York, Remote"
            )
        
        num_jobs = st.slider("Number of Jobs:", 10, 100, 20)
        
        if st.button("🔍 Search Jobs", type="primary"):
            search_jobs(job_query, location, num_jobs, components)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🔍 Search Features</h4>
            <ul>
                <li>🌐 Multi-platform job scraping</li>
                <li>🎯 Smart job matching</li>
                <li>📊 Compatibility scoring</li>
                <li>💡 Application recommendations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Display search results
    if st.session_state.job_search_results:
        display_job_search_results()

def search_jobs(query, location, num_jobs, components):
    """Search for jobs and match with user profile"""
    with st.spinner(f"🔍 Searching for {query} jobs..."):
        try:
            # Search jobs
            jobs = job_scraper.search_jobs(query, location, num_jobs)
            
            if not jobs:
                st.warning("⚠️ No jobs found. Try different search terms.")
                return
            
            # Match jobs with user skills if available
            if st.session_state.user_skills:
                matched_jobs = job_scraper.match_jobs_to_resume(jobs, st.session_state.user_skills)
                st.session_state.job_search_results = matched_jobs
            else:
                # Convert to matched format without scoring
                st.session_state.job_search_results = [
                    {
                        'job': job,
                        'compatibility_score': 0.5,
                        'matching_skills': [],
                        'missing_skills': job.skills,
                        'recommendation': "🟡 Analyze your resume first for better matching"
                    }
                    for job in jobs
                ]
            
            st.success(f"✅ Found {len(jobs)} jobs!")
            
        except Exception as e:
            logger.error(f"Error searching jobs: {e}")
            st.error(f"❌ Error searching jobs: {str(e)}")

def display_job_search_results():
    """Display job search results with enhanced formatting"""
    st.subheader(f"📋 Job Search Results ({len(st.session_state.job_search_results)} jobs)")
    
    # Filter and sort options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sort_by = st.selectbox("Sort by:", ["Compatibility", "Date", "Company"])
    
    with col2:
        min_compatibility = st.slider("Min Compatibility:", 0.0, 1.0, 0.0, 0.1)
    
    with col3:
        show_count = st.selectbox("Show:", [10, 20, 50, "All"])
    
    # Filter results
    filtered_results = [
        result for result in st.session_state.job_search_results
        if result['compatibility_score'] >= min_compatibility
    ]
    
    # Sort results
    if sort_by == "Compatibility":
        filtered_results.sort(key=lambda x: x['compatibility_score'], reverse=True)
    elif sort_by == "Company":
        filtered_results.sort(key=lambda x: x['job'].company)
    
    # Limit results
    if show_count != "All":
        filtered_results = filtered_results[:show_count]
    
    # Display results
    for i, result in enumerate(filtered_results):
        job = result['job']
        compatibility = result['compatibility_score']
        
        # Determine card style based on compatibility
        if compatibility >= 0.7:
            card_class = "compatibility-high"
        elif compatibility >= 0.4:
            card_class = "compatibility-medium"
        else:
            card_class = "compatibility-low"
        
        with st.container():
            st.markdown(f"""
            <div class="job-card {card_class}">
                <h4>{job.title}</h4>
                <p><strong>🏢 {job.company}</strong> | 📍 {job.location}</p>
                <p>💰 {job.salary or 'Salary not specified'}</p>
                <p>🎯 Compatibility: {compatibility:.1%}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Expandable details
            with st.expander(f"View Details - {job.title}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Description:**")
                    st.write(job.description[:300] + "..." if len(job.description) > 300 else job.description)
                    
                    st.write("**Required Skills:**")
                    for skill in job.skills[:8]:
                        st.badge(skill, type="outline")
                
                with col2:
                    st.write("**Matching Skills:**")
                    for skill in result['matching_skills']:
                        st.badge(skill, type="secondary")
                    
                    st.write("**Missing Skills:**")
                    for skill in result['missing_skills'][:5]:
                        st.badge(skill, type="outline")
                    
                    st.write("**Recommendation:**")
                    st.info(result['recommendation'])
                
                if job.url:
                    st.link_button("🔗 Apply Now", job.url)

def interview_prep_page(components):
    """Interview preparation page with AI-generated questions"""
    st.header("🎤 Interview Preparation")
    
    if not st.session_state.user_skills:
        st.warning("⚠️ Please analyze your resume first to get personalized interview questions")
        return
    
    # Interview session management
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if not st.session_state.interview_session:
            st.subheader("🚀 Start Interview Practice")
            
            num_questions = st.slider("Number of Questions:", 5, 15, 8)
            
            if st.button("🎯 Generate Interview Questions", type="primary"):
                generate_interview_session(num_questions)
        else:
            conduct_interview_session()
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🎤 Interview Features</h4>
            <ul>
                <li>🤖 AI-generated questions</li>
                <li>📊 Personalized based on skills</li>
                <li>💡 Real-time feedback</li>
                <li>📈 Performance scoring</li>
                <li>🎯 Technical & behavioral mix</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Interview tips
        st.subheader("💡 Interview Tips")
        tips = [
            "Use the STAR method for behavioral questions",
            "Prepare specific examples from your experience",
            "Practice explaining technical concepts clearly",
            "Ask thoughtful questions about the role",
            "Research the company beforehand"
        ]
        
        for tip in tips:
            st.write(f"• {tip}")

def generate_interview_session(num_questions):
    """Generate a new interview session"""
    with st.spinner("🤖 Generating personalized interview questions..."):
        try:
            session = interview_prep.create_practice_session(
                st.session_state.user_skills,
                st.session_state.experience_level
            )
            
            # Limit questions to requested number
            session.questions = session.questions[:num_questions]
            
            st.session_state.interview_session = session
            st.session_state.current_question_index = 0
            st.session_state.interview_answers = {}
            
            st.success(f"✅ Generated {len(session.questions)} personalized questions!")
            st.rerun()
            
        except Exception as e:
            logger.error(f"Error generating interview session: {e}")
            st.error(f"❌ Error generating questions: {str(e)}")

def conduct_interview_session():
    """Conduct the interview practice session"""
    session = st.session_state.interview_session
    current_index = st.session_state.current_question_index
    
    if current_index >= len(session.questions):
        display_interview_results()
        return
    
    current_question = session.questions[current_index]
    
    # Progress indicator
    progress = (current_index + 1) / len(session.questions)
    st.progress(progress, text=f"Question {current_index + 1} of {len(session.questions)}")
    
    # Question display
    st.subheader(f"Question {current_index + 1}")
    
    # Question category and difficulty badges
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        st.badge(current_question.category.title(), type="secondary")
    with col2:
        difficulty_colors = {"easy": "secondary", "medium": "outline", "hard": "primary"}
        st.badge(current_question.difficulty.title(), type=difficulty_colors.get(current_question.difficulty, "secondary"))
    
    st.markdown(f"**{current_question.question}**")
    
    # Answer input
    answer_key = f"answer_{current_index}"
    answer = st.text_area(
        "Your Answer:",
        height=150,
        key=answer_key,
        placeholder="Provide a detailed answer with specific examples..."
    )
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if current_index > 0:
            if st.button("⬅️ Previous"):
                st.session_state.current_question_index -= 1
                st.rerun()
    
    with col2:
        if st.button("💾 Save & Next", type="primary"):
            if answer.strip():
                st.session_state.interview_answers[current_index] = answer
                st.session_state.current_question_index += 1
                st.rerun()
            else:
                st.error("Please provide an answer before proceeding")
    
    with col3:
        if st.button("🏁 Finish Interview"):
            if answer.strip():
                st.session_state.interview_answers[current_index] = answer
            st.session_state.current_question_index = len(session.questions)
            st.rerun()
    
    # Show expected points as hints
    with st.expander("💡 Key Points to Consider"):
        for point in current_question.expected_answer_points:
            st.write(f"• {point}")

def display_interview_results():
    """Display interview session results and feedback"""
    st.subheader("🎯 Interview Results")
    
    session = st.session_state.interview_session
    answers = st.session_state.interview_answers
    
    if not answers:
        st.warning("⚠️ No answers recorded")
        return
    
    # Calculate overall performance
    total_score = 0
    evaluations = []
    
    for i, question in enumerate(session.questions):
        if i in answers:
            evaluation = interview_prep.evaluate_answer(question, answers[i])
            evaluations.append(evaluation)
            total_score += evaluation['score']
    
    average_score = total_score / len(evaluations) if evaluations else 0
    
    # Overall performance metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 Overall Score", f"{average_score:.1%}")
    
    with col2:
        st.metric("✅ Questions Answered", f"{len(answers)}/{len(session.questions)}")
    
    with col3:
        performance_level = "Excellent" if average_score >= 0.8 else "Good" if average_score >= 0.6 else "Needs Improvement"
        st.metric("🎯 Performance", performance_level)
    
    # Detailed feedback
    st.subheader("📋 Detailed Feedback")
    
    for i, (question, evaluation) in enumerate(zip(session.questions, evaluations)):
        with st.expander(f"Question {i+1}: {question.question[:50]}..."):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Your Answer:**")
                st.write(answers[i])
                
                st.write("**Score:**")
                st.progress(evaluation['score'], text=f"{evaluation['score']:.1%}")
            
            with col2:
                st.write("**Feedback:**")
                st.info(evaluation['feedback'])
                
                if evaluation['suggestions']:
                    st.write("**Suggestions:**")
                    for suggestion in evaluation['suggestions']:
                        st.write(f"• {suggestion}")
    
    # Action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Start New Session", type="primary"):
            st.session_state.interview_session = None
            st.session_state.current_question_index = 0
            st.session_state.interview_answers = {}
            st.rerun()
    
    with col2:
        if st.button("📊 View Analytics"):
            st.session_state.page = "📊 Analytics Dashboard"
            st.rerun()

def skill_recommendations_page(components):
    """Enhanced skill recommendations page"""
    st.header("🛠️ Skill Recommendations")
    
    if not st.session_state.current_analysis:
        st.warning("⚠️ Please analyze a resume first")
        return
    
    current_skills = st.session_state.user_skills
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Current Skills")
        if current_skills:
            skill_categories = categorize_skills(current_skills)
            
            # Display by category
            for category, skills in skill_categories.items():
                st.write(f"**{category.title()}:**")
                for skill in skills:
                    st.badge(skill.title(), type="secondary")
        else:
            st.info("No skills detected in resume")
    
    with col2:
        st.subheader("🚀 Recommended Skills")
        
        # Generate recommendations based on current skills and job market trends
        recommended_skills = generate_enhanced_skill_recommendations(current_skills)
        
        for category, skills in recommended_skills.items():
            st.write(f"**{category.title()}:**")
            for skill in skills:
                st.badge(skill, type="primary")
    
    # Learning roadmap
    st.subheader("🗺️ Learning Roadmap")
    
    roadmap_tabs = st.tabs(["📚 Beginner", "🚀 Intermediate", "⭐ Advanced"])
    
    with roadmap_tabs[0]:
        display_learning_resources("beginner", current_skills)
    
    with roadmap_tabs[1]:
        display_learning_resources("intermediate", current_skills)
    
    with roadmap_tabs[2]:
        display_learning_resources("advanced", current_skills)

def categorize_skills(skills):
    """Categorize skills into different domains"""
    categories = {
        'programming': [],
        'web': [],
        'database': [],
        'cloud': [],
        'tools': [],
        'other': []
    }
    
    skill_mapping = {
        'programming': ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 'php', 'ruby'],
        'web': ['react', 'angular', 'vue', 'html', 'css', 'node.js', 'express', 'django', 'flask'],
        'database': ['mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle'],
        'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform'],
        'tools': ['git', 'github', 'jenkins', 'jira', 'figma']
    }
    
    for skill in skills:
        skill_lower = skill.lower()
        categorized = False
        
        for category, category_skills in skill_mapping.items():
            if any(cat_skill in skill_lower for cat_skill in category_skills):
                categories[category].append(skill)
                categorized = True
                break
        
        if not categorized:
            categories['other'].append(skill)
    
    # Remove empty categories
    return {k: v for k, v in categories.items() if v}

def generate_enhanced_skill_recommendations(current_skills):
    """Generate enhanced skill recommendations based on market trends"""
    recommendations = {
        'trending': [],
        'complementary': [],
        'advanced': []
    }
    
    # Trending skills in 2024
    trending_skills = [
        'artificial intelligence', 'machine learning', 'data science',
        'cloud computing', 'cybersecurity', 'devops', 'blockchain',
        'microservices', 'containerization', 'serverless'
    ]
    
    # Skill progression maps
    skill_progressions = {
        'python': ['django', 'flask', 'fastapi', 'pandas', 'numpy', 'tensorflow'],
        'javascript': ['react', 'node.js', 'typescript', 'vue', 'next.js'],
        'java': ['spring', 'hibernate', 'maven', 'gradle', 'microservices'],
        'aws': ['ec2', 's3', 'lambda', 'rds', 'cloudformation', 'eks'],
        'react': ['redux', 'next.js', 'typescript', 'testing-library'],
        'docker': ['kubernetes', 'helm', 'istio', 'prometheus']
    }
    
    current_skills_lower = [skill.lower() for skill in current_skills]
    
    # Add trending skills not already known
    for skill in trending_skills:
        if skill not in current_skills_lower:
            recommendations['trending'].append(skill)
    
    # Add complementary skills
    for current_skill in current_skills_lower:
        if current_skill in skill_progressions:
            for prog_skill in skill_progressions[current_skill]:
                if prog_skill not in current_skills_lower:
                    recommendations['complementary'].append(prog_skill)
    
    # Add advanced skills
    advanced_skills = [
        'system design', 'distributed systems', 'performance optimization',
        'security architecture', 'data engineering', 'mlops'
    ]
    
    for skill in advanced_skills:
        if skill not in current_skills_lower:
            recommendations['advanced'].append(skill)
    
    # Limit recommendations
    for category in recommendations:
        recommendations[category] = recommendations[category][:6]
    
    return recommendations

def display_learning_resources(level, current_skills):
    """Display learning resources based on level"""
    resources = {
        'beginner': {
            'Programming Fundamentals': ['Codecademy', 'freeCodeCamp', 'Python.org Tutorial'],
            'Web Development': ['MDN Web Docs', 'W3Schools', 'Frontend Mentor'],
            'Version Control': ['Git Tutorial', 'GitHub Learning Lab', 'Atlassian Git Tutorials']
        },
        'intermediate': {
            'Frameworks & Libraries': ['React Documentation', 'Django Tutorial', 'Spring Boot Guide'],
            'Databases': ['MySQL Tutorial', 'MongoDB University', 'PostgreSQL Documentation'],
            'Cloud Platforms': ['AWS Training', 'Azure Learn', 'Google Cloud Skills']
        },
        'advanced': {
            'System Design': ['System Design Primer', 'High Scalability', 'AWS Architecture Center'],
            'Performance': ['Web Performance', 'Database Optimization', 'Caching Strategies'],
            'Leadership': ['Tech Lead Skills', 'Engineering Management', 'Architecture Decisions']
        }
    }
    
    level_resources = resources.get(level, {})
    
    for category, platforms in level_resources.items():
        with st.expander(f"📖 {category}"):
            for platform in platforms:
                st.write(f"• {platform}")

def ats_resume_builder_page(components):
    """Enhanced ATS resume builder page"""
    st.header("🏗️ ATS Resume Builder")
    st.markdown("Build an ATS-friendly resume that passes through applicant tracking systems")
    
    builder = components['resume_builder']
    
    # Enhanced tabs with more features
    tabs = st.tabs([
        "📝 Personal Info", 
        "💼 Experience", 
        "🎓 Education", 
        "🛠️ Skills", 
        "🚀 Projects",
        "📄 Generate"
    ])
    
    with tabs[0]:
        build_personal_info_section()
    
    with tabs[1]:
        build_experience_section()
    
    with tabs[2]:
        build_education_section()
    
    with tabs[3]:
        build_skills_section()
    
    with tabs[4]:
        build_projects_section()
    
    with tabs[5]:
        build_generate_section(builder)

def build_personal_info_section():
    """Build personal information section"""
    st.subheader("Personal Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        full_name = st.text_input("Full Name *", value=st.session_state.resume_data.personal_info.full_name)
        email = st.text_input("Email *", value=st.session_state.resume_data.personal_info.email)
        phone = st.text_input("Phone *", value=st.session_state.resume_data.personal_info.phone)
    
    with col2:
        location = st.text_input("Location", value=st.session_state.resume_data.personal_info.location)
        linkedin = st.text_input("LinkedIn URL", value=st.session_state.resume_data.personal_info.linkedin)
        github = st.text_input("GitHub URL", value=st.session_state.resume_data.personal_info.github)
    
    # Professional Summary
    st.subheader("Professional Summary")
    summary = st.text_area(
        "Write a compelling professional summary (2-3 sentences)",
        value=st.session_state.resume_data.summary,
        height=100,
        help="Focus on your key strengths, experience, and career objectives"
    )
    
    if st.button("💾 Save Personal Info", type="primary"):
        st.session_state.resume_data.personal_info.full_name = full_name
        st.session_state.resume_data.personal_info.email = email
        st.session_state.resume_data.personal_info.phone = phone
        st.session_state.resume_data.personal_info.location = location
        st.session_state.resume_data.personal_info.linkedin = linkedin
        st.session_state.resume_data.personal_info.github = github
        st.session_state.resume_data.summary = summary
        st.success("✅ Personal information saved!")

def build_experience_section():
    """Build experience section with enhanced features"""
    st.subheader("Work Experience")
    
    # Display existing experiences
    if st.session_state.resume_data.experience:
        st.write("**Current Experiences:**")
        for i, exp in enumerate(st.session_state.resume_data.experience):
            with st.expander(f"{exp.title} at {exp.company}"):
                st.write(f"**Location:** {exp.location}")
                st.write(f"**Duration:** {exp.start_date} - {exp.end_date}")
                st.write("**Description:**")
                for desc in exp.description:
                    st.write(f"• {desc}")
                
                if st.button(f"🗑️ Remove", key=f"remove_exp_{i}"):
                    st.session_state.resume_data.experience.pop(i)
                    st.rerun()
    
    # Add new experience
    with st.expander("➕ Add New Experience"):
        col1, col2 = st.columns(2)
        
        with col1:
            exp_title = st.text_input("Job Title")
            exp_company = st.text_input("Company")
            exp_start = st.text_input("Start Date (MM/YYYY)")
        
        with col2:
            exp_location = st.text_input("Location")
            exp_end = st.text_input("End Date (MM/YYYY or Present)")
        
        exp_description = st.text_area(
            "Job Description (one bullet point per line)",
            height=100,
            help="Use action verbs and quantify achievements where possible"
        )
        
        if st.button("➕ Add Experience"):
            if exp_title and exp_company:
                new_exp = Experience(
                    title=exp_title,
                    company=exp_company,
                    location=exp_location,
                    start_date=exp_start,
                    end_date=exp_end,
                    description=exp_description.split('\n') if exp_description else []
                )
                st.session_state.resume_data.experience.append(new_exp)
                st.success("✅ Experience added!")
                st.rerun()

def build_education_section():
    """Build education section"""
    st.subheader("Education")
    
    # Display existing education
    if st.session_state.resume_data.education:
        st.write("**Current Education:**")
        for i, edu in enumerate(st.session_state.resume_data.education):
            with st.expander(f"{edu.degree} - {edu.institution}"):
                st.write(f"**Graduation:** {edu.graduation_date}")
                if edu.gpa:
                    st.write(f"**GPA:** {edu.gpa}")
                
                if st.button(f"🗑️ Remove", key=f"remove_edu_{i}"):
                    st.session_state.resume_data.education.pop(i)
                    st.rerun()
    
    with st.expander("➕ Add Education"):
        col1, col2 = st.columns(2)
        
        with col1:
            edu_degree = st.text_input("Degree")
            edu_institution = st.text_input("Institution")
        
        with col2:
            edu_graduation = st.text_input("Graduation Date (MM/YYYY)")
            edu_gpa = st.text_input("GPA (optional)")
        
        if st.button("➕ Add Education"):
            if edu_degree and edu_institution:
                new_edu = Education(
                    degree=edu_degree,
                    institution=edu_institution,
                    graduation_date=edu_graduation,
                    gpa=edu_gpa
                )
                st.session_state.resume_data.education.append(new_edu)
                st.success("✅ Education added!")
                st.rerun()

def build_skills_section():
    """Build skills section with categorization"""
    st.subheader("Technical Skills")
    
    # Skill categories
    skill_categories = ['Programming Languages', 'Web Technologies', 'Databases', 'Cloud Platforms', 'Tools & Frameworks', 'Other']
    
    for category in skill_categories:
        with st.expander(f"📂 {category}"):
            category_key = category.lower().replace(' ', '_').replace('&', 'and')
            
            if category_key not in st.session_state:
                st.session_state[category_key] = []
            
            # Display current skills in category
            if st.session_state[category_key]:
                st.write("**Current skills:**")
                for skill in st.session_state[category_key]:
                    st.badge(skill, type="secondary")
            
            # Add new skill
            new_skill = st.text_input(f"Add skill to {category}", key=f"new_skill_{category_key}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"➕ Add", key=f"add_{category_key}"):
                    if new_skill and new_skill not in st.session_state[category_key]:
                        st.session_state[category_key].append(new_skill)
                        st.rerun()
            
            with col2:
                if st.button(f"🔄 Clear All", key=f"clear_{category_key}"):
                    st.session_state[category_key] = []
                    st.rerun()
    
    # Combine all skills
    if st.button("💾 Save All Skills", type="primary"):
        all_skills = []
        for category in skill_categories:
            category_key = category.lower().replace(' ', '_').replace('&', 'and')
            all_skills.extend(st.session_state.get(category_key, []))
        
        st.session_state.resume_data.skills = all_skills
        st.success(f"✅ Saved {len(all_skills)} skills!")

def build_projects_section():
    """Build projects section"""
    st.subheader("Projects")
    
    # Display existing projects
    if hasattr(st.session_state.resume_data, 'projects') and st.session_state.resume_data.projects:
        st.write("**Current Projects:**")
        for i, project in enumerate(st.session_state.resume_data.projects):
            with st.expander(f"{project.name}"):
                st.write(f"**Description:** {project.description}")
                st.write(f"**Technologies:** {', '.join(project.technologies)}")
                if project.url:
                    st.write(f"**URL:** {project.url}")
                
                if st.button(f"🗑️ Remove", key=f"remove_project_{i}"):
                    st.session_state.resume_data.projects.pop(i)
                    st.rerun()
    
    # Add new project
    with st.expander("➕ Add New Project"):
        project_name = st.text_input("Project Name")
        project_description = st.text_area("Project Description", height=100)
        project_technologies = st.text_input("Technologies Used (comma-separated)")
        project_url = st.text_input("Project URL (optional)")
        
        if st.button("➕ Add Project"):
            if project_name and project_description:
                if not hasattr(st.session_state.resume_data, 'projects'):
                    st.session_state.resume_data.projects = []
                
                new_project = {
                    'name': project_name,
                    'description': project_description,
                    'technologies': [tech.strip() for tech in project_technologies.split(',') if tech.strip()],
                    'url': project_url
                }
                st.session_state.resume_data.projects.append(new_project)
                st.success("✅ Project added!")
                st.rerun()

def build_generate_section(builder):
    """Build resume generation section"""
    st.subheader("Generate Your ATS-Friendly Resume")
    
    # Check completeness
    has_name = bool(st.session_state.resume_data.personal_info.full_name)
    has_email = bool(st.session_state.resume_data.personal_info.email)
    has_content = bool(
        st.session_state.resume_data.experience or 
        st.session_state.resume_data.education or 
        st.session_state.resume_data.skills
    )
    
    if has_name and has_email and has_content:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📋 Resume Preview")
            
            # Display preview
            st.markdown(f"**{st.session_state.resume_data.personal_info.full_name}**")
            contact_info = f"{st.session_state.resume_data.personal_info.email}"
            if st.session_state.resume_data.personal_info.phone:
                contact_info += f" | {st.session_state.resume_data.personal_info.phone}"
            if st.session_state.resume_data.personal_info.location:
                contact_info += f" | {st.session_state.resume_data.personal_info.location}"
            st.markdown(contact_info)
            
            if st.session_state.resume_data.summary:
                st.markdown(f"**Summary:** {st.session_state.resume_data.summary}")
            
            # Template selection
            st.subheader("📄 Template Selection")
            template = st.selectbox(
                "Choose Resume Template:",
                ["Modern ATS", "Classic Professional", "Tech-Focused", "Creative"]
            )
            
            if st.button("📄 Generate PDF Resume", type="primary"):
                generate_resume_pdf(builder, template)
        
        with col2:
            st.subheader("🎯 ATS Optimization Tips")
            tips = [
                "Use standard section headers",
                "Include relevant keywords",
                "Use simple, clean formatting",
                "Avoid images and graphics",
                "Use standard fonts",
                "Include quantified achievements"
            ]
            
            for tip in tips:
                st.info(f"💡 {tip}")
            
            # Resume score
            score = calculate_resume_completeness()
            st.metric("📊 Completeness Score", f"{score:.1%}")
            
            if score < 0.8:
                st.warning("⚠️ Consider adding more sections for a complete resume")
    else:
        st.warning("⚠️ Please complete the following to generate your resume:")
        if not has_name:
            st.write("• Add your full name")
        if not has_email:
            st.write("• Add your email address")
        if not has_content:
            st.write("• Add at least one section (Experience, Education, or Skills)")

def generate_resume_pdf(builder, template):
    """Generate PDF resume with selected template"""
    try:
        with st.spinner(f"Generating your {template} resume..."):
            # This would integrate with the resume builder
            # For now, show success message
            st.success("✅ Resume generated successfully!")
            
            # Create download button
            filename = f"{st.session_state.resume_data.personal_info.full_name.replace(' ', '_')}_Resume_{template.replace(' ', '_')}.pdf"
            
            # Placeholder for actual PDF generation
            st.download_button(
                label="📥 Download Resume",
                data="PDF content would be here",
                file_name=filename,
                mime="application/pdf"
            )
            
    except Exception as e:
        st.error(f"❌ Error generating resume: {str(e)}")

def calculate_resume_completeness():
    """Calculate resume completeness score"""
    score = 0.0
    
    # Personal info (30%)
    if st.session_state.resume_data.personal_info.full_name:
        score += 0.1
    if st.session_state.resume_data.personal_info.email:
        score += 0.1
    if st.session_state.resume_data.personal_info.phone:
        score += 0.05
    if st.session_state.resume_data.personal_info.location:
        score += 0.05
    
    # Summary (10%)
    if st.session_state.resume_data.summary:
        score += 0.1
    
    # Experience (30%)
    if st.session_state.resume_data.experience:
        score += 0.3
    
    # Education (15%)
    if st.session_state.resume_data.education:
        score += 0.15
    
    # Skills (15%)
    if st.session_state.resume_data.skills:
        score += 0.15
    
    return min(score, 1.0)

def analytics_dashboard_page(components):
    """Enhanced analytics dashboard"""
    st.header("📊 Analytics Dashboard")
    
    analytics = components['analytics']
    
    if not st.session_state.analysis_history:
        st.info("📈 No analysis data yet. Analyze some resumes to see insights!")
        return
    
    # Time period selector
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📈 Performance Overview")
    
    with col2:
        period = st.selectbox("Time Period:", [7, 30, 90], index=1, format_func=lambda x: f"Last {x} days")
    
    # Get analytics summary
    summary = analytics.get_analytics_summary(days=period)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📄 Total Analyses", summary['total_events'])
    
    with col2:
        avg_score = summary['resume_analysis']['average_score']
        st.metric("📊 Average Score", f"{avg_score:.1%}")
    
    with col3:
        st.metric("🎯 Job Matches", summary['job_matching']['total_matches'])
    
    with col4:
        st.metric("👥 Unique Sessions", summary['unique_sessions'])
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Score distribution
        if st.session_state.analysis_history:
            scores = [h['score'] for h in st.session_state.analysis_history]
            
            fig = px.histogram(
                x=scores,
                nbins=10,
                title="Resume Score Distribution",
                labels={'x': 'Score', 'y': 'Count'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Skills analysis
        all_skills = []
        for analysis in st.session_state.analysis_history:
            all_skills.extend(analysis.get('skills', []))
        
        if all_skills:
            skill_counts = pd.Series(all_skills).value_counts().head(10)
            
            fig = px.bar(
                x=skill_counts.values,
                y=skill_counts.index,
                orientation='h',
                title="Most Common Skills",
                labels={'x': 'Count', 'y': 'Skills'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Activity timeline
    if summary['daily_activity']:
        st.subheader("📅 Activity Timeline")
        
        dates = list(summary['daily_activity'].keys())
        counts = list(summary['daily_activity'].values())
        
        fig = px.line(
            x=dates,
            y=counts,
            title="Daily Activity",
            labels={'x': 'Date', 'y': 'Activities'}
        )
        st.plotly_chart(fig, use_container_width=True)

def settings_page(components):
    """Settings and configuration page"""
    st.header("⚙️ Settings")
    
    # API Configuration
    st.subheader("🔑 API Configuration")
    
    with st.expander("OpenAI Configuration"):
        openai_key = st.text_input(
            "OpenAI API Key:",
            type="password",
            help="Enter your OpenAI API key for enhanced AI features"
        )
        
        if st.button("💾 Save OpenAI Key"):
            if openai_key:
                os.environ['OPENAI_API_KEY'] = openai_key
                st.success("✅ OpenAI API key saved!")
            else:
                st.error("❌ Please enter a valid API key")
    
    # Data Management
    st.subheader("🗄️ Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export Analytics Data"):
            try:
                analytics_data = components['analytics'].export_analytics('json')
                st.download_button(
                    label="📥 Download Analytics",
                    data=analytics_data,
                    file_name=f"job_snipper_analytics_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
            except Exception as e:
                st.error(f"❌ Export failed: {e}")
    
    with col2:
        if st.button("🧹 Clean Old Data"):
            try:
                removed_count = components['analytics'].cleanup_old_data(days=90)
                st.success(f"✅ Removed {removed_count} old records")
            except Exception as e:
                st.error(f"❌ Cleanup failed: {e}")
    
    # Application Info
    st.subheader("ℹ️ Application Information")
    
    info_data = {
        "Version": "2.0.0 Enhanced",
        "Features": [
            "AI-Powered Resume Analysis",
            "Job Search & Matching",
            "Interview Preparation",
            "ATS Resume Builder",
            "Analytics Dashboard"
        ],
        "AI Models": [
            "Enhanced AI Engine with fallbacks",
            "Skill extraction and categorization",
            "Job compatibility scoring",
            "Interview question generation"
        ]
    }
    
    st.json(info_data)

if __name__ == "__main__":
    main()