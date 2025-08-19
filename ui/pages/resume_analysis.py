"""
🎯 Quantum Resume Analysis Page
==============================

Revolutionary resume analysis interface with AI-powered insights,
interactive visualizations, and quantum UI components.
"""

import streamlit as st
import tempfile
import os
import time
from typing import Dict, Any, Optional
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from ui.components.quantum_components import (
    quantum_header, quantum_card, quantum_metrics_grid, quantum_progress,
    quantum_status, quantum_timeline
)
from utils.validators import validate_resume_upload
from utils.error_handler import show_success, show_warning
from utils.pdf_reader import extract_text_from_pdf


class QuantumResumeAnalyzer:
    """Advanced resume analysis with quantum UI"""
    
    def __init__(self):
        self.analysis_results = None
        
    def render(self):
        """Render the quantum resume analysis page"""
        
        quantum_header(
            title="Resume Analysis",
            subtitle="AI-powered resume optimization with quantum precision and real-time insights",
            icon="📄",
            gradient="ocean"
        )
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "📤 Upload & Analyze", 
            "📊 Analysis Results", 
            "💡 Recommendations", 
            "📈 Optimization"
        ])
        
        with tab1:
            self.render_upload_section()
        
        with tab2:
            self.render_results_section()
        
        with tab3:
            self.render_recommendations_section()
        
        with tab4:
            self.render_optimization_section()
    
    def render_upload_section(self):
        """Render the quantum file upload section"""
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'doc', 'docx'],
            help="Upload your resume for quantum AI analysis",
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            self.handle_file_upload(uploaded_file)
    
    def handle_file_upload(self, uploaded_file):
        """Handle file upload and analysis"""
        import tempfile
        import os
        from utils.pdf_reader import extract_text_from_pdf
        from agents.controller_agent import ControllerAgent

        # Show success message
        st.success(f"✅ File uploaded successfully: {uploaded_file.name}")

        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name

            # Validate file
            from utils.validators import validate_resume_upload
            validation = validate_resume_upload(tmp_path)

            if not validation['valid']:
                for error in validation['errors']:
                    st.error(f"❌ {error}")
                return

            # Show warnings if any
            for warning in validation.get('warnings', []):
                st.warning(f"⚠️ {warning}")

            # Extract text and analyze
            if st.button("🚀 Analyze Resume", type="primary", use_container_width=True):
                self.analyze_resume(tmp_path)

        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
        finally:
            if 'tmp_path' in locals() and os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def analyze_resume(self, file_path: str):
        """Analyze resume using AI agents"""
        from utils.pdf_reader import extract_text_from_pdf
        from agents.controller_agent import ControllerAgent

        with st.spinner("🔍 Analyzing your resume..."):
            try:
                # Extract text
                resume_text = extract_text_from_pdf(file_path)
                if not resume_text or len(resume_text.strip()) < 50:
                    st.warning("⚠️ Could not extract sufficient text. Please ensure the file is not image-based.")
                    return

                # Run analysis through controller agent
                controller = ControllerAgent()
                analysis_results = controller.run(resume_text)

                # Store results in session state
                st.session_state['resume_analysis'] = analysis_results
                self.analysis_results = analysis_results

                st.success("✅ Resume analysis completed! Check the other tabs for detailed results.")
                st.balloons()

            except Exception as e:
                st.error(f"❌ Error analyzing resume: {str(e)}")
                # Fallback to mock analysis for demo
                self.analysis_results = self.generate_mock_analysis(resume_text if 'resume_text' in locals() else "")
                st.session_state['resume_analysis'] = self.analysis_results

    def generate_mock_analysis(self, resume_text: str) -> Dict[str, Any]:
        """Generate mock analysis results as fallback"""
        return {
            'parsed_data': {
                'name': 'Resume Candidate',
                'skills': ['Python', 'JavaScript', 'SQL', 'Machine Learning'],
                'experience': 'Software Developer with 3+ years experience',
                'education': 'Bachelor of Computer Science',
                'contact': 'candidate@email.com'
            },
            'matched_data': {
                'matched_skills': ['Python', 'JavaScript', 'SQL'],
                'match_percent': 75,
                'suggested_skills': ['React', 'AWS', 'Docker'],
                'job_roles': ['Software Developer', 'Full Stack Developer', 'Backend Developer']
            },
            'feedback': {
                'overall_score': 7.5,
                'strengths': ['Strong technical skills', 'Good experience level'],
                'improvements': ['Add more quantified achievements', 'Include certifications'],
                'recommendations': ['Consider adding cloud technologies', 'Highlight leadership experience']
            }
        }

    def render_results_section(self):
        """Render analysis results"""
        if 'resume_analysis' not in st.session_state:
            st.markdown("""
            <div style="text-align: center; padding: 3rem; color: #666;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">📊</div>
                <h3>No Analysis Results</h3>
                <p>Upload a resume in the "Upload & Analyze" tab to see detailed analysis results here.</p>
            </div>
            """, unsafe_allow_html=True)
            return

        results = st.session_state['resume_analysis']

        # Display parsed data
        if 'parsed_data' in results:
            parsed = results['parsed_data']

            st.subheader("📋 Parsed Information")
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Name:** {parsed.get('name', 'N/A')}")
                st.write(f"**Contact:** {parsed.get('contact', 'N/A')}")
                st.write(f"**Experience:** {parsed.get('years_of_experience', 'N/A')} years")

            with col2:
                st.write(f"**Education:** {parsed.get('education', 'N/A')}")
                if parsed.get('skills'):
                    st.write(f"**Skills:** {', '.join(parsed['skills'][:5])}")

        # Display matching results
        if 'matched_data' in results:
            matched = results['matched_data']

            st.subheader("🎯 Job Matching Analysis")

            # Match percentage
            match_percent = matched.get('match_percent', 0)
            st.metric("Overall Match Score", f"{match_percent}%")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Matched Skills:**")
                for skill in matched.get('matched_skills', []):
                    st.write(f"✅ {skill}")

            with col2:
                st.write("**Suggested Skills:**")
                for skill in matched.get('suggested_skills', []):
                    st.write(f"📚 {skill}")

            st.write("**Recommended Job Roles:**")
            for role in matched.get('job_roles', []):
                st.write(f"🎯 {role}")

        # Display feedback
        if 'feedback' in results:
            feedback = results['feedback']

            st.subheader("💡 AI Feedback")

            if 'overall_score' in feedback:
                st.metric("Overall Resume Score", f"{feedback['overall_score']}/10")

            if feedback.get('strengths'):
                st.write("**Strengths:**")
                for strength in feedback['strengths']:
                    st.write(f"💪 {strength}")

            if feedback.get('improvements'):
                st.write("**Areas for Improvement:**")
                for improvement in feedback['improvements']:
                    st.write(f"🔧 {improvement}")

    def render_recommendations_section(self):
        """Render recommendations"""
        if 'resume_analysis' not in st.session_state:
            st.markdown("""
            <div style="text-align: center; padding: 3rem; color: #666;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">💡</div>
                <h3>No Recommendations Available</h3>
                <p>Analyze your resume first to get personalized recommendations for improvement.</p>
            </div>
            """, unsafe_allow_html=True)
            return

        results = st.session_state['resume_analysis']

        st.subheader("💡 Personalized Recommendations")

        # Skill recommendations
        if 'matched_data' in results and results['matched_data'].get('suggested_skills'):
            st.write("### 📚 Skills to Learn")
            for skill in results['matched_data']['suggested_skills']:
                with st.expander(f"Learn {skill}"):
                    st.write(f"Adding {skill} to your skillset could improve your job market competitiveness.")
                    st.write("**Recommended Resources:**")
                    st.write("- Online courses (Coursera, Udemy)")
                    st.write("- Official documentation")
                    st.write("- Practice projects")

        # General recommendations
        if 'feedback' in results and results['feedback'].get('recommendations'):
            st.write("### 🎯 Career Recommendations")
            for i, rec in enumerate(results['feedback']['recommendations'], 1):
                st.write(f"{i}. {rec}")

        # Job role recommendations
        if 'matched_data' in results and results['matched_data'].get('job_roles'):
            st.write("### 🎯 Recommended Job Roles")
            for role in results['matched_data']['job_roles']:
                st.write(f"• **{role}** - Based on your current skills and experience")

    def render_optimization_section(self):
        """Render optimization tools"""
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #666;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📈</div>
            <h3>Optimization Tools</h3>
            <p>Advanced optimization features will be available after resume analysis.</p>
        </div>
        """, unsafe_allow_html=True)


def render():
    """Render the quantum resume analysis page"""
    analyzer = QuantumResumeAnalyzer()
    analyzer.render()