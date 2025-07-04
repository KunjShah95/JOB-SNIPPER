from agents.multi_ai_base import MultiAIAgent
from agents.message_protocol import AgentMessage
import json
import logging
import re
from typing import Dict, Any


class JobMatcherAgent(MultiAIAgent):
    """Job Matching Agent that analyzes resumes and matches them with suitable job roles.
    
    This agent implements the abstract process method from the Agent base class
    and provides comprehensive job matching functionality.
    """
    
    def __init__(self):
        super().__init__(
            name="JobMatcherAgent",
            use_gemini=True,
            use_mistral=True,
            return_mode="compare"  # Use compare to see both model outputs
        )
        self.required_skills = {"Python", "AI", "ML", "SQL", "Data Science", "NLP"}
        self.job_roles = {
            "Data Scientist": ["Python", "ML", "SQL", "Statistics"],
            "ML Engineer": ["Python", "ML", "TensorFlow", "PyTorch"],
            "Data Engineer": ["Python", "SQL", "ETL", "Spark"],
            "AI Researcher": ["AI", "NLP", "ML", "PyTorch"],
            "Software Engineer": ["Java", "Python", "JavaScript", "AWS"],
        }

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Implementation of abstract process method from Agent base class
        
        Args:
            input_data: Dictionary containing resume data with skills and experience
            
        Returns:
            Dictionary containing job matching results
        """
        try:
            # Validate input
            if not isinstance(input_data, dict):
                raise ValueError(f"Expected dict input, got {type(input_data)}")
            
            # Convert input_data to the expected message format for run() method
            if isinstance(input_data, dict) and 'data' in input_data:
                # If input_data already has the expected structure
                message = AgentMessage(sender="user", recipient=self.name, data=input_data['data'])
                result_json = self.run(message.to_json())
            else:
                # Assume input_data is the parsed resume data directly
                message = AgentMessage(sender="user", recipient=self.name, data=input_data)
                result_json = self.run(message.to_json())
            
            # Parse the result
            result = json.loads(result_json) if isinstance(result_json, str) else result_json
            
            # Extract the actual data from the message format
            if isinstance(result, dict) and 'data' in result:
                return result['data']
            else:
                return result
                
        except Exception as e:
            logging.error(f"Error in JobMatcherAgent.process: {e}")
            return self.fallback_matching(input_data)

    def run(self, message_json):
        """Process job matching request using AI models"""
        try:
            msg = AgentMessage.from_json(message_json)
            parsed_resume = msg.data

            # Handle various input formats
            if isinstance(parsed_resume, str):
                try:
                    parsed_resume = json.loads(parsed_resume)
                except json.JSONDecodeError as e:
                    logging.error(f"Failed to decode resume JSON: {e}")
                    parsed_resume = {"skills": []}

            if not isinstance(parsed_resume, dict):
                logging.error(f"Expected dict, got {type(parsed_resume)}")
                parsed_resume = {"skills": []}

            if "skills" not in parsed_resume or not isinstance(parsed_resume["skills"], list):
                logging.warning("No skills found in parsed resume or skills not in list format")
                parsed_resume["skills"] = []

            prompt = f"""Analyze these skills from a resume and provide job matching information in JSON format:

Resume Skills: {parsed_resume.get("skills", [])}

Years of Experience: {parsed_resume.get("years_of_experience", 0)}

Provide the following in your response:
1. matched_skills: A list of skills that match with top job requirements
2. match_percent: A percentage (0-100) of how well the skills match job requirements
3. suggested_skills: A list of skills the candidate should acquire to improve employability
4. job_roles: A list of job roles that match well with the candidate's skills

Return ONLY valid JSON with these fields. No additional text."""

            try:
                response = self.generate_response(prompt)
                
                # Clean and parse the response
                cleaned_response = self.clean_json_response(response)
                match_data = json.loads(cleaned_response)
                
                # Validate and enhance the match data
                match_data = self.validate_and_enhance_match_data(match_data, parsed_resume)
                
            except Exception as e:
                logging.error(f"AI matching failed: {e}")
                match_data = self.fallback_matching(parsed_resume)

            # Return as AgentMessage
            response = AgentMessage(
                sender=self.name,
                recipient=msg.sender,
                data=match_data
            )
            return response.to_json()
            
        except Exception as e:
            logging.error(f"Error in JobMatcherAgent.run: {e}")
            # Return fallback response in proper format
            fallback_data = self.get_fallback_response()
            response = AgentMessage(
                sender=self.name,
                recipient="user",
                data=fallback_data
            )
            return response.to_json()

    def clean_json_response(self, response):
        """Clean AI response to extract valid JSON"""
        if not response:
            raise ValueError("Empty response")
        
        # Handle multiple AI responses
        if isinstance(response, dict) and "responses" in response:
            # Try each provider response
            for provider in ["gemini", "mistral"]:
                if provider in response["responses"]:
                    provider_response = response["responses"][provider]
                    try:
                        return self._extract_json_from_text(provider_response)
                    except:
                        continue
            raise ValueError("No valid JSON found in any provider response")
        else:
            return self._extract_json_from_text(str(response))

    def _extract_json_from_text(self, text):
        """Extract JSON from text response"""
        # Remove markdown formatting
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*$', '', text)
        
        # Find JSON object
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json_match.group(0)
        else:
            raise ValueError("No JSON object found in response")

    def validate_and_enhance_match_data(self, match_data, parsed_resume):
        """Validate and enhance match data"""
        if not isinstance(match_data, dict):
            raise ValueError("Match data is not a dictionary")
        
        # Ensure required fields exist
        required_fields = ['matched_skills', 'match_percent', 'suggested_skills', 'job_roles']
        for field in required_fields:
            if field not in match_data:
                match_data[field] = [] if field != 'match_percent' else 0
        
        # Validate match_percent
        if not isinstance(match_data['match_percent'], (int, float)):
            match_data['match_percent'] = 0
        match_data['match_percent'] = max(0, min(100, match_data['match_percent']))
        
        # Ensure lists are actually lists
        for list_field in ['matched_skills', 'suggested_skills', 'job_roles']:
            if not isinstance(match_data[list_field], list):
                match_data[list_field] = []
        
        # Add fallback matching if AI didn't provide good results
        if match_data['match_percent'] == 0 and parsed_resume.get('skills'):
            fallback_data = self.fallback_matching(parsed_resume)
            for key in required_fields:
                if not match_data[key] and fallback_data.get(key):
                    match_data[key] = fallback_data[key]
        
        return match_data

    def fallback_matching(self, parsed_resume):
        """Fallback matching using rule-based approach"""
        logging.info("Using fallback matching method")
        
        skills = parsed_resume.get("skills", []) if isinstance(parsed_resume, dict) else []
        if isinstance(skills, str):
            skills = [skills]
        
        # Convert to lowercase for matching
        skills_lower = [skill.lower() for skill in skills]
        
        # Find matched skills
        matched_skills = []
        for skill in skills:
            for required_skill in self.required_skills:
                if required_skill.lower() in skill.lower():
                    matched_skills.append(skill)
                    break
        
        # Calculate match percentage
        if skills:
            match_percent = min(100, (len(matched_skills) / len(skills)) * 100)
        else:
            match_percent = 0
        
        # Suggest skills
        suggested_skills = []
        for required_skill in self.required_skills:
            if not any(required_skill.lower() in skill.lower() for skill in skills_lower):
                suggested_skills.append(required_skill)
        
        # Find matching job roles
        matching_roles = []
        for role, role_skills in self.job_roles.items():
            role_match_count = sum(1 for role_skill in role_skills 
                                 if any(role_skill.lower() in skill.lower() for skill in skills_lower))
            if role_match_count > 0:
                matching_roles.append(role)
        
        return {
            "matched_skills": matched_skills[:10],  # Limit to 10
            "match_percent": round(match_percent, 1),
            "suggested_skills": suggested_skills[:8],  # Limit to 8
            "job_roles": matching_roles[:5]  # Limit to 5
        }

    def get_fallback_response(self, parsed_resume=None):
        """Get fallback response when all matching fails"""
        return {
            "matched_skills": [],
            "match_percent": 0,
            "suggested_skills": ["Python", "SQL", "Machine Learning"],
            "job_roles": ["Entry Level Positions"]
        }
