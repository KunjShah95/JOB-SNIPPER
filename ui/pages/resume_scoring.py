"""
Resume Scoring Page - AI-Powered Resume Evaluation
New page for the enhanced JobSniper AI with scoring capabilities
"""

import streamlit as st
import tempfile
import os
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any

def render():
    """Render the resume scoring page"""
    
    st.title("🎯 AI Resume Scoring")
    st.markdown("Get detailed AI-powered analysis and scoring of your resume")
    
    # Create tabs for different scoring features
    tab1, tab2, tab3 = st.tabs(["📊 Score Resume", "📈 Analytics", "💡 Improvement Tips"])
    
    with tab1:
        render_scoring_interface()
    
    with tab2:
        render_scoring_analytics()
    
    with tab3:
        render_improvement_tips()

def render_scoring_interface():
    """Main resume scoring interface"""
    
    st.markdown("### Upload Resume for Scoring")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose your resume file",
        type=['pdf', 'docx', 'txt'],
        help="Upload your resume in PDF, DOCX, or TXT format"
    )
    
    if uploaded_file is not None:
        # Display file info
        st.success(f"✅ File uploaded: {uploaded_file.name} ({uploaded_file.size} bytes)")
        
        # Processing options
        col1, col2 = st.columns(2)
        
        with col1:
            target_role = st.selectbox(
                "Target Role (Optional)",
                ["General", "Software Engineer", "Data Scientist", "Product Manager", 
                 "Marketing Manager", "Sales Representative", "Designer"]
            )
        
        with col2:
            experience_level = st.selectbox(
                "Experience Level",
                ["Auto-detect", "Entry Level", "Mid Level", "Senior Level", "Executive"]
            )
        
        # Score button
        if st.button("🚀 Score My Resume", type="primary", use_container_width=True):
            score_resume(uploaded_file, target_role, experience_level)

def score_resume(uploaded_file, target_role: str, experience_level: str):
    """Process and score the uploaded resume"""
    
    with st.spinner("🔍 Analyzing your resume..."):
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            # Extract text from file
            resume_text = extract_text_from_file(tmp_path)
            
            if not resume_text:
                st.error("❌ Could not extract text from the file. Please try a different format.")
                return
            
            # Get scoring results (mock for now - will integrate with enhanced_orchestrator)
            scoring_result = get_resume_score(resume_text, target_role, experience_level)
            
            # Display results
            display_scoring_results(scoring_result)
            
            # Store in session state for analytics
            if "scoring_history" not in st.session_state:
                st.session_state.scoring_history = []
            
            st.session_state.scoring_history.append({
                "timestamp": datetime.now(),
                "filename": uploaded_file.name,
                "score": scoring_result["overall_score"],
                "target_role": target_role,
                "result": scoring_result
            })
            
        except Exception as e:
            st.error(f"❌ Error processing resume: {str(e)}")
        
        finally:
            # Clean up temporary file
            if 'tmp_path' in locals() and os.path.exists(tmp_path):
                os.unlink(tmp_path)

def extract_text_from_file(file_path: str) -> str:
    """Extract text from uploaded file"""
    try:
        if file_path.endswith('.pdf'):
            from utils.pdf_reader import extract_text_from_pdf
            return extract_text_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            from docx import Document
            doc = Document(file_path)
            return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        elif file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return ""
    except Exception as e:
        st.error(f"Error extracting text: {str(e)}")
        return ""

