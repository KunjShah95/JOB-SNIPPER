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
    # Add content offset for fixed navbar
    st.markdown('<div class="jobsniper-content-offset">', unsafe_allow_html=True)

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

    st.markdown('</div>', unsafe_allow_html=True)

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
    """Get resume score using the actual ResumeScorerAgent"""
    
    try:
        from agents.resume_scorer_agent import ResumeScorerAgent
        from agents.message_protocol import AgentMessage
        
        # Initialize the scorer agent
        scorer = ResumeScorerAgent()
        
        # Prepare scoring input
        scoring_input = {
            "resume_text": resume_text,
            "target_role": target_role,
            "experience_level": experience_level
        }
        
        # Create message for scorer agent
        msg = AgentMessage("ResumeScoringPage", "ResumeScorerAgent", scoring_input)
        
        # Run scoring agent
        scoring_response = scorer.run(msg.to_json())
        scoring_msg = AgentMessage.from_json(scoring_response)
        
        # Get the scoring result
        result = scoring_msg.data
        
        # Ensure all required fields are present
        if not isinstance(result, dict):
            # Fallback to mock if result is not a dict
            return get_mock_score(resume_text, target_role, experience_level)
        
        # Validate and enhance the result
        result = validate_scoring_result(result)
        
        return result
        
    except Exception as e:
        st.warning(f"⚠️ AI scoring failed, using fallback method: {str(e)}")
        # Fallback to mock scoring
        return get_mock_score(resume_text, target_role, experience_level)

def get_mock_score(resume_text: str, target_role: str, experience_level: str) -> Dict[str, Any]:
    """Fallback mock scoring when AI fails"""
    
    import random
    
    # Analyze resume content for better scoring
    word_count = len(resume_text.split())
    has_skills = any(keyword in resume_text.lower() for keyword in ['python', 'java', 'javascript', 'sql', 'aws', 'docker'])
    has_experience = any(keyword in resume_text.lower() for keyword in ['experience', 'worked', 'developed', 'managed'])
    has_education = any(keyword in resume_text.lower() for keyword in ['bachelor', 'master', 'degree', 'university'])
    
    # Calculate scores based on content analysis
    base_score = min(word_count // 15, 70)  # Better base score calculation
    
    # Technical skills score (0-25)
    tech_score = 15 if has_skills else 8
    tech_score += min(len([w for w in resume_text.split() if w.lower() in ['python', 'java', 'sql', 'aws']]), 10)
    tech_score = min(tech_score, 25)
    
    # Experience relevance score (0-25)
    exp_score = 15 if has_experience else 8
    if experience_level == "Senior Level":
        exp_score += 7
    elif experience_level == "Mid Level":
        exp_score += 4
    exp_score = min(exp_score, 25)
    
    # Education alignment score (0-20)
    edu_score = 15 if has_education else 8
    edu_score = min(edu_score, 20)
    
    # Format structure score (0-15)
    format_score = min(word_count // 50, 12)  # Better format scoring
    format_score = min(format_score, 15)
    
    # Keywords density score (0-15)
    keyword_score = min(len([w for w in resume_text.lower().split() if w in ['project', 'team', 'leadership', 'analysis']]), 12)
    keyword_score = min(keyword_score, 15)
    
    scores = {
        "technical_skills": tech_score,
        "experience_relevance": exp_score,
        "education_alignment": edu_score,
        "format_structure": format_score,
        "keywords_density": keyword_score
    }
    
    overall_score = sum(scores.values())
    
    # Dynamic strengths based on content
    strengths = []
    if has_skills:
        strengths.append("Strong technical skill set")
    if has_experience:
        strengths.append("Relevant professional experience")
    if has_education:
        strengths.append("Solid educational background")
    if word_count > 300:
        strengths.append("Comprehensive content coverage")
    if any(keyword in resume_text.lower() for keyword in ['leadership', 'team', 'managed']):
        strengths.append("Leadership experience")
    
    # Dynamic improvements based on missing elements
    improvements = []
    if not has_skills:
        improvements.append("Add more technical skills relevant to your field")
    if not has_experience:
        improvements.append("Include detailed work experience descriptions")
    if not has_education:
        improvements.append("Add educational background and qualifications")
    if word_count < 200:
        improvements.append("Expand on your experience and achievements")
    if overall_score < 70:
        improvements.append("Include quantified achievements and metrics")
    
    # Dynamic missing skills based on target role
    missing_skills = []
    if target_role == "Software Engineer":
        missing_skills = ["System Design", "API Development", "Testing Frameworks", "Version Control"]
    elif target_role == "Data Scientist":
        missing_skills = ["Machine Learning", "Statistical Analysis", "Data Visualization", "Python Libraries"]
    elif target_role == "Product Manager":
        missing_skills = ["Product Strategy", "User Research", "Agile Methodologies", "Data Analysis"]
    else:
        missing_skills = ["Cloud Computing", "API Development", "Agile Methodologies", "Data Analysis"]
    
    return {
        "overall_score": overall_score,
        "breakdown": scores,
        "strengths": strengths[:5],
        "improvements": improvements[:5],
        "missing_skills": missing_skills[:5],
        "industry_match": target_role if target_role != "General" else "Technology",
        "experience_level": experience_level if experience_level != "Auto-detect" else "Mid-Level",
        "timestamp": datetime.now().isoformat(),
        "scoring_method": "content_analysis"
    }

def validate_scoring_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and ensure all required fields are present in scoring result"""
    
    # Required fields with defaults
    required_fields = {
        "overall_score": 0,
        "breakdown": {},
        "strengths": [],
        "improvements": [],
        "missing_skills": [],
        "industry_match": "General",
        "experience_level": "Junior",
        "scoring_method": "unknown"
    }
    
    # Ensure all required fields exist
    for field, default in required_fields.items():
        if field not in result:
            result[field] = default
    
    # Validate score ranges
    if result["overall_score"] > 100:
        result["overall_score"] = 100
    elif result["overall_score"] < 0:
        result["overall_score"] = 0
    
    # Ensure breakdown has all components
    breakdown_defaults = {
        "technical_skills": 0,
        "experience_relevance": 0,
        "education_alignment": 0,
        "format_structure": 0,
        "keywords_density": 0
    }
    
    if "breakdown" not in result:
        result["breakdown"] = breakdown_defaults
    else:
        for key, default in breakdown_defaults.items():
            if key not in result["breakdown"]:
                result["breakdown"][key] = default
    
    # Ensure lists are actually lists
    list_fields = ["strengths", "improvements", "missing_skills"]
    for field in list_fields:
        if not isinstance(result[field], list):
            result[field] = []
    
    # Add timestamp if missing
    if "timestamp" not in result:
        result["timestamp"] = datetime.now().isoformat()
    
    return result

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
