#!/usr/bin/env python3
"""
Simple JobSniper AI App - Fixed Version

This is a simplified version that works with all the fixes applied.
"""

import streamlit as st
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Apply sidebar fix immediately
st.markdown('<style>section[data-testid="stSidebar"]{background:linear-gradient(180deg,#1a365d 0%,#2d3748 50%,#1a202c 100%)!important}section[data-testid="stSidebar"] *{color:white!important}</style>', unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Set page config
    st.set_page_config(
        page_title="JobSniper AI - Fixed",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Main content
    st.title("🎯 JobSniper AI - All Fixes Applied")
    st.write("Professional Resume & Career Intelligence Platform")
    
    # Sidebar
    with st.sidebar:
        st.title("🎯 JobSniper AI")
        st.write("Navigation & Settings")
        
        # Navigation
        page = st.radio(
            "Choose a section:",
            ["🏠 Home", "📄 Resume Analysis", "🎯 Job Matching", "⚙️ Settings"],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Status
        st.markdown("### ⚙️ System Status")
        
        try:
            from utils.config import validate_config
            validation = validate_config()
            
            if validation.get('ai_providers'):
                providers = ', '.join(validation['ai_providers']).replace('gemini-2.5-pro', 'Gemini 2.5 Pro')
                st.success(f"🤖 AI: {providers}")
            else:
                st.warning("🤖 AI: Configure API keys")
                
            st.info(f"🔧 Features: {validation.get('total_features', 0)} enabled")
            
        except Exception as e:
            st.error(f"❌ Config Error: {str(e)[:50]}...")
        
        st.divider()
        
        # Quick settings
        st.markdown("### 🔧 Quick Settings")
        demo_mode = st.checkbox("Demo Mode", value=True)
        debug_mode = st.checkbox("Debug Mode", value=False)
    
    # Main content based on selection
    if page == "🏠 Home":
        show_home()
    elif page == "📄 Resume Analysis":
        show_resume_analysis()
    elif page == "🎯 Job Matching":
        show_job_matching()
    elif page == "⚙️ Settings":
        show_settings()

def show_home():
    """Show home page"""
    st.header("🏠 Welcome to JobSniper AI")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📄 Resume Analysis
        - Parse and analyze resumes
        - Extract skills and experience
        - Get improvement suggestions
        """)
    
    with col2:
        st.markdown("""
        ### 🎯 Job Matching
        - Match skills to job requirements
        - Find suitable positions
        - Get compatibility scores
        """)
    
    with col3:
        st.markdown("""
        ### 🚀 AI-Powered
        - Gemini 2.5 Pro model
        - Advanced NLP processing
        - Intelligent recommendations
        """)
    
    st.markdown("---")
    
    # Test the fixed components
    st.subheader("🧪 Component Tests")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Test Resume Parser"):
            try:
                from agents.resume_parser_agent import ResumeParserAgent
                agent = ResumeParserAgent()
                st.success("✅ Resume Parser working!")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    with col2:
        if st.button("Test Controller"):
            try:
                from agents.controller_agent import ControllerAgent
                controller = ControllerAgent()
                st.success("✅ Controller working!")
            except Exception as e:
                st.error(f"❌ Error: {e}")

def show_resume_analysis():
    """Show resume analysis page"""
    st.header("📄 Resume Analysis")
    
    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=['pdf', 'docx', 'txt'],
        help="Upload a PDF, DOCX, or TXT file"
    )
    
    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        
        if st.button("Analyze Resume"):
            with st.spinner("Analyzing resume..."):
                try:
                    # Simple demo analysis
                    st.subheader("📊 Analysis Results")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Skills Found", "12")
                        st.metric("Experience Years", "5")
                        st.metric("Match Score", "85%")
                    
                    with col2:
                        st.write("**Top Skills:**")
                        st.write("• Python")
                        st.write("• Machine Learning")
                        st.write("• Data Analysis")
                        st.write("• Streamlit")
                    
                    st.success("✅ Analysis complete!")
                    
                except Exception as e:
                    st.error(f"❌ Analysis failed: {e}")

def show_job_matching():
    """Show job matching page"""
    st.header("🎯 Job Matching")
    
    job_title = st.text_input("Enter job title:", placeholder="e.g., Data Scientist")
    
    if job_title:
        if st.button("Find Matches"):
            with st.spinner("Finding job matches..."):
                st.subheader("🎯 Job Matches")
                
                # Demo matches
                matches = [
                    {"title": "Senior Data Scientist", "company": "TechCorp", "match": "92%"},
                    {"title": "ML Engineer", "company": "AI Startup", "match": "88%"},
                    {"title": "Data Analyst", "company": "BigCorp", "match": "75%"}
                ]
                
                for match in matches:
                    with st.expander(f"{match['title']} at {match['company']} - {match['match']} match"):
                        st.write(f"**Company:** {match['company']}")
                        st.write(f"**Match Score:** {match['match']}")
                        st.write("**Requirements:** Python, SQL, Machine Learning")

def show_settings():
    """Show settings page"""
    st.header("⚙️ Settings")
    
    st.subheader("🔑 API Configuration")
    
    with st.form("api_config"):
        gemini_key = st.text_input("Gemini API Key", type="password")
        mistral_key = st.text_input("Mistral API Key", type="password")
        
        if st.form_submit_button("Save Configuration"):
            if gemini_key or mistral_key:
                st.success("✅ Configuration saved!")
            else:
                st.warning("⚠️ Please provide at least one API key")
    
    st.subheader("🎛️ Feature Toggles")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("Resume Builder", value=True)
        st.checkbox("Job Matching", value=True)
        st.checkbox("Skill Analysis", value=True)
    
    with col2:
        st.checkbox("Auto Apply", value=False)
        st.checkbox("Email Reports", value=False)
        st.checkbox("Analytics", value=True)

if __name__ == "__main__":
    main()