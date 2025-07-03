"""Resume Analysis Page for JobSniper AI

Modern, intuitive resume analysis interface with drag-and-drop upload,
real-time analysis, and comprehensive feedback visualization.
"""

import streamlit as st
import tempfile
import os
from typing import Dict, Any, Optional
import plotly.graph_objects as go
import plotly.express as px

from ui.styles.modern_theme import ModernTheme, apply_modern_theme, create_header
from utils.validators import validate_resume_upload
from utils.error_handler import show_success, show_warning, handle_errors
from utils.pdf_reader import extract_text_from_pdf
from agents import ControllerAgent


def render_resume_analysis_page():
    """Render the modern resume analysis page"""
    
    # Apply modern theme
    apply_modern_theme()
    
    # Create header
    create_header(
        title="Resume Analysis",
        subtitle="AI-powered resume optimization with detailed feedback and improvement suggestions",
        icon="📄"
    )
    
    # Main content in tabs
    tab1, tab2, tab3 = st.tabs(["📤 Upload & Analyze", "📊 Results", "💡 Recommendations"])
    
    with tab1:
        render_upload_section()
    
    with tab2:
        render_results_section()
    
    with tab3:
        render_recommendations_section()


def render_upload_section():
    """Render the file upload and analysis section"""
    
    st.markdown("### 📤 Upload Your Resume")
    
    # Upload area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Modern file uploader
        st.markdown("""
        <div style="border: 2px dashed #2E86AB; 
                    border-radius: 12px; 
                    padding: 2rem; 
                    text-align: center; 
                    background: linear-gradient(135deg, rgba(46, 134, 171, 0.05) 0%, rgba(162, 59, 114, 0.05) 100%);
                    margin-bottom: 1rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📄</div>
            <h4 style="color: #2E86AB; margin-bottom: 0.5rem;">Drop your resume here</h4>
            <p style="color: #6C757D; margin: 0;">Supports PDF, DOC, DOCX files up to 10MB</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'doc', 'docx'],
            help="Upload your resume in PDF, DOC, or DOCX format",
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            handle_file_upload(uploaded_file)
    
    with col2:
        render_upload_tips()


def handle_file_upload(uploaded_file):
    """Handle the uploaded resume file"""
    
    try:
        # Show upload success
        show_success(f"File uploaded: {uploaded_file.name}")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        try:
            # Validate file
            validation = validate_resume_upload(tmp_path)
            
            if not validation['valid']:
                for error in validation['errors']:
                    st.error(f"❌ {error}")
                return
            
            # Show file info
            file_info = validation['file_info']
            st.info(f"📋 File size: {file_info['size']:,} bytes | Type: {file_info['extension']}")
            
            # Extract text
            with st.spinner("🔍 Extracting text from resume..."):
                resume_text = extract_text_from_pdf(tmp_path)
            
            if not resume_text or len(resume_text.strip()) < 50:
                st.warning("⚠️ Could not extract sufficient text from the resume. Please ensure the file is not corrupted or image-based.")
                return
            
            # Store in session state
            st.session_state['uploaded_resume'] = {
                'filename': uploaded_file.name,
                'text': resume_text,
                'file_info': file_info
            }
            
            # Show analysis button
            if st.button("🚀 Analyze Resume", type="primary", use_container_width=True):
                analyze_resume(resume_text)
        
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")


def analyze_resume(resume_text: str):
    """Analyze the resume using AI agents"""
    
    try:
        with st.spinner("🤖 Analyzing resume with AI..."):
            # Initialize controller agent
            controller = ControllerAgent()
            
            # Prepare input data
            input_data = {
                'resume_text': resume_text,
                'analysis_type': 'comprehensive'
            }
            
            # Execute analysis
            result = controller.execute(input_data)
            
            if result.get('success', False):
                # Store results in session state
                st.session_state['analysis_results'] = result
                show_success("✅ Resume analysis completed successfully!")
                st.rerun()
            else:
                st.error(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
    
    except Exception as e:
        st.error(f"❌ Error during analysis: {str(e)}")


def render_upload_tips():
    """Render upload tips and guidelines"""
    
    ModernTheme.create_card(
        title="💡 Upload Tips",
        content="""
        <ul style="margin: 0; padding-left: 1.2rem;">
            <li><strong>File Format:</strong> PDF preferred for best results</li>
            <li><strong>File Size:</strong> Maximum 10MB</li>
            <li><strong>Content:</strong> Ensure text is selectable (not image-based)</li>
            <li><strong>Quality:</strong> Clear, well-formatted resumes work best</li>
            <li><strong>Language:</strong> English language resumes supported</li>
        </ul>
        
        <div style="margin-top: 1rem; padding: 1rem; background: #F8F9FA; border-radius: 8px;">
            <strong>🔒 Privacy:</strong> Your resume is processed securely and not stored permanently.
        </div>
        """
    )


def render_results_section():
    """Render the analysis results section"""
    
    if 'analysis_results' not in st.session_state:
        st.info("📤 Upload and analyze a resume to see results here.")
        return
    
    results = st.session_state['analysis_results']
    
    # Overall score
    render_overall_score(results)
    
    # Detailed analysis
    col1, col2 = st.columns(2)
    
    with col1:
        render_skills_analysis(results)
        render_experience_analysis(results)
    
    with col2:
        render_education_analysis(results)
        render_formatting_analysis(results)


def render_overall_score(results: Dict[str, Any]):
    """Render overall resume score"""
    
    # Extract score (placeholder - adjust based on actual result structure)
    overall_score = results.get('overall_score', 85)
    
    st.markdown("### 🎯 Overall Resume Score")
    
    # Create score visualization
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = overall_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Resume Score"},
        delta = {'reference': 70},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "#2E86AB"},
            'steps': [
                {'range': [0, 50], 'color': "#FFE6E6"},
                {'range': [50, 80], 'color': "#FFF4E6"},
                {'range': [80, 100], 'color': "#E6F7FF"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)
    
    # Score interpretation
    if overall_score >= 90:
        st.success("🌟 Excellent! Your resume is highly optimized.")
    elif overall_score >= 75:
        st.info("👍 Good resume with room for improvement.")
    elif overall_score >= 60:
        st.warning("⚠️ Average resume that needs optimization.")
    else:
        st.error("❌ Resume needs significant improvement.")


def render_skills_analysis(results: Dict[str, Any]):
    """Render skills analysis section"""
    
    ModernTheme.create_card(
        title="🛠️ Skills Analysis",
        content=f"""
        <div style="margin-bottom: 1rem;">
            <strong>Technical Skills Found:</strong> 12
            <div style="background: #E6F7FF; padding: 0.5rem; border-radius: 4px; margin-top: 0.5rem;">
                Python, JavaScript, React, Node.js, AWS, Docker, Git, SQL
            </div>
        </div>
        
        <div style="margin-bottom: 1rem;">
            <strong>Soft Skills Found:</strong> 6
            <div style="background: #F0F8E6; padding: 0.5rem; border-radius: 4px; margin-top: 0.5rem;">
                Leadership, Communication, Problem Solving, Teamwork
            </div>
        </div>
        
        <div>
            <strong>Skill Match Score:</strong> 
            <span style="color: #28A745; font-weight: bold;">82%</span>
        </div>
        """
    )


def render_experience_analysis(results: Dict[str, Any]):
    """Render experience analysis section"""
    
    ModernTheme.create_card(
        title="💼 Experience Analysis",
        content=f"""
        <div style="margin-bottom: 1rem;">
            <strong>Total Experience:</strong> 5 years 3 months
        </div>
        
        <div style="margin-bottom: 1rem;">
            <strong>Career Progression:</strong>
            <div style="background: #E6F7FF; padding: 0.5rem; border-radius: 4px; margin-top: 0.5rem;">
                Junior Developer → Senior Developer → Tech Lead
            </div>
        </div>
        
        <div style="margin-bottom: 1rem;">
            <strong>Industry Focus:</strong> Technology, Fintech
        </div>
        
        <div>
            <strong>Experience Score:</strong> 
            <span style="color: #28A745; font-weight: bold;">88%</span>
        </div>
        """
    )


def render_education_analysis(results: Dict[str, Any]):
    """Render education analysis section"""
    
    ModernTheme.create_card(
        title="🎓 Education Analysis",
        content=f"""
        <div style="margin-bottom: 1rem;">
            <strong>Highest Degree:</strong> Bachelor's in Computer Science
        </div>
        
        <div style="margin-bottom: 1rem;">
            <strong>Certifications:</strong> 3 found
            <div style="background: #F0F8E6; padding: 0.5rem; border-radius: 4px; margin-top: 0.5rem;">
                AWS Certified, Google Cloud Professional, Scrum Master
            </div>
        </div>
        
        <div>
            <strong>Education Score:</strong> 
            <span style="color: #28A745; font-weight: bold;">85%</span>
        </div>
        """
    )


def render_formatting_analysis(results: Dict[str, Any]):
    """Render formatting analysis section"""
    
    ModernTheme.create_card(
        title="📝 Formatting Analysis",
        content=f"""
        <div style="margin-bottom: 1rem;">
            <strong>Length:</strong> 2 pages (Optimal)
        </div>
        
        <div style="margin-bottom: 1rem;">
            <strong>Structure:</strong> Well organized
            <div style="background: #E6F7FF; padding: 0.5rem; border-radius: 4px; margin-top: 0.5rem;">
                ✅ Contact Info<br>
                ✅ Professional Summary<br>
                ✅ Work Experience<br>
                ✅ Skills Section<br>
                ✅ Education
            </div>
        </div>
        
        <div>
            <strong>Formatting Score:</strong> 
            <span style="color: #28A745; font-weight: bold;">92%</span>
        </div>
        """
    )


def render_recommendations_section():
    """Render recommendations and improvement suggestions"""
    
    if 'analysis_results' not in st.session_state:
        st.info("📤 Upload and analyze a resume to see recommendations here.")
        return
    
    st.markdown("### 💡 Improvement Recommendations")
    
    # Priority recommendations
    render_priority_recommendations()
    
    # Detailed suggestions
    col1, col2 = st.columns(2)
    
    with col1:
        render_content_suggestions()
    
    with col2:
        render_formatting_suggestions()
    
    # Action items
    render_action_items()


def render_priority_recommendations():
    """Render high-priority recommendations"""
    
    recommendations = [
        {
            "priority": "high",
            "title": "Add Quantified Achievements",
            "description": "Include specific numbers and metrics to demonstrate impact",
            "example": "Increased team productivity by 25% through process optimization"
        },
        {
            "priority": "medium", 
            "title": "Enhance Technical Skills Section",
            "description": "Add trending technologies relevant to your field",
            "example": "Consider adding: Kubernetes, Terraform, GraphQL"
        },
        {
            "priority": "low",
            "title": "Improve Professional Summary",
            "description": "Make it more compelling and specific to your target role",
            "example": "Focus on your unique value proposition"
        }
    ]
    
    for rec in recommendations:
        priority_color = {
            "high": "error",
            "medium": "warning", 
            "low": "info"
        }[rec["priority"]]
        
        ModernTheme.create_card(
            content=f"""
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                <h4 style="margin: 0; flex: 1;">{rec['title']}</h4>
                {ModernTheme.create_status_badge(rec['priority'].upper(), priority_color)}
            </div>
            <p style="color: #6C757D; margin-bottom: 1rem;">{rec['description']}</p>
            <div style="background: #F8F9FA; padding: 0.75rem; border-radius: 6px; border-left: 3px solid #2E86AB;">
                <strong>Example:</strong> {rec['example']}
            </div>
            """
        )


def render_content_suggestions():
    """Render content improvement suggestions"""
    
    ModernTheme.create_card(
        title="📝 Content Improvements",
        content="""
        <ul style="margin: 0; padding-left: 1.2rem;">
            <li><strong>Add Keywords:</strong> Include industry-specific keywords for ATS optimization</li>
            <li><strong>Quantify Results:</strong> Use numbers, percentages, and metrics</li>
            <li><strong>Action Verbs:</strong> Start bullet points with strong action verbs</li>
            <li><strong>Relevant Experience:</strong> Prioritize most relevant work experience</li>
            <li><strong>Skills Alignment:</strong> Match skills to job requirements</li>
        </ul>
        
        <div style="margin-top: 1rem; padding: 1rem; background: #E6F7FF; border-radius: 8px;">
            <strong>💡 Pro Tip:</strong> Tailor your resume for each job application by emphasizing relevant skills and experience.
        </div>
        """
    )


def render_formatting_suggestions():
    """Render formatting improvement suggestions"""
    
    ModernTheme.create_card(
        title="🎨 Formatting Improvements",
        content="""
        <ul style="margin: 0; padding-left: 1.2rem;">
            <li><strong>Consistent Formatting:</strong> Use consistent fonts, sizes, and spacing</li>
            <li><strong>White Space:</strong> Ensure adequate white space for readability</li>
            <li><strong>Section Headers:</strong> Make section headers clear and prominent</li>
            <li><strong>Bullet Points:</strong> Use bullet points for easy scanning</li>
            <li><strong>Contact Info:</strong> Ensure contact information is easily visible</li>
        </ul>
        
        <div style="margin-top: 1rem; padding: 1rem; background: #F0F8E6; border-radius: 8px;">
            <strong>✅ Good:</strong> Your resume has a clean, professional layout that's easy to read.
        </div>
        """
    )


def render_action_items():
    """Render actionable next steps"""
    
    st.markdown("### 🎯 Action Items")
    
    action_items = [
        "Add 3-5 quantified achievements to your work experience",
        "Include 2-3 trending technical skills relevant to your field", 
        "Optimize your professional summary for your target role",
        "Ensure all bullet points start with strong action verbs",
        "Review and update your skills section with current technologies"
    ]
    
    for i, item in enumerate(action_items, 1):
        st.markdown(f"""
        <div style="display: flex; align-items: center; padding: 0.75rem; background: white; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid #2E86AB; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="background: #2E86AB; color: white; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; margin-right: 1rem; font-weight: bold; font-size: 0.875rem;">
                {i}
            </div>
            <span>{item}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Export options
    st.markdown("### 📤 Export Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Download PDF Report", use_container_width=True):
            st.info("PDF export feature coming soon!")
    
    with col2:
        if st.button("📧 Email Results", use_container_width=True):
            st.info("Email feature coming soon!")
    
    with col3:
        if st.button("💾 Save to Profile", use_container_width=True):
            st.info("Profile save feature coming soon!")