def get_resume_score(resume_text: str, target_role: str, experience_level: str) -> Dict[str, Any]:
    """Get resume score (mock implementation - will integrate with enhanced_orchestrator)"""
    
    # TODO: Integrate with enhanced_orchestrator.py and resume_scorer_agent.py
    # For now, return mock data
    
    import random
    
    # Simulate scoring based on content length and keywords
    base_score = min(len(resume_text.split()) // 10, 70)  # Base score from content length
    
    # Add randomness for demo
    scores = {
        "technical_skills": min(base_score + random.randint(-5, 10), 25),
        "experience_relevance": min(base_score + random.randint(-5, 10), 25),
        "education_alignment": min(base_score + random.randint(-5, 8), 20),
        "format_structure": min(base_score + random.randint(-3, 5), 15),
        "keywords_density": min(base_score + random.randint(-3, 5), 15)
    }
    
    overall_score = sum(scores.values())
    
    return {
        "overall_score": overall_score,
        "breakdown": scores,
        "strengths": [
            "Strong technical skill set",
            "Clear professional experience",
            "Well-structured format",
            "Good use of action verbs"
        ],
        "improvements": [
            "Add more quantified achievements",
            "Include relevant keywords for ATS",
            "Expand on project outcomes",
            "Consider adding a professional summary"
        ],
        "missing_skills": [
            "Cloud Computing (AWS/Azure)",
            "API Development",
            "Agile Methodologies",
            "Data Analysis"
        ],
        "industry_match": target_role if target_role != "General" else "Technology",
        "experience_level": experience_level if experience_level != "Auto-detect" else "Mid-Level",
        "timestamp": datetime.now().isoformat(),
        "scoring_method": "ai_enhanced"
    }

def display_scoring_results(result: Dict[str, Any]):
    """Display the scoring results with visualizations"""
    
    overall_score = result["overall_score"]
    breakdown = result["breakdown"]
    
    # Overall score display
    st.markdown("### 📊 Overall Score")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Score gauge
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = overall_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Resume Score"},
            delta = {'reference': 80},
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
        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        # Score interpretation
        if overall_score >= 80:
            st.success("🌟 Excellent")
            st.markdown("Your resume is highly competitive!")
        elif overall_score >= 60:
            st.warning("👍 Good")
            st.markdown("Your resume is solid with room for improvement.")
        else:
            st.error("📈 Needs Work")
            st.markdown("Consider significant improvements.")
    
    with col3:
        # Quick stats
        st.metric("Industry Match", result.get("industry_match", "General"))
        st.metric("Experience Level", result.get("experience_level", "Mid-Level"))
    
    # Detailed breakdown
    st.markdown("### 📋 Detailed Breakdown")
    
    # Create breakdown chart
    categories = list(breakdown.keys())
    scores = list(breakdown.values())
    max_scores = [25, 25, 20, 15, 15]  # Maximum possible scores
    
    fig_breakdown = go.Figure()
    
    # Add actual scores
    fig_breakdown.add_trace(go.Bar(
        name='Your Score',
        x=categories,
        y=scores,
        marker_color='steelblue'
    ))
    
    # Add maximum possible scores as reference
    fig_breakdown.add_trace(go.Bar(
        name='Maximum Possible',
        x=categories,
        y=max_scores,
        marker_color='lightgray',
        opacity=0.5
    ))
    
    fig_breakdown.update_layout(
        title="Score Breakdown by Category",
        xaxis_title="Categories",
        yaxis_title="Points",
        barmode='overlay',
        height=400
    )
    
    st.plotly_chart(fig_breakdown, use_container_width=True)
    
    # Strengths and improvements
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Strengths")
        for strength in result.get("strengths", []):
            st.markdown(f"• {strength}")
    
    with col2:
        st.markdown("### 🔧 Areas for Improvement")
        for improvement in result.get("improvements", []):
            st.markdown(f"• {improvement}")
    
    # Missing skills
    if result.get("missing_skills"):
        st.markdown("### 🎯 Recommended Skills to Add")
        skills_cols = st.columns(len(result["missing_skills"]))
        for i, skill in enumerate(result["missing_skills"]):
            with skills_cols[i]:
                st.info(skill)

def render_scoring_analytics():
    """Render scoring analytics and history"""
    
    st.markdown("### 📈 Your Scoring History")
    
    if "scoring_history" not in st.session_state or not st.session_state.scoring_history:
        st.info("📊 No scoring history yet. Upload and score a resume to see analytics here.")
        return
    
    history = st.session_state.scoring_history
    
    # Score trend over time
    if len(history) > 1:
        dates = [entry["timestamp"] for entry in history]
        scores = [entry["score"] for entry in history]
        
        fig_trend = px.line(
            x=dates, 
            y=scores,
            title="Resume Score Trend",
            labels={"x": "Date", "y": "Score"}
        )
        fig_trend.update_traces(mode='markers+lines')
        st.plotly_chart(fig_trend, use_container_width=True)
    
    # Recent scores table
    st.markdown("### 📋 Recent Scores")
    
    for i, entry in enumerate(reversed(history[-5:])):  # Show last 5 entries
        with st.expander(f"📄 {entry['filename']} - Score: {entry['score']}/100"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Overall Score", f"{entry['score']}/100")
            
            with col2:
                st.metric("Target Role", entry['target_role'])
            
            with col3:
                st.metric("Date", entry['timestamp'].strftime("%Y-%m-%d"))

def render_improvement_tips():
    """Render general improvement tips and best practices"""
    
    st.markdown("### 💡 Resume Improvement Tips")
    
    tips_categories = {
        "🎯 Content Optimization": [
            "Use action verbs to start bullet points (e.g., 'Developed', 'Implemented', 'Led')",
            "Quantify achievements with specific numbers and percentages",
            "Tailor your resume for each job application",
            "Include relevant keywords from the job description",
            "Focus on accomplishments, not just job duties"
        ],
        "📝 Format & Structure": [
            "Keep it to 1-2 pages maximum",
            "Use consistent formatting and fonts",
            "Include clear section headers",
            "Use bullet points for easy scanning",
            "Ensure adequate white space"
        ],
        "🔧 Technical Skills": [
            "List technical skills relevant to your target role",
            "Include proficiency levels where appropriate",
            "Mention specific tools, frameworks, and technologies",
            "Add certifications and relevant coursework",
            "Include both hard and soft skills"
        ],
        "📊 ATS Optimization": [
            "Use standard section headings (Experience, Education, Skills)",
            "Avoid complex formatting, tables, and graphics",
            "Include keywords naturally throughout the resume",
            "Use common job titles and industry terms",
            "Save as both PDF and Word formats"
        ]
    }
    
    for category, tips in tips_categories.items():
        with st.expander(category):
            for tip in tips:
                st.markdown(f"• {tip}")
    
    # Interactive tip generator
    st.markdown("### 🎲 Get Personalized Tips")
    
    col1, col2 = st.columns(2)
    
    with col1:
        industry = st.selectbox(
            "Your Industry",
            ["Technology", "Healthcare", "Finance", "Marketing", "Sales", "Education", "Other"]
        )
    
    with col2:
        career_level = st.selectbox(
            "Career Level",
            ["Entry Level", "Mid Level", "Senior Level", "Executive"]
        )
    
    if st.button("Get Personalized Tips"):
        personalized_tips = get_personalized_tips(industry, career_level)
        
        st.markdown("#### 🎯 Tips for You:")
        for tip in personalized_tips:
            st.info(tip)

def get_personalized_tips(industry: str, career_level: str) -> list:
    """Generate personalized tips based on industry and career level"""
    
    tips = []
    
    # Industry-specific tips
    if industry == "Technology":
        tips.extend([
            "Highlight your GitHub profile and open-source contributions",
            "Include specific programming languages and frameworks",
            "Mention cloud platforms (AWS, Azure, GCP) if relevant"
        ])
    elif industry == "Healthcare":
        tips.extend([
            "Include relevant certifications and licenses",
            "Highlight patient care experience and outcomes",
            "Mention compliance with healthcare regulations"
        ])
    elif industry == "Finance":
        tips.extend([
            "Include financial modeling and analysis experience",
            "Mention relevant certifications (CFA, FRM, etc.)",
            "Highlight risk management and compliance experience"
        ])
    
    # Career level specific tips
    if career_level == "Entry Level":
        tips.extend([
            "Emphasize internships, projects, and relevant coursework",
            "Include volunteer work and extracurricular activities",
            "Focus on potential and eagerness to learn"
        ])
    elif career_level == "Senior Level":
        tips.extend([
            "Highlight leadership and mentoring experience",
            "Include strategic initiatives and business impact",
            "Mention team size and budget responsibility"
        ])
    
    return tips[:5]  # Return top 5 tips
