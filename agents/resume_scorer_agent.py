"""
Resume Scorer Agent - AI-Powered Resume Evaluation
Integrates with existing JobSniper AI architecture
"""

from agents.multi_ai_base import MultiAIAgent
from agents.message_protocol import AgentMessage
import json
import re
import logging
from typing import Dict, List, Any
from datetime import datetime

class ResumeScorerAgent(MultiAIAgent):
    def __init__(self):
        super().__init__(
            name="ResumeScorerAgent",
            use_gemini=True,
            use_mistral=True,
            return_mode="compare"
        )
        
        # Scoring criteria weights
        self.scoring_weights = {
            "technical_skills": 25,
            "experience_relevance": 25,
            "education_alignment": 20,
            "format_structure": 15,
            "keywords_density": 15
        }
        
        # Industry-specific skill databases
        self.skill_databases = {
            "software_engineering": [
                "Python", "Java", "JavaScript", "React", "Node.js", "SQL", "Git",
                "AWS", "Docker", "Kubernetes", "MongoDB", "PostgreSQL", "Redis",
                "Machine Learning", "AI", "Data Science", "API", "REST", "GraphQL"
            ],
            "data_science": [
                "Python", "R", "SQL", "Machine Learning", "Deep Learning", "TensorFlow",
                "PyTorch", "Pandas", "NumPy", "Scikit-learn", "Tableau", "Power BI",
                "Statistics", "Data Visualization", "Big Data", "Spark", "Hadoop"
            ],
            "product_management": [
                "Product Strategy", "Roadmap", "Agile", "Scrum", "User Research",
                "A/B Testing", "Analytics", "Wireframing", "Stakeholder Management",
                "Go-to-Market", "Competitive Analysis", "KPIs", "OKRs"
            ]
        }

    def run(self, message_json):
        """Main scoring method"""
        msg = AgentMessage.from_json(message_json)
        
        # Handle different input formats
        if isinstance(msg.data, str):
            # If raw resume text
            resume_data = {"resume_text": msg.data}
        elif isinstance(msg.data, dict):
            # If parsed resume data
            resume_data = msg.data
        else:
            return AgentMessage(self.name, msg.sender, self._get_error_response()).to_json()

        try:
            # Generate comprehensive score
            scoring_result = self._score_resume(resume_data)
            return AgentMessage(self.name, msg.sender, scoring_result).to_json()
            
        except Exception as e:
            logging.error(f"Resume scoring failed: {e}")
            return AgentMessage(self.name, msg.sender, self._get_fallback_score()).to_json()

    def _score_resume(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive resume scoring"""
        
        # Extract resume text for analysis
        resume_text = resume_data.get("resume_text", "")
        if not resume_text and "parsed_data" in resume_data:
            # Reconstruct text from parsed data
            parsed = resume_data["parsed_data"]
            resume_text = self._reconstruct_text_from_parsed(parsed)

        # AI-powered scoring prompt
        scoring_prompt = f"""
        Analyze this resume and provide a detailed scoring breakdown:

        Resume Content:
        {resume_text}

        Evaluate based on these criteria (return JSON only):
        1. technical_skills (0-25): Relevance and depth of technical skills
        2. experience_relevance (0-25): Quality and relevance of work experience
        3. education_alignment (0-20): Educational background alignment
        4. format_structure (0-15): Resume formatting and organization
        5. keywords_density (0-15): Industry keyword optimization

        Also provide:
        - overall_score: Sum of all scores (0-100)
        - strengths: List of 3-5 key strengths
        - improvements: List of 3-5 improvement suggestions
        - missing_skills: List of skills that could enhance the profile
        - industry_match: Best matching industry/role
        - experience_level: Junior/Mid/Senior assessment

        Return ONLY valid JSON with these fields.
        """

        try:
            # Get AI response
            ai_response = self.generate_ai_response(scoring_prompt)
            
            # Parse AI response
            if isinstance(ai_response, dict) and "responses" in ai_response:
                # Use the best available response
                for provider in self.provider_priority:
                    if provider in ai_response["responses"]:
                        try:
                            response_text = ai_response["responses"][provider]
                            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                            if json_match:
                                response_text = json_match.group(0)
                                # Try to clean up the JSON string
                                response_text = self._clean_json_string(response_text)
                            parsed_score = json.loads(response_text)
                            break
                        except Exception as e:
                            logging.warning(f"Failed to parse {provider} scoring response: {e}")
                            continue
                else:
                    # Fallback to rule-based scoring
                    parsed_score = self._rule_based_scoring(resume_data)
            else:
                # Single response format
                try:
                    if isinstance(ai_response, str):
                        json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
                        if json_match:
                            ai_response = json_match.group(0)
                            ai_response = self._clean_json_string(ai_response)
                    parsed_score = json.loads(ai_response)
                except Exception as e:
                    logging.warning(f"Failed to parse AI scoring response: {e}")
                    parsed_score = self._rule_based_scoring(resume_data)

            # Validate and enhance the score
            final_score = self._validate_and_enhance_score(parsed_score, resume_data)
            
            return final_score

        except Exception as e:
            logging.error(f"AI scoring failed: {e}")
            return self._rule_based_scoring(resume_data)

    def _rule_based_scoring(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback rule-based scoring when AI fails"""
        
        resume_text = resume_data.get("resume_text", "")
        parsed_data = resume_data.get("parsed_data", {})
        
        scores = {}
        
        # Technical Skills Scoring (0-25)
        skills = parsed_data.get("skills", [])
        if isinstance(skills, str):
            skills = [s.strip() for s in skills.split(",")]
        
        tech_score = min(len(skills) * 2, 25)  # 2 points per skill, max 25
        scores["technical_skills"] = tech_score
        
        # Experience Relevance (0-25)
        years_exp = parsed_data.get("years_of_experience", 0)
        exp_score = min(years_exp * 3, 25)  # 3 points per year, max 25
        scores["experience_relevance"] = exp_score
        
        # Education Alignment (0-20)
        education = parsed_data.get("education", "")
        edu_score = 15 if any(degree in education.lower() for degree in 
                             ["bachelor", "master", "phd", "degree"]) else 10
        scores["education_alignment"] = edu_score
        
        # Format Structure (0-15)
        format_score = 12  # Assume decent format if parsed successfully
        scores["format_structure"] = format_score
        
        # Keywords Density (0-15)
        keyword_count = len(re.findall(r'\b(experience|skills|projects|achievements)\b', 
                                     resume_text.lower()))
        keyword_score = min(keyword_count * 2, 15)
        scores["keywords_density"] = keyword_score
        
        overall_score = sum(scores.values())
        
        return {
            "overall_score": overall_score,
            "breakdown": scores,
            "strengths": self._identify_strengths(parsed_data),
            "improvements": self._suggest_improvements(parsed_data, overall_score),
            "missing_skills": self._identify_missing_skills(skills),
            "industry_match": self._determine_industry_match(skills),
            "experience_level": self._assess_experience_level(years_exp),
            "timestamp": datetime.now().isoformat(),
            "scoring_method": "rule_based"
        }

    def _identify_strengths(self, parsed_data: Dict) -> List[str]:
        """Identify resume strengths"""
        strengths = []
        
        skills = parsed_data.get("skills", [])
        years_exp = parsed_data.get("years_of_experience", 0)
        
        if len(skills) > 10:
            strengths.append("Diverse technical skill set")
        
        if years_exp > 5:
            strengths.append("Extensive professional experience")
        
        if any(skill.lower() in ["leadership", "management", "team lead"] for skill in skills):
            strengths.append("Leadership experience")
        
        if any(skill.lower() in ["python", "java", "javascript"] for skill in skills):
            strengths.append("Strong programming foundation")
        
        return strengths[:5]  # Return top 5

    def _suggest_improvements(self, parsed_data: Dict, score: int) -> List[str]:
        """Suggest improvements based on score"""
        improvements = []
        
        if score < 60:
            improvements.append("Add more relevant technical skills")
            improvements.append("Include quantified achievements")
        
        if score < 70:
            improvements.append("Enhance work experience descriptions")
            improvements.append("Add industry-specific keywords")
        
        if score < 80:
            improvements.append("Include project details and outcomes")
        
        return improvements

    def _identify_missing_skills(self, current_skills: List[str]) -> List[str]:
        """Identify missing skills based on industry trends"""
        current_lower = [skill.lower() for skill in current_skills]
        
        # Common high-demand skills
        trending_skills = [
            "Cloud Computing", "AWS", "Docker", "Kubernetes", 
            "Machine Learning", "Data Analysis", "API Development"
        ]
        
        missing = [skill for skill in trending_skills 
                  if skill.lower() not in current_lower]
        
        return missing[:5]

    def _determine_industry_match(self, skills: List[str]) -> str:
        """Determine best industry match"""
        skill_lower = [s.lower() for s in skills]
        
        matches = {}
        for industry, industry_skills in self.skill_databases.items():
            match_count = sum(1 for skill in industry_skills 
                            if skill.lower() in skill_lower)
            matches[industry] = match_count
        
        best_match = max(matches, key=matches.get) if matches else "general"
        return best_match.replace("_", " ").title()

    def _assess_experience_level(self, years: int) -> str:
        """Assess experience level"""
        if years < 2:
            return "Junior"
        elif years < 5:
            return "Mid-Level"
        else:
            return "Senior"

    def _validate_and_enhance_score(self, score_data: Dict, resume_data: Dict) -> Dict:
        """Validate and enhance AI-generated scores"""
        
        # Ensure all required fields exist
        required_fields = {
            "overall_score": 0,
            "breakdown": {},
            "strengths": [],
            "improvements": [],
            "missing_skills": [],
            "industry_match": "General",
            "experience_level": "Junior"
        }
        
        for field, default in required_fields.items():
            if field not in score_data:
                score_data[field] = default
        
        # Validate score ranges
        if score_data["overall_score"] > 100:
            score_data["overall_score"] = 100
        elif score_data["overall_score"] < 0:
            score_data["overall_score"] = 0
        
        # Add metadata
        score_data["timestamp"] = datetime.now().isoformat()
        score_data["scoring_method"] = "ai_enhanced"
        score_data["agent_version"] = "1.0"
        
        return score_data

    def _reconstruct_text_from_parsed(self, parsed_data: Dict) -> str:
        """Reconstruct resume text from parsed data"""
        text_parts = []
        
        if "name" in parsed_data:
            text_parts.append(f"Name: {parsed_data['name']}")
        
        if "skills" in parsed_data:
            skills = parsed_data["skills"]
            if isinstance(skills, list):
                text_parts.append(f"Skills: {', '.join(skills)}")
            else:
                text_parts.append(f"Skills: {skills}")
        
        if "experience" in parsed_data:
            text_parts.append(f"Experience: {parsed_data['experience']}")
        
        if "education" in parsed_data:
            text_parts.append(f"Education: {parsed_data['education']}")
        
        return "\n".join(text_parts)

    def _get_fallback_score(self) -> Dict[str, Any]:
        """Provide fallback score when all methods fail"""
        return {
            "overall_score": 65,
            "breakdown": {
                "technical_skills": 15,
                "experience_relevance": 15,
                "education_alignment": 12,
                "format_structure": 12,
                "keywords_density": 11
            },
            "strengths": ["Professional presentation", "Clear structure"],
            "improvements": ["Add more technical details", "Include quantified achievements"],
            "missing_skills": ["Cloud Computing", "API Development"],
            "industry_match": "Technology",
            "experience_level": "Mid-Level",
            "timestamp": datetime.now().isoformat(),
            "scoring_method": "fallback"
        }

    def _get_error_response(self) -> Dict[str, Any]:
        """Return error response"""
        return {
            "error": "Invalid input format for resume scoring",
            "overall_score": 0,
            "timestamp": datetime.now().isoformat()
        }
    
    def _clean_json_string(self, json_str):
        """Clean up JSON string by removing markdown formatting and extra content"""
        import re
        # Remove markdown code blocks
        json_str = re.sub(r'```json\s*', '', json_str)
        json_str = re.sub(r'```\s*', '', json_str)
        
        # Remove any text before the first {
        first_brace = json_str.find('{')
        if first_brace > 0:
            json_str = json_str[first_brace:]
        
        # Remove any text after the last }
        last_brace = json_str.rfind('}')
        if last_brace >= 0 and last_brace < len(json_str) - 1:
            json_str = json_str[:last_brace + 1]
        
        # Remove trailing commas before closing braces/brackets
        json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
        
        return json_str.strip()
