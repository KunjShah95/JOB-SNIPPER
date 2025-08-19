"""Skill Recommendations Page for JobSniper AI

Personalized skill development recommendations with learning paths,
course suggestions, and career advancement guidance.
"""

import streamlit as st
from ui.components.quantum_components import quantum_header, quantum_card

def render():
    """Render the skill recommendations page"""
    
    quantum_header(
        title="Skill Recommendations",
        subtitle="Personalized learning paths and skill development guidance",
        icon="📚"
    )
    
    # Check if user has analyzed their resume
    if 'resume_analysis' in st.session_state:
        _render_personalized_recommendations()
    else:
        _render_general_recommendations()

def _render_personalized_recommendations():
    """Render personalized skill recommendations based on resume analysis"""
    st.subheader("🎯 Personalized Skill Recommendations")

    results = st.session_state['resume_analysis']

    # Get suggested skills from analysis
    if 'matched_data' in results and results['matched_data'].get('suggested_skills'):
        suggested_skills = results['matched_data']['suggested_skills']

        st.write("### 📚 Skills to Learn Next")
        st.write("Based on your resume analysis, here are skills that could boost your career:")

        for skill in suggested_skills:
            with st.expander(f"📖 Learn {skill}"):
                st.write(f"**Why learn {skill}?**")
                st.write("- High demand in current job market")
                st.write("- Complements your existing skills")
                st.write("- Could increase salary potential")

                st.write("**Learning Resources:**")
                st.write("- 🎓 Online courses (Coursera, Udemy, Pluralsight)")
                st.write("- 📖 Official documentation and tutorials")
                st.write("- 🛠️ Hands-on projects and practice")
                st.write("- 👥 Community forums and study groups")

    # Industry trends
    st.write("### 📈 Trending Skills in Your Field")
    trending_skills = ["Artificial Intelligence", "Cloud Computing", "DevOps", "Cybersecurity", "Data Analytics"]

    for skill in trending_skills:
        st.write(f"🔥 **{skill}** - High growth potential")

def _render_general_recommendations():
    """Render general skill recommendations"""
    quantum_card(
        title="📚 Skill Development Hub",
        content="""
        <div style="text-align: center; padding: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
            <h3>Get Personalized Skill Recommendations</h3>
            <p style="color: #6B7280; margin-bottom: 2rem;">
                Upload and analyze your resume first to get personalized skill recommendations!
            </p>
        </div>
        """,
        card_type="glass"
    )

    st.write("### 🔥 Currently Trending Skills")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Technical Skills:**")
        tech_skills = [
            "Artificial Intelligence", "Machine Learning", "Cloud Computing",
            "DevOps", "Cybersecurity", "Data Science", "React", "Python"
        ]
        for skill in tech_skills:
            st.write(f"• {skill}")

    with col2:
        st.write("**Soft Skills:**")
        soft_skills = [
            "Leadership", "Communication", "Problem Solving",
            "Project Management", "Adaptability", "Critical Thinking"
        ]
        for skill in soft_skills:
            st.write(f"• {skill}")

    st.info("💡 Analyze your resume in the Resume Analysis section to get personalized recommendations!")