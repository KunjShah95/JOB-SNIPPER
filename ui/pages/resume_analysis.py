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
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📤 Upload & Analyze", 
            "📊 Analysis Results", 
            "🎯 Resume Score",
            "💡 Recommendations", 
            "📈 Optimization"
        ])
        
        with tab1:
            self.render_upload_section()
        
        with tab2:
            self.render_results_section()
        
        with tab3:
            self.render_scoring_section()
        
        with tab4:
            self.render_recommendations_section()
        
        with tab5:
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

                # Ensure analysis_results is a dictionary
                if not isinstance(analysis_results, dict):
                    st.warning("⚠️ Analysis returned invalid format, using fallback data.")
                    analysis_results = self.generate_mock_analysis(resume_text)

                # Store results in session state
                st.session_state['resume_analysis'] = analysis_results
                self.analysis_results = analysis_results

                st.success("✅ Resume analysis completed! Check the other tabs for detailed results.")
                st.balloons()

            except Exception as e:
                st.error(f"❌ Error analyzing resume: {str(e)}")
                # Fallback to mock analysis for demo
                mock_results = self.generate_mock_analysis(resume_text if 'resume_text' in locals() else "")
                self.analysis_results = mock_results
                st.session_state['resume_analysis'] = mock_results

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

        # Ensure results is a dictionary
        if not isinstance(results, dict):
            st.error("❌ Invalid analysis results format. Please re-upload and analyze your resume.")
            return

        # Display parsed data
        if isinstance(results.get('parsed_data'), dict):
            parsed = results['parsed_data']

            st.subheader("📋 Parsed Information")
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Name:** {parsed.get('name', 'N/A')}")
                st.write(f"**Contact:** {parsed.get('contact', 'N/A')}")
                st.write(f"**Experience:** {parsed.get('years_of_experience', 'N/A')} years")

            with col2:
                st.write(f"**Education:** {parsed.get('education', 'N/A')}")
                if parsed.get('skills') and isinstance(parsed['skills'], list):
                    st.write(f"**Skills:** {', '.join(parsed['skills'][:5])}")

        # Display matching results
        if isinstance(results.get('matched_data'), dict):
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
        if isinstance(results.get('feedback'), dict):
            feedback = results['feedback']

            st.subheader("💡 AI Feedback")

            if 'overall_score' in feedback:
                st.metric("Overall Resume Score", f"{feedback['overall_score']}/10")

            if feedback.get('strengths') and isinstance(feedback['strengths'], list):
                st.write("**Strengths:**")
                for strength in feedback['strengths']:
                    st.write(f"💪 {strength}")

            if feedback.get('improvements') and isinstance(feedback['improvements'], list):
                st.write("**Areas for Improvement:**")
                for improvement in feedback['improvements']:
                    st.write(f"🔧 {improvement}")

    def render_scoring_section(self):
        """Render resume scoring results"""
        if 'resume_analysis' not in st.session_state:
            st.markdown("""
            <div style="text-align: center; padding: 3rem; color: #666;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🎯</div>
                <h3>No Scoring Results</h3>
                <p>Upload and analyze your resume to get detailed scoring and feedback.</p>
            </div>
            """, unsafe_allow_html=True)
            return

        results = st.session_state['resume_analysis']

        # Ensure results is a dictionary
        if not isinstance(results, dict):
            st.error("❌ Invalid analysis results format.")
            return

        # Check if scoring results are available
        if 'scoring_result' not in results or not isinstance(results['scoring_result'], dict):
            st.markdown("""
            <div style="text-align: center; padding: 2rem; color: #666;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
                <h4>Resume Scoring Not Available</h4>
                <p>The scoring analysis is being processed. Please try again in a moment.</p>
            </div>
            """, unsafe_allow_html=True)
            return

        scoring = results['scoring_result']

        # Overall Score Display
        st.subheader("📊 Resume Score Overview")

        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            overall_score = scoring.get('overall_score', 0)
            # Score gauge using plotly
            import plotly.graph_objects as go

            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=overall_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Overall Resume Score"},
                delta={'reference': 80, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
                gauge={
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': "darkblue"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 40], 'color': 'lightcoral'},
                        {'range': [40, 60], 'color': 'lightyellow'},
                        {'range': [60, 80], 'color': 'lightgreen'},
                        {'range': [80, 100], 'color': 'darkgreen'}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 80
                    }
                }
            ))

            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Score interpretation
            if overall_score >= 80:
                st.success("🏆 Excellent!")
                st.write("Your resume is highly competitive.")
            elif overall_score >= 60:
                st.warning("👍 Good")
                st.write("Your resume is solid with room for improvement.")
            else:
                st.error("⚠️ Needs Work")
                st.write("Consider major improvements to your resume.")

        with col3:
            # Scoring method
            method = scoring.get('scoring_method', 'Unknown')
            st.info(f"Method: {method}")
            level = scoring.get('experience_level', 'Unknown')
            st.write(f"Level: {level}")

        # Detailed Breakdown
        st.subheader("📈 Detailed Score Breakdown")

        breakdown = scoring.get('breakdown', {})
        if breakdown:
            # Create a radar chart for the breakdown
            categories = list(breakdown.keys())
            values = [breakdown[cat] for cat in categories]

            fig_radar = go.Figure()

            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='Your Scores',
                line_color='darkblue'
            ))

            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, max(values) + 5] if values else [0, 25]
                    )),
                showlegend=False,
                height=400
            )

            st.plotly_chart(fig_radar, use_container_width=True)

            # Individual score bars
            st.write("**Individual Component Scores:**")
            for category, score in breakdown.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{category.replace('_', ' ').title()}:**")
                with col2:
                    st.progress(score / 25 if 'skills' in category.lower() or 'relevance' in category.lower() else
                              score / 20 if 'education' in category.lower() else score / 15)
                    st.write(f"{score}")

        # Strengths and Improvements
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("💪 Strengths")
            strengths = scoring.get('strengths', [])
            if strengths:
                for strength in strengths:
                    st.success(f"✅ {strength}")
            else:
                st.write("No specific strengths identified.")

        with col2:
            st.subheader("🔧 Areas for Improvement")
            improvements = scoring.get('improvements', [])
            if improvements:
                for improvement in improvements:
                    st.warning(f"⚠️ {improvement}")
            else:
                st.write("No major improvements needed.")

        # Missing Skills
        st.subheader("📚 Recommended Skills to Add")
        missing_skills = scoring.get('missing_skills', [])
        if missing_skills:
            cols = st.columns(3)
            for i, skill in enumerate(missing_skills):
                with cols[i % 3]:
                    st.info(f"🎯 {skill}")
        else:
            st.write("No additional skills recommended at this time.")

        # Industry Match
        industry_match = scoring.get('industry_match', 'General')
        st.subheader(f"🏢 Best Industry Match: {industry_match}")

        # Timestamp
        timestamp = scoring.get('timestamp', 'Unknown')
        st.caption(f"Analysis completed: {timestamp}")

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
    # Add content offset for fixed navbar
    st.markdown('<div class="jobsniper-content-offset">', unsafe_allow_html=True)

    analyzer = QuantumResumeAnalyzer()
    analyzer.render()

    st.markdown('</div>', unsafe_allow_html=True)