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

if __name__ == "__main__":
    main()