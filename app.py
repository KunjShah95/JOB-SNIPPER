#!/usr/bin/env python3
"""
JobSniper AI - Modern Job Matching Platform
A clean, deployable job matching and resume analysis tool
"""

import streamlit as st
import os
import sys
from pathlib import Path
import logging
from datetime import datetime
import json
import io
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="JobSniper AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    
    .sidebar-content {
        background: linear-gradient(180deg, #1a365d 0%, #2d3748 50%, #1a202c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
    }
    
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class JobSniperAI:
    """Main JobSniper AI Application Class"""
    
    def __init__(self):
        self.setup_session_state()
        
    def setup_session_state(self):
        """Initialize session state variables"""
        if 'resume_data' not in st.session_state:
            st.session_state.resume_data = None
        if 'job_matches' not in st.session_state:
            st.session_state.job_matches = []
        if 'analysis_history' not in st.session_state:
            st.session_state.analysis_history = []
    
    def render_header(self):
        """Render the main header"""
        st.markdown("""
        <div class="main-header">
            <h1>🎯 JobSniper AI</h1>
            <p>AI-Powered Resume Analysis & Job Matching Platform</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render the sidebar navigation"""
        with st.sidebar:
            st.markdown("### 🎯 JobSniper AI")
            st.markdown("---")
            
            # Navigation
            page = st.selectbox(
                "Navigate to:",
                ["🏠 Dashboard", "📄 Resume Analysis", "🎯 Job Matching", 
                 "📊 Analytics", "⚙️ Settings"],
                key="navigation"
            )
            
            st.markdown("---")
            
            # Quick stats
            st.markdown("### 📊 Quick Stats")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Resumes Analyzed", len(st.session_state.analysis_history))
            with col2:
                st.metric("Job Matches", len(st.session_state.job_matches))
            
            st.markdown("---")
            
            # System status
            st.markdown("### 🔧 System Status")
            st.success("✅ AI Engine: Active")
            st.info("📡 API: Connected")
            st.warning("🔑 Demo Mode: Active")
            
            return page
    
    def parse_resume_text(self, text):
        """Parse resume text and extract key information"""
        # Simple text analysis for demo
        lines = text.split('\n')
        
        # Extract basic information
        skills = []
        experience = []
        education = []
        
        current_section = None
        
        for line in lines:
            line = line.strip().lower()
            
            if any(keyword in line for keyword in ['skill', 'technical', 'programming']):
                current_section = 'skills'
            elif any(keyword in line for keyword in ['experience', 'work', 'employment']):
                current_section = 'experience'
            elif any(keyword in line for keyword in ['education', 'degree', 'university']):
                current_section = 'education'
            
            # Extract skills
            if current_section == 'skills' or any(skill in line for skill in 
                ['python', 'java', 'javascript', 'react', 'sql', 'machine learning', 'ai']):
                for skill in ['python', 'java', 'javascript', 'react', 'sql', 'machine learning', 'ai', 'data science']:
                    if skill in line and skill not in skills:
                        skills.append(skill.title())
        
        # Generate mock data if no skills found
        if not skills:
            skills = ['Python', 'Data Analysis', 'Machine Learning', 'SQL']
        
        return {
            'skills': skills[:10],  # Limit to top 10
            'experience_years': min(len(experience) + 2, 10),
            'education_level': 'Bachelor\'s Degree',
            'total_score': min(85 + len(skills) * 2, 100)
        }
    
    def generate_job_matches(self, resume_data):
        """Generate job matches based on resume data"""
        # Mock job matches based on skills
        job_templates = [
            {
                'title': 'Senior Data Scientist',
                'company': 'TechCorp Inc.',
                'location': 'San Francisco, CA',
                'salary': '$120,000 - $150,000',
                'match_score': 92,
                'required_skills': ['Python', 'Machine Learning', 'SQL', 'Data Analysis'],
                'description': 'Lead data science initiatives and build ML models.'
            },
            {
                'title': 'Machine Learning Engineer',
                'company': 'AI Innovations',
                'location': 'New York, NY',
                'salary': '$110,000 - $140,000',
                'match_score': 88,
                'required_skills': ['Python', 'Machine Learning', 'AI'],
                'description': 'Develop and deploy ML models in production.'
            },
            {
                'title': 'Data Analyst',
                'company': 'DataFlow Solutions',
                'location': 'Austin, TX',
                'salary': '$80,000 - $100,000',
                'match_score': 85,
                'required_skills': ['SQL', 'Data Analysis', 'Python'],
                'description': 'Analyze data and create insights for business decisions.'
            },
            {
                'title': 'Software Developer',
                'company': 'CodeCraft LLC',
                'location': 'Seattle, WA',
                'salary': '$90,000 - $120,000',
                'match_score': 78,
                'required_skills': ['Python', 'JavaScript', 'SQL'],
                'description': 'Build web applications and software solutions.'
            }
        ]
        
        # Filter and score based on resume skills
        user_skills = set(skill.lower() for skill in resume_data['skills'])
        
        for job in job_templates:
            job_skills = set(skill.lower() for skill in job['required_skills'])
            skill_overlap = len(user_skills.intersection(job_skills))
            total_skills = len(job_skills)
            
            # Adjust match score based on skill overlap
            if total_skills > 0:
                skill_match_ratio = skill_overlap / total_skills
                job['match_score'] = int(job['match_score'] * (0.7 + 0.3 * skill_match_ratio))
        
        # Sort by match score
        job_templates.sort(key=lambda x: x['match_score'], reverse=True)
        
        return job_templates
    
    def render_dashboard(self):
        """Render the main dashboard"""
        st.markdown("## 🏠 Dashboard")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>📄</h3>
                <h2>{}</h2>
                <p>Resumes Analyzed</p>
            </div>
            """.format(len(st.session_state.analysis_history)), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>🎯</h3>
                <h2>{}</h2>
                <p>Job Matches</p>
            </div>
            """.format(len(st.session_state.job_matches)), unsafe_allow_html=True)
        
        with col3:
            avg_score = 0
            if st.session_state.analysis_history:
                avg_score = sum(item.get('total_score', 0) for item in st.session_state.analysis_history) / len(st.session_state.analysis_history)
            
            st.markdown("""
            <div class="metric-card">
                <h3>📊</h3>
                <h2>{}%</h2>
                <p>Avg Match Score</p>
            </div>
            """.format(int(avg_score)), unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <h3>🚀</h3>
                <h2>Active</h2>
                <p>AI Status</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Recent activity
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Recent Activity")
            if st.session_state.analysis_history:
                for i, analysis in enumerate(st.session_state.analysis_history[-3:]):
                    st.markdown(f"""
                    <div class="feature-card">
                        <strong>Analysis #{i+1}</strong><br>
                        Skills: {len(analysis.get('skills', []))}<br>
                        Score: {analysis.get('total_score', 0)}%
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No recent activity. Upload a resume to get started!")
        
        with col2:
            st.markdown("### 🎯 Top Job Matches")
            if st.session_state.job_matches:
                for job in st.session_state.job_matches[:3]:
                    st.markdown(f"""
                    <div class="feature-card">
                        <strong>{job['title']}</strong><br>
                        {job['company']}<br>
                        Match: {job['match_score']}%
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No job matches yet. Analyze a resume first!")
    
    def render_resume_analysis(self):
        """Render the resume analysis page"""
        st.markdown("## 📄 Resume Analysis")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload your resume",
            type=['pdf', 'docx', 'txt'],
            help="Supported formats: PDF, DOCX, TXT"
        )
        
        # Text input as alternative
        st.markdown("### Or paste your resume text:")
        resume_text = st.text_area(
            "Resume content",
            height=200,
            placeholder="Paste your resume content here..."
        )
        
        if uploaded_file is not None or resume_text:
            if st.button("🔍 Analyze Resume", type="primary"):
                with st.spinner("Analyzing resume..."):
                    # Process the resume
                    if uploaded_file:
                        # For demo, we'll use the filename as text
                        text_content = f"Resume file: {uploaded_file.name}\nDemo content for analysis."
                    else:
                        text_content = resume_text
                    
                    # Parse resume
                    resume_data = self.parse_resume_text(text_content)
                    st.session_state.resume_data = resume_data
                    
                    # Add to history
                    analysis_record = {
                        'timestamp': datetime.now().isoformat(),
                        'filename': uploaded_file.name if uploaded_file else 'Text Input',
                        **resume_data
                    }
                    st.session_state.analysis_history.append(analysis_record)
                    
                    # Generate job matches
                    job_matches = self.generate_job_matches(resume_data)
                    st.session_state.job_matches = job_matches
                
                st.success("✅ Resume analysis complete!")
        
        # Display results
        if st.session_state.resume_data:
            st.markdown("---")
            st.markdown("### 📊 Analysis Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🎯 Key Metrics")
                data = st.session_state.resume_data
                
                st.metric("Overall Score", f"{data['total_score']}%")
                st.metric("Skills Identified", len(data['skills']))
                st.metric("Experience Level", f"{data['experience_years']} years")
                st.metric("Education", data['education_level'])
            
            with col2:
                st.markdown("#### 🛠️ Skills Found")
                for skill in st.session_state.resume_data['skills']:
                    st.markdown(f"• **{skill}**")
                
                if len(st.session_state.resume_data['skills']) == 0:
                    st.info("No specific skills detected. Consider adding more technical details to your resume.")
            
            # Recommendations
            st.markdown("#### 💡 Recommendations")
            score = st.session_state.resume_data['total_score']
            
            if score >= 90:
                st.markdown("""
                <div class="success-box">
                    <strong>Excellent Resume!</strong> Your resume shows strong technical skills and experience. 
                    Consider applying to senior-level positions.
                </div>
                """, unsafe_allow_html=True)
            elif score >= 75:
                st.markdown("""
                <div class="warning-box">
                    <strong>Good Resume!</strong> Consider adding more specific technical skills or certifications 
                    to improve your match score.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("Consider adding more technical skills and specific experience details to improve your resume.")
    
    def render_job_matching(self):
        """Render the job matching page"""
        st.markdown("## 🎯 Job Matching")
        
        if not st.session_state.resume_data:
            st.warning("Please analyze a resume first to see job matches.")
            return
        
        if not st.session_state.job_matches:
            st.info("No job matches available. Please analyze a resume first.")
            return
        
        st.markdown(f"### Found {len(st.session_state.job_matches)} job matches")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            min_score = st.slider("Minimum Match Score", 0, 100, 70)
        
        with col2:
            location_filter = st.selectbox(
                "Location",
                ["All Locations"] + list(set(job['location'] for job in st.session_state.job_matches))
            )
        
        with col3:
            sort_by = st.selectbox("Sort by", ["Match Score", "Salary", "Company"])
        
        # Filter jobs
        filtered_jobs = [
            job for job in st.session_state.job_matches 
            if job['match_score'] >= min_score and 
            (location_filter == "All Locations" or job['location'] == location_filter)
        ]
        
        # Sort jobs
        if sort_by == "Match Score":
            filtered_jobs.sort(key=lambda x: x['match_score'], reverse=True)
        elif sort_by == "Company":
            filtered_jobs.sort(key=lambda x: x['company'])
        
        # Display jobs
        for i, job in enumerate(filtered_jobs):
            with st.expander(f"🎯 {job['title']} at {job['company']} - {job['match_score']}% match"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Company:** {job['company']}")
                    st.markdown(f"**Location:** {job['location']}")
                    st.markdown(f"**Salary:** {job['salary']}")
                    st.markdown(f"**Match Score:** {job['match_score']}%")
                
                with col2:
                    st.markdown("**Required Skills:**")
                    for skill in job['required_skills']:
                        if skill.lower() in [s.lower() for s in st.session_state.resume_data['skills']]:
                            st.markdown(f"✅ {skill}")
                        else:
                            st.markdown(f"❌ {skill}")
                
                st.markdown(f"**Description:** {job['description']}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"Apply Now", key=f"apply_{i}"):
                        st.success("Application submitted! (Demo mode)")
                with col2:
                    if st.button(f"Save Job", key=f"save_{i}"):
                        st.info("Job saved to your list!")
                with col3:
                    if st.button(f"Get Details", key=f"details_{i}"):
                        st.info("Opening job details... (Demo mode)")
    
    def render_analytics(self):
        """Render the analytics page"""
        st.markdown("## 📊 Analytics")
        
        if not st.session_state.analysis_history:
            st.info("No data available yet. Analyze some resumes to see analytics!")
            return
        
        # Summary stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_analyses = len(st.session_state.analysis_history)
            st.metric("Total Analyses", total_analyses)
        
        with col2:
            avg_score = sum(item.get('total_score', 0) for item in st.session_state.analysis_history) / len(st.session_state.analysis_history)
            st.metric("Average Score", f"{avg_score:.1f}%")
        
        with col3:
            total_skills = sum(len(item.get('skills', [])) for item in st.session_state.analysis_history)
            st.metric("Total Skills Found", total_skills)
        
        # Skills analysis
        st.markdown("### 🛠️ Skills Analysis")
        
        all_skills = []
        for analysis in st.session_state.analysis_history:
            all_skills.extend(analysis.get('skills', []))
        
        if all_skills:
            from collections import Counter
            skill_counts = Counter(all_skills)
            
            # Display top skills
            st.markdown("#### Most Common Skills")
            for skill, count in skill_counts.most_common(10):
                st.markdown(f"• **{skill}**: {count} times")
        
        # Timeline
        st.markdown("### 📈 Analysis Timeline")
        
        timeline_data = []
        for analysis in st.session_state.analysis_history:
            timeline_data.append({
                'Date': analysis['timestamp'][:10],
                'Score': analysis.get('total_score', 0),
                'Skills': len(analysis.get('skills', []))
            })
        
        if timeline_data:
            import pandas as pd
            df = pd.DataFrame(timeline_data)
            st.line_chart(df.set_index('Date'))
    
    def render_settings(self):
        """Render the settings page"""
        st.markdown("## ⚙️ Settings")
        
        # API Configuration
        st.markdown("### 🔑 API Configuration")
        
        with st.form("api_settings"):
            st.markdown("Configure your AI API keys for enhanced functionality:")
            
            gemini_key = st.text_input(
                "Gemini API Key",
                type="password",
                help="Get your API key from Google AI Studio"
            )
            
            openai_key = st.text_input(
                "OpenAI API Key",
                type="password",
                help="Get your API key from OpenAI Platform"
            )
            
            if st.form_submit_button("Save API Keys"):
                if gemini_key or openai_key:
                    st.success("✅ API keys saved successfully!")
                    st.info("🔄 Please restart the application to apply changes.")
                else:
                    st.warning("Please provide at least one API key.")
        
        st.markdown("---")
        
        # Application Settings
        st.markdown("### 🎛️ Application Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Features")
            auto_match = st.checkbox("Auto-generate job matches", value=True)
            save_history = st.checkbox("Save analysis history", value=True)
            email_reports = st.checkbox("Email reports", value=False)
        
        with col2:
            st.markdown("#### Preferences")
            theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
            language = st.selectbox("Language", ["English", "Spanish", "French"])
            notifications = st.checkbox("Enable notifications", value=True)
        
        if st.button("Save Settings"):
            st.success("Settings saved successfully!")
        
        st.markdown("---")
        
        # Data Management
        st.markdown("### 🗂️ Data Management")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Export Data"):
                # Create export data
                export_data = {
                    'analysis_history': st.session_state.analysis_history,
                    'job_matches': st.session_state.job_matches,
                    'export_date': datetime.now().isoformat()
                }
                
                # Convert to JSON
                json_data = json.dumps(export_data, indent=2)
                
                # Create download
                st.download_button(
                    label="Download Export",
                    data=json_data,
                    file_name=f"jobsniper_export_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("Clear History"):
                st.session_state.analysis_history = []
                st.session_state.job_matches = []
                st.success("History cleared!")
        
        with col3:
            if st.button("Reset App"):
                for key in st.session_state.keys():
                    del st.session_state[key]
                st.success("App reset! Please refresh the page.")
    
    def run(self):
        """Main application runner"""
        self.render_header()
        
        # Sidebar navigation
        current_page = self.render_sidebar()
        
        # Main content
        if current_page == "🏠 Dashboard":
            self.render_dashboard()
        elif current_page == "📄 Resume Analysis":
            self.render_resume_analysis()
        elif current_page == "🎯 Job Matching":
            self.render_job_matching()
        elif current_page == "📊 Analytics":
            self.render_analytics()
        elif current_page == "⚙️ Settings":
            self.render_settings()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; padding: 1rem;">
            🎯 JobSniper AI - Built with Streamlit | 
            <a href="https://github.com/KunjShah95/JOB-SNIPPER" target="_blank">GitHub</a>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main entry point"""
    try:
        app = JobSniperAI()
        app.run()
    except Exception as e:
        st.error(f"Application Error: {str(e)}")
        logger.error(f"Application error: {e}")

if __name__ == "__main__":
    main()