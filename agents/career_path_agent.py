from agents.multi_ai_base import MultiAIAgent
import logging


class CareerPathAgent(MultiAIAgent):
    """AI Agent for career path analysis and visualization"""
    
    def __init__(self):
        super().__init__(
            name="CareerPathAgent",
            use_gemini=True,
            use_mistral=True,
            return_mode="compare"
        )

    def run(self, resume_data, career_goals, industry="technology"):
        """Generate career path analysis and roadmap"""
        try:
            return self._generate_career_path(resume_data, career_goals, industry)
        except Exception as e:
            logging.error(f"Error generating career path: {e}")
            return self._get_fallback_career_path(career_goals)

    def _generate_career_path(self, resume_data, career_goals, industry):
        """Generate AI-powered career path analysis"""
        
        prompt = f"""
        Create a comprehensive career path analysis for this professional:
        
        Current Background:
        - Skills: {', '.join(resume_data.get('skills', [])[:15])}
        - Experience: {resume_data.get('experience', '')}
        - Education: {resume_data.get('education', '')}
        
        Career Goals: {career_goals}
        Industry: {industry}
        
        Generate:
        1. Current position assessment
        2. 3 potential career paths with timelines
        3. Required skills for each path
        4. Salary progression estimates
        5. Industry trends and opportunities
        6. Recommended certifications and training
        7. Networking strategies
        8. Action plan for next 6 months
        
        Format as structured analysis with clear progression steps.
        """
        
        try:
            response = self.generate_ai_response(prompt)
            return self._parse_career_response(response, industry)
        except Exception:
            return self._get_fallback_career_path(career_goals)

    def _parse_career_response(self, response, industry):
        """Parse career path response into structured format"""
        return {
            "analysis": response,
            "paths": self._extract_career_paths(response),
            "skills_needed": self._extract_skills_needed(response),
            "timeline": self._extract_timeline(response),
            "salary_progression": self._generate_salary_data(industry),
            "action_items": self._extract_action_items(response)
        }

    def _generate_salary_data(self, industry):
        """Generate salary progression data for visualization"""
        base_salaries = {
            "technology": [65000, 85000, 110000, 140000, 180000],
            "finance": [60000, 80000, 105000, 135000, 170000],
            "healthcare": [55000, 75000, 95000, 120000, 150000],
            "marketing": [50000, 65000, 85000, 110000, 140000]
        }
        
        salaries = base_salaries.get(industry.lower(), base_salaries["technology"])
        
        return {
            "years": [0, 2, 5, 8, 12],
            "salaries": salaries,
            "positions": ["Entry Level", "Mid Level", "Senior", "Lead", "Executive"]
        }

    def _get_fallback_career_path(self, career_goals):
        """Fallback career path when AI is unavailable"""
        return {
            "analysis":     """
# 🚀 Career Path Analysis

## 🎯 Current Assessment
Based on your background, you have strong potential for growth in your chosen field.

## 📈 Recommended Career Paths

### Path 1: Technical Leadership Track
- **Years 1-2**: Senior Individual Contributor
- **Years 3-5**: Team Lead / Technical Lead  
- **Years 6-8**: Engineering Manager
- **Years 9+**: Director of Engineering

### Path 2: Specialist Expert Track
- **Years 1-2**: Senior Specialist
- **Years 3-5**: Principal Specialist
- **Years 6-8**: Distinguished Engineer
- **Years 9+**: Chief Technology Officer

### Path 3: Product & Strategy Track
- **Years 1-2**: Senior Product Developer
- **Years 3-5**: Product Manager
- **Years 6-8**: Senior Product Manager
- **Years 9+**: VP of Product

## 🎓 Skill Development Priorities
1. Leadership and communication skills
2. Strategic thinking and planning
3. Industry-specific technical expertise
4. Project management capabilities
5. Business acumen and market understanding

## 💰 Salary Progression
- Current Level: $65,000 - $85,000
- 2-3 Years: $85,000 - $110,000
- 5-7 Years: $110,000 - $140,000
- 8+ Years: $140,000 - $200,000+

## 📋 Next Steps
1. Identify specific skills gaps
2. Create learning and development plan
3. Build professional network
4. Seek mentorship opportunities
5. Consider relevant certifications
            """,
            "paths": [
                {"name": "Technical Leadership", "timeline": "5-8 years", "growth": "High"},
                {"name": "Specialist Expert", "timeline": "6-10 years", "growth": "Medium"},
                {"name": "Product Strategy", "timeline": "4-7 years", "growth": "High"}
            ],
            "skills_needed": [
                "Leadership", "Communication", "Strategic Thinking", 
                "Project Management", "Business Acumen"
            ],
            "timeline": {
                "short_term": "Focus on current role excellence",
                "medium_term": "Develop leadership skills",
                "long_term": "Transition to management or specialist role"
            },
            "salary_progression": self._generate_salary_data("technology"),
            "action_items": [
                "Complete leadership training",
                "Join professional associations",
                "Seek mentorship",
                "Build portfolio of achievements"
            ]
        }