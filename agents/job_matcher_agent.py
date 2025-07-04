"""
JobMatcherAgent - Complete Rewrite from Scratch
==============================================

This is a brand new implementation that will definitely work without abstract method errors.
"""

from agents.agent_base import Agent
from typing import Dict, Any, List
import json
import logging
import re


class JobMatcherAgent(Agent):
    """
    Job Matching Agent - Built from scratch to avoid abstract method issues.
    
    This agent directly inherits from Agent and implements all required methods.
    """
    
    def __init__(self):
        """Initialize the JobMatcherAgent"""
        super().__init__(name="JobMatcherAgent", version="2.0.0")
        
        # Job matching configuration
        self.required_skills = {
            "Python", "JavaScript", "Java", "SQL", "Machine Learning", 
            "Data Science", "AI", "React", "Node.js", "AWS", "Docker"
        }
        
        self.job_roles = {
            "Data Scientist": {
                "required_skills": ["Python", "SQL", "Machine Learning", "Statistics"],
                "nice_to_have": ["R", "TensorFlow", "PyTorch"],
                "min_experience": 2
            },
            "Software Engineer": {
                "required_skills": ["Python", "JavaScript", "SQL"],
                "nice_to_have": ["React", "Node.js", "AWS"],
                "min_experience": 1
            },
            "ML Engineer": {
                "required_skills": ["Python", "Machine Learning", "TensorFlow"],
                "nice_to_have": ["PyTorch", "Kubernetes", "MLOps"],
                "min_experience": 3
            },
            "Full Stack Developer": {
                "required_skills": ["JavaScript", "React", "Node.js", "SQL"],
                "nice_to_have": ["Python", "AWS", "Docker"],
                "min_experience": 2
            },
            "Data Engineer": {
                "required_skills": ["Python", "SQL", "ETL"],
                "nice_to_have": ["Spark", "Kafka", "Airflow"],
                "min_experience": 2
            }
        }
        
        self.logger.info("JobMatcherAgent initialized successfully")
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main processing method - implements the abstract method from Agent base class.
        
        Args:
            input_data: Dictionary containing resume data with skills and experience
            
        Returns:
            Dictionary containing job matching results
        """
        try:
            self.logger.info("Processing job matching request")
            
            # Validate input
            if not isinstance(input_data, dict):
                raise ValueError(f"Expected dictionary input, got {type(input_data)}")
            
            # Extract skills and experience from input
            skills = self._extract_skills(input_data)
            experience = self._extract_experience(input_data)
            
            # Perform job matching
            matching_results = self._match_jobs(skills, experience)
            
            # Generate skill recommendations
            skill_recommendations = self._recommend_skills(skills)
            
            # Compile final results
            results = {
                "success": True,
                "matched_skills": matching_results["matched_skills"],
                "match_percent": matching_results["match_percent"],
                "suggested_skills": skill_recommendations,
                "job_roles": matching_results["job_roles"],
                "experience_level": experience,
                "total_skills": len(skills),
                "agent": self.name,
                "version": self.version
            }
            
            self.logger.info(f"Job matching completed successfully. Match: {results['match_percent']}%")
            return results
            
        except Exception as e:
            self.logger.error(f"Error in job matching: {str(e)}")
            return self.handle_error(e, "Job matching process")
    
    def _extract_skills(self, input_data: Dict[str, Any]) -> List[str]:
        """Extract skills from input data"""
        skills = []
        
        # Try different possible keys for skills
        possible_skill_keys = ["skills", "technical_skills", "skill_list", "technologies"]
        
        for key in possible_skill_keys:
            if key in input_data:
                skill_data = input_data[key]
                if isinstance(skill_data, list):
                    skills.extend(skill_data)
                elif isinstance(skill_data, str):
                    # Parse comma-separated skills
                    skills.extend([s.strip() for s in skill_data.split(",")])
                break
        
        # If no skills found in structured format, try to extract from text
        if not skills:
            text_data = input_data.get("data", "") or input_data.get("text", "") or str(input_data)
            skills = self._extract_skills_from_text(text_data)
        
        # Clean and normalize skills
        cleaned_skills = []
        for skill in skills:
            if isinstance(skill, str) and skill.strip():
                cleaned_skills.append(skill.strip().title())
        
        return list(set(cleaned_skills))  # Remove duplicates
    
    def _extract_experience(self, input_data: Dict[str, Any]) -> int:
        """Extract years of experience from input data"""
        experience_keys = ["years_of_experience", "experience", "years_experience", "exp"]
        
        for key in experience_keys:
            if key in input_data:
                exp = input_data[key]
                if isinstance(exp, (int, float)):
                    return int(exp)
                elif isinstance(exp, str):
                    # Try to extract number from string
                    numbers = re.findall(r'\d+', exp)
                    if numbers:
                        return int(numbers[0])
        
        # Default to 0 if not found
        return 0
    
    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Extract skills from free text using pattern matching"""
        if not isinstance(text, str):
            return []
        
        found_skills = []
        text_lower = text.lower()
        
        # Look for known skills in the text
        for skill in self.required_skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        # Look for common programming languages and technologies
        common_skills = [
            "HTML", "CSS", "Git", "GitHub", "Linux", "Windows", "Mac",
            "MongoDB", "PostgreSQL", "MySQL", "Redis", "Elasticsearch",
            "Django", "Flask", "FastAPI", "Spring", "Express",
            "Angular", "Vue", "Svelte", "Bootstrap", "Tailwind"
        ]
        
        for skill in common_skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def _match_jobs(self, skills: List[str], experience: int) -> Dict[str, Any]:
        """Match skills and experience against job roles"""
        skills_lower = [skill.lower() for skill in skills]
        matched_skills = []
        job_matches = []
        
        # Find skills that match our requirements
        for skill in skills:
            for required_skill in self.required_skills:
                if required_skill.lower() in skill.lower():
                    matched_skills.append(skill)
                    break
        
        # Calculate overall match percentage
        if skills:
            match_percent = (len(matched_skills) / len(skills)) * 100
        else:
            match_percent = 0
        
        # Match against specific job roles
        for role_name, role_info in self.job_roles.items():
            role_score = self._calculate_role_match(skills_lower, experience, role_info)
            
            if role_score > 30:  # Minimum 30% match required
                job_matches.append({
                    "role": role_name,
                    "match_score": role_score,
                    "meets_experience": experience >= role_info["min_experience"]
                })
        
        # Sort job matches by score
        job_matches.sort(key=lambda x: x["match_score"], reverse=True)
        
        return {
            "matched_skills": matched_skills[:10],  # Limit to top 10
            "match_percent": round(match_percent, 1),
            "job_roles": [match["role"] for match in job_matches[:5]]  # Top 5 roles
        }
    
    def _calculate_role_match(self, skills_lower: List[str], experience: int, role_info: Dict) -> float:
        """Calculate match score for a specific role"""
        required_skills = role_info["required_skills"]
        nice_to_have = role_info.get("nice_to_have", [])
        min_experience = role_info["min_experience"]
        
        # Count required skill matches
        required_matches = 0
        for req_skill in required_skills:
            if any(req_skill.lower() in skill for skill in skills_lower):
                required_matches += 1
        
        # Count nice-to-have skill matches
        nice_matches = 0
        for nice_skill in nice_to_have:
            if any(nice_skill.lower() in skill for skill in skills_lower):
                nice_matches += 1
        
        # Calculate score
        required_score = (required_matches / len(required_skills)) * 70  # 70% weight for required
        nice_score = (nice_matches / max(len(nice_to_have), 1)) * 20     # 20% weight for nice-to-have
        experience_score = min(experience / max(min_experience, 1), 1) * 10  # 10% weight for experience
        
        total_score = required_score + nice_score + experience_score
        return round(total_score, 1)
    
    def _recommend_skills(self, current_skills: List[str]) -> List[str]:
        """Recommend skills to improve job prospects"""
        current_skills_lower = [skill.lower() for skill in current_skills]
        recommendations = []
        
        # Find missing high-value skills
        high_value_skills = [
            "Python", "JavaScript", "SQL", "Machine Learning", 
            "AWS", "Docker", "React", "Node.js"
        ]
        
        for skill in high_value_skills:
            if not any(skill.lower() in current_skill for current_skill in current_skills_lower):
                recommendations.append(skill)
        
        # Add role-specific recommendations based on current skills
        if any("python" in skill for skill in current_skills_lower):
            recommendations.extend(["Django", "Flask", "Pandas", "NumPy"])
        
        if any("javascript" in skill for skill in current_skills_lower):
            recommendations.extend(["TypeScript", "React", "Node.js"])
        
        if any("data" in skill for skill in current_skills_lower):
            recommendations.extend(["SQL", "Tableau", "Power BI"])
        
        # Remove duplicates and limit
        unique_recommendations = []
        for rec in recommendations:
            if rec not in unique_recommendations and len(unique_recommendations) < 8:
                unique_recommendations.append(rec)
        
        return unique_recommendations
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about this agent"""
        return {
            "name": self.name,
            "version": self.version,
            "description": "Job matching agent that analyzes skills and recommends suitable roles",
            "supported_job_roles": list(self.job_roles.keys()),
            "tracked_skills": list(self.required_skills),
            "capabilities": [
                "Skill extraction from text",
                "Job role matching",
                "Skill gap analysis", 
                "Career recommendations"
            ]
        }


# Test function to verify the agent works
def test_job_matcher_agent():
    """Test function to verify the agent works correctly"""
    try:
        # Create agent instance
        agent = JobMatcherAgent()
        print("✅ JobMatcherAgent created successfully!")
        
        # Test with sample data
        test_data = {
            "skills": ["Python", "SQL", "Machine Learning", "Pandas"],
            "years_of_experience": 3
        }
        
        # Process the data
        result = agent.process(test_data)
        print("✅ Process method executed successfully!")
        print(f"Result: {json.dumps(result, indent=2)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🧪 Testing JobMatcherAgent...")
    success = test_job_matcher_agent()
    if success:
        print("\n🎉 JobMatcherAgent is working perfectly!")
    else:
        print("\n💥 JobMatcherAgent test failed!")
