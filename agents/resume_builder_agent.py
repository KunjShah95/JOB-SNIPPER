from agents.multi_ai_base import MultiAIAgent
import logging
from typing import Dict, List


class ResumeBuilderAgent(MultiAIAgent):
    """Advanced AI-powered resume builder with multiple templates and optimization"""
    
    def __init__(self):
        super().__init__(
            name="ResumeBuilderAgent",
            use_gemini=True,
            use_mistral=True,
            return_mode="compare"
        )
    
    def build_resume(self, user_data: Dict, target_job: Dict = None, template_style: str = "professional") -> Dict:
        """Build a complete resume from user data"""
        try:
            # Generate different sections
            sections = {
                "header": self._generate_header(user_data),
                "professional_summary": self._generate_summary(user_data, target_job),
                "experience": self._generate_experience_section(user_data, target_job),
                "education": self._generate_education_section(user_data),
                "skills": self._generate_skills_section(user_data, target_job),
                "projects": self._generate_projects_section(user_data),
                "certifications": self._generate_certifications_section(user_data),
                "additional": self._generate_additional_sections(user_data)
            }
            
            # Apply template formatting
            formatted_resume = self._apply_template(sections, template_style)
            
            # Generate ATS optimization suggestions
            ats_optimization = self._generate_ats_optimization(sections, target_job)
            
            return {
                "success": True,
                "resume_sections": sections,
                "formatted_resume": formatted_resume,
                "ats_optimization": ats_optimization,
                "template_style": template_style,
                "word_count": self._count_words(formatted_resume),
                "ats_score": self._calculate_ats_score(sections, target_job)
            }
            
        except Exception as e:
            logging.error(f"Error building resume: {e}")
            return self._fallback_resume_builder(user_data)
    
    def optimize_for_job(self, existing_resume: Dict, target_job: Dict) -> Dict:
        """Optimize existing resume for specific job"""
        try:
            optimization_prompt = f"""
            Optimize this resume for the target job:
            
            Target Job: {target_job.get('title', '')}
            Company: {target_job.get('company', '')}
            Job Description: {target_job.get('description', '')[:1500]}
            
            Current Resume Sections:
            {str(existing_resume)[:2000]}
            
            Provide specific optimization recommendations:
            1. Keywords to add/emphasize
            2. Skills to highlight
            3. Experience points to modify
            4. New achievements to include
            5. Sections to reorder
            6. ATS optimization tips
            
            Return as structured JSON with specific actionable changes.
            """
            
            optimization_response = self.generate_ai_response(optimization_prompt)
            
            return {
                "success": True,
                "optimizations": optimization_response,
                "target_job": target_job.get('title', ''),
                "match_improvement": "15-25% expected increase in ATS compatibility"
            }
            
        except Exception as e:
            logging.error(f"Error optimizing resume: {e}")
            return {"success": False, "error": str(e)}
    
    def _generate_header(self, user_data: Dict) -> Dict:
        """Generate professional header section"""
        return {
            "name": user_data.get("full_name", ""),
            "title": user_data.get("professional_title", ""),
            "email": user_data.get("email", ""),
            "phone": user_data.get("phone", ""),
            "location": user_data.get("location", ""),
            "linkedin": user_data.get("linkedin_url", ""),
            "portfolio": user_data.get("portfolio_url", ""),
            "github": user_data.get("github_url", "")
        }
    
    def _generate_summary(self, user_data: Dict, target_job: Dict = None) -> str:
        """Generate AI-powered professional summary"""
        
        prompt = f"""
        Create a compelling professional summary for this candidate:
        
        Background:
        - Experience: {user_data.get('years_experience', 0)} years
        - Current Role: {user_data.get('current_role', '')}
        - Key Skills: {', '.join(user_data.get('skills', [])[:10])}
        - Industry: {user_data.get('industry', '')}
        - Achievements: {', '.join(user_data.get('achievements', [])[:3])}
        
        Target Role: {target_job.get('title', '') if target_job else 'General'}
        
        Create a 3-4 sentence professional summary that:
        1. Highlights relevant experience and expertise
        2. Showcases key achievements with metrics
        3. Aligns with target role requirements
        4. Uses strong action words and industry keywords
        
        Make it compelling and ATS-friendly.
        """
        
        try:
            return self.generate_ai_response(prompt)
        except Exception:
            return f"Experienced professional with {user_data.get('years_experience', 'several')} years in {user_data.get('industry', 'the field')}, specializing in {', '.join(user_data.get('skills', ['various technologies'])[:3])}. Proven track record of delivering results and driving innovation."
    
    def _generate_experience_section(self, user_data: Dict, target_job: Dict = None) -> List[Dict]:
        """Generate optimized work experience section"""
        
        experiences = user_data.get('work_experience', [])
        optimized_experiences = []
        
        for exp in experiences:
            prompt = f"""
            Optimize this work experience for a resume:
            
            Company: {exp.get('company', '')}
            Role: {exp.get('title', '')}
            Duration: {exp.get('start_date', '')} - {exp.get('end_date', 'Present')}
            Responsibilities: {exp.get('description', '')}
            
            Target Role: {target_job.get('title', '') if target_job else 'General'}
            
            Create 4-6 bullet points that:
            1. Start with strong action verbs
            2. Include quantifiable achievements
            3. Highlight relevant skills and technologies
            4. Show progression and impact
            5. Use keywords from target job description
            
            Format as bullet points with metrics where possible.
            """
            
            try:
                optimized_bullets = self.generate_ai_response(prompt)
                optimized_experiences.append({
                    "company": exp.get('company', ''),
                    "title": exp.get('title', ''),
                    "duration": f"{exp.get('start_date', '')} - {exp.get('end_date', 'Present')}",
                    "location": exp.get('location', ''),
                    "bullets": optimized_bullets.split('\n') if optimized_bullets else []
                })
            except Exception:
                # Fallback formatting
                optimized_experiences.append({
                    "company": exp.get('company', ''),
                    "title": exp.get('title', ''),
                    "duration": f"{exp.get('start_date', '')} - {exp.get('end_date', 'Present')}",
                    "location": exp.get('location', ''),
                    "bullets": [exp.get('description', '')]
                })
        
        return optimized_experiences
    
    def _generate_skills_section(self, user_data: Dict, target_job: Dict = None) -> Dict:
        """Generate categorized skills section"""
        
        all_skills = user_data.get('skills', [])
        
        # Categorize skills using AI
        prompt = f"""
        Categorize these skills into relevant groups for a resume:
        
        Skills: {', '.join(all_skills)}
        Target Job: {target_job.get('title', '') if target_job else 'General'}
        
        Organize into categories like:
        - Technical Skills
        - Programming Languages
        - Frameworks & Tools
        - Soft Skills
        - Certifications
        - Languages
        
        Prioritize skills most relevant to the target role.
        Return as JSON with categories and skills arrays.
        """
        
        try:
            categorized_response = self.generate_ai_response(prompt)
            import json
            return json.loads(categorized_response)
        except Exception:
            # Fallback categorization
            return {
                "Technical Skills": all_skills[:8],
                "Tools & Technologies": all_skills[8:15] if len(all_skills) > 8 else [],
                "Soft Skills": ["Communication", "Leadership", "Problem Solving", "Team Collaboration"]
            }
    
    def _apply_template(self, sections: Dict, template_style: str) -> str:
        """Apply formatting template to resume sections"""
        
        templates = {
            "professional": self._professional_template,
            "modern": self._modern_template,
            "creative": self._creative_template,
            "ats_optimized": self._ats_template
        }
        
        template_func = templates.get(template_style, self._professional_template)
        return template_func(sections)
    
    def _professional_template(self, sections: Dict) -> str:
        """Professional resume template"""
        
        header = sections["header"]
        resume_content = f"""
# {header["name"]}
{header["title"]}

📧 {header["email"]} | 📱 {header["phone"]} | 📍 {header["location"]}
🔗 {header["linkedin"]} | 💼 {header["portfolio"]}

## PROFESSIONAL SUMMARY
{sections["professional_summary"]}

## PROFESSIONAL EXPERIENCE
"""
        
        for exp in sections["experience"]:
            resume_content += f"""
### {exp["title"]} | {exp["company"]}
*{exp["duration"]} | {exp["location"]}*

"""
            for bullet in exp["bullets"]:
                if bullet.strip():
                    resume_content += f"• {bullet.strip()}\n"

        resume_content += "\n\n## TECHNICAL SKILLS\n"

        skills = sections["skills"]
        for category, skill_list in skills.items():
            if skill_list:
                resume_content += f"**{category}:** {', '.join(skill_list)}\n"

        resume_content += f"""

## EDUCATION
{sections["education"]}

## PROJECTS
{sections["projects"]}
"""

        return resume_content
    
    def _calculate_ats_score(self, sections: Dict, target_job: Dict = None) -> int:
        """Calculate ATS compatibility score"""
        score = 70  # Base score
        
        # Check for key sections
        if sections.get("professional_summary"):
            score += 5
        if sections.get("skills"):
            score += 10
        if sections.get("experience"):
            score += 10
        
        # Check for keywords if target job provided
        if target_job and target_job.get("description"):
            job_keywords = target_job["description"].lower().split()
            resume_text = str(sections).lower()
            
            keyword_matches = sum(1 for keyword in job_keywords[:20] if keyword in resume_text)
            score += min(keyword_matches, 15)
        
        return min(score, 100)