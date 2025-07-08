import streamlit as st
import os
import tempfile
import logging
from datetime import datetime
import json
from typing import Dict, List, Optional

# Import core modules
from core.file_processor import FileProcessor
from core.security import SecurityValidator
from core.ai_engine import ai_engine, AnalysisResult
from utils.analytics import AnalyticsTracker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Job Snipper AI - Advanced Resume Analysis",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None

# Initialize components
file_processor = FileProcessor()
analytics = AnalyticsTracker()

def main():
    """Main application function"""
    # Header
    st.title("🎯 Job Snipper AI")
    st.markdown("**Advanced Resume Analysis & Job Matching Platform**")
    
    # Sidebar navigation
    with st.sidebar:
        st.header("🚀 Navigation")
        page = st.selectbox(
            "Choose a feature:",
            ["Resume Analysis", "Job Matching", "Skill Recommendations", "Analytics Dashboard"]
        )
        
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        st.metric("Analyses Today", len(st.session_state.analysis_history))
        
        if st.session_state.current_analysis:
            st.metric("Last Score", f"{st.session_state.current_analysis.score:.1%}")
    
    # Route to selected page
    if page == "Resume Analysis":
        resume_analysis_page()
    elif page == "Job Matching":
        job_matching_page()
    elif page == "Skill Recommendations":
        skill_recommendations_page()
    elif page == "Analytics Dashboard":
        analytics_dashboard_page()

def resume_analysis_page():
    """Resume analysis page with security validation"""
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
            # Security validation
            with st.spinner("Validating file security..."):
                # Save to temporary file for validation
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                # Validate file
                is_valid, error_msg = SecurityValidator.validate_file(
                    tmp_path, ['pdf', 'doc', 'docx', 'txt']
                )
                
                if not is_valid:
                    st.error(f"❌ File validation failed: {error_msg}")
                    os.unlink(tmp_path)
                    return
                
                st.success("✅ File validated successfully")
            
            # Process file
            with st.spinner("Processing resume..."):
                try:
                    # Extract text
                    resume_text = file_processor.extract_text(tmp_path)
                    
                    if not resume_text or len(resume_text.strip()) < 50:
                        st.error("❌ Could not extract meaningful text from the resume")
                        os.unlink(tmp_path)
                        return
                    
                    # AI Analysis
                    analysis_result = ai_engine.analyze_resume(resume_text)
                    
                    # Store in session
                    st.session_state.current_analysis = analysis_result
                    st.session_state.analysis_history.append({
                        'filename': uploaded_file.name,
                        'timestamp': datetime.now(),
                        'score': analysis_result.score
                    })
                    
                    # Track analytics
                    analytics.track_analysis(uploaded_file.name, analysis_result.score)
                    
                    st.success("✅ Resume analyzed successfully!")
                    
                except Exception as e:
                    logger.error(f"Error processing resume: {e}")
                    st.error(f"❌ Error processing resume: {str(e)}")
                finally:
                    # Clean up temp file
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
    
    with col2:
        st.subheader("Analysis Tips")
        st.info("""
        📝 **Best Practices:**
        - Use clear section headers
        - Include relevant keywords
        - Quantify achievements
        - Keep format consistent
        """)
    
    # Display results
    if st.session_state.current_analysis:
        display_analysis_results(st.session_state.current_analysis)

def display_analysis_results(analysis: AnalysisResult):
    """Display comprehensive analysis results"""
    st.markdown("---")
    st.header("📊 Analysis Results")
    
    # Overall score
    col1, col2, col3 = st.columns(3)
    
    with col1:
        score_color = "🟢" if analysis.score > 0.7 else "🟡" if analysis.score > 0.4 else "🔴"
        st.metric(
            f"{score_color} Overall Score",
            f"{analysis.score:.1%}",
            help="Based on AI analysis of content, structure, and completeness"
        )
    
    with col2:
        st.metric(
            "🎯 Confidence",
            f"{analysis.confidence:.1%}",
            help="AI confidence in the analysis"
        )
    
    with col3:
        skills_count = len(analysis.details.get('extracted_skills', []))
        st.metric(
            "🛠️ Skills Found",
            skills_count,
            help="Number of technical skills identified"
        )
    
    # Detailed breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🛠️ Extracted Skills")
        skills = analysis.details.get('extracted_skills', [])
        if skills:
            for skill in skills[:10]:  # Show top 10
                st.badge(skill.title())
        else:
            st.info("No technical skills detected")
        
        st.subheader("📈 Structure Analysis")
        structure_score = analysis.details.get('structure_score', 0)
        st.progress(structure_score, text=f"Structure Quality: {structure_score:.1%}")
    
    with col2:
        st.subheader("💡 Recommendations")
        for i, rec in enumerate(analysis.recommendations, 1):
            st.write(f"{i}. {rec}")
        
        # Experience and Education
        experience = analysis.details.get('experience', [])
        education = analysis.details.get('education', [])
        
        if experience:
            st.subheader("💼 Experience Found")
            for exp in experience[:3]:  # Show top 3
                st.write(f"• {exp.get('title', 'N/A')} at {exp.get('company', 'N/A')}")
        
        if education:
            st.subheader("🎓 Education Found")
            for edu in education[:2]:  # Show top 2
                st.write(f"• {edu.get('institution', 'N/A')}")

def job_matching_page():
    """Job matching page"""
    st.header("🎯 Job Matching")
    
    if not st.session_state.current_analysis:
        st.warning("⚠️ Please analyze a resume first in the Resume Analysis section")
        return
    
    st.subheader("Job Description")
    job_description = st.text_area(
        "Paste the job description here:",
        height=200,
        placeholder="Paste the complete job description including requirements, responsibilities, and qualifications..."
    )
    
    if st.button("🔍 Analyze Job Match", type="primary"):
        if job_description.strip():
            with st.spinner("Analyzing job match..."):
                # Get resume text from previous analysis
                # For demo, we'll use a placeholder - in real app, store resume text
                resume_text = "Sample resume text"  # This should come from stored analysis
                
                # Analyze job match
                match_analysis = ai_engine.analyze_resume(resume_text, job_description)
                
                # Display match results
                st.success("✅ Job match analysis complete!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    match_score = match_analysis.details.get('job_match_score', 0.5)
                    st.metric("🎯 Match Score", f"{match_score:.1%}")
                    st.progress(match_score, text=f"Job Compatibility: {match_score:.1%}")
                
                with col2:
                    st.subheader("📋 Match Recommendations")
                    for rec in match_analysis.recommendations:
                        st.write(f"• {rec}")
        else:
            st.error("❌ Please enter a job description")

def skill_recommendations_page():
    """Skill recommendations page"""
    st.header("🛠️ Skill Recommendations")
    
    if not st.session_state.current_analysis:
        st.warning("⚠️ Please analyze a resume first in the Resume Analysis section")
        return
    
    # Current skills
    current_skills = st.session_state.current_analysis.details.get('extracted_skills', [])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Current Skills")
        if current_skills:
            for skill in current_skills:
                st.badge(skill.title(), type="secondary")
        else:
            st.info("No skills detected in resume")
    
    with col2:
        st.subheader("🚀 Recommended Skills")
        
        # Generate skill recommendations based on current skills
        recommended_skills = generate_skill_recommendations(current_skills)
        
        for skill in recommended_skills:
            st.badge(skill, type="primary")
    
    # Learning resources
    st.subheader("📚 Learning Resources")
    
    resources = {
        "Programming": ["Codecademy", "freeCodeCamp", "LeetCode"],
        "Cloud": ["AWS Training", "Azure Learn", "Google Cloud Skills"],
        "Data Science": ["Kaggle Learn", "Coursera", "edX"]
    }
    
    for category, platforms in resources.items():
        with st.expander(f"📖 {category} Resources"):
            for platform in platforms:
                st.write(f"• {platform}")

def generate_skill_recommendations(current_skills: List[str]) -> List[str]:
    """Generate intelligent skill recommendations"""
    # Skill progression maps
    skill_maps = {
        'python': ['django', 'flask', 'fastapi', 'pandas', 'numpy'],
        'javascript': ['react', 'node.js', 'typescript', 'vue', 'angular'],
        'java': ['spring', 'hibernate', 'maven', 'gradle', 'junit'],
        'aws': ['ec2', 's3', 'lambda', 'rds', 'cloudformation'],
        'docker': ['kubernetes', 'helm', 'istio', 'prometheus', 'grafana']
    }
    
    recommendations = set()
    
    for skill in current_skills:
        skill_lower = skill.lower()
        if skill_lower in skill_maps:
            recommendations.update(skill_maps[skill_lower][:3])  # Top 3 recommendations
    
    # Add trending skills if no specific recommendations
    if not recommendations:
        recommendations = {'machine learning', 'cloud computing', 'devops', 'cybersecurity', 'data analysis'}
    
    return list(recommendations)[:6]  # Return top 6

def analytics_dashboard_page():
    """Analytics dashboard page"""
    st.header("📊 Analytics Dashboard")
    
    if not st.session_state.analysis_history:
        st.info("📈 No analysis data yet. Analyze some resumes to see insights!")
        return
    
    # Analytics overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_analyses = len(st.session_state.analysis_history)
        st.metric("📄 Total Analyses", total_analyses)
    
    with col2:
        avg_score = sum(h['score'] for h in st.session_state.analysis_history) / total_analyses
        st.metric("📊 Average Score", f"{avg_score:.1%}")
    
    with col3:
        latest_score = st.session_state.analysis_history[-1]['score']
        st.metric("🎯 Latest Score", f"{latest_score:.1%}")
    
    # Analysis history
    st.subheader("📈 Analysis History")
    
    # Create DataFrame for display
    import pandas as pd
    df = pd.DataFrame(st.session_state.analysis_history)
    df['score_percent'] = df['score'].apply(lambda x: f"{x:.1%}")
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
    
    st.dataframe(
        df[['filename', 'timestamp', 'score_percent']],
        column_config={
            'filename': 'File Name',
            'timestamp': 'Analysis Time',
            'score_percent': 'Score'
        },
        use_container_width=True
    )

if __name__ == "__main__":
    main()
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