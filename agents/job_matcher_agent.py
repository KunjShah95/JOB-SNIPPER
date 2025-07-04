from agents.multi_ai_base import MultiAIAgent
import json
import logging
import re
from typing import Dict, Any


class JobMatcherAgent(MultiAIAgent):
    def __init__(self):
        super().__init__(
            name="JobMatcherAgent",
            use_gemini=True,
            use_mistral=True,
            return_mode="compare",  # Use compare to see both model outputs
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
        from agents.message_protocol import AgentMessage
        if 'data' in input_data:
            # If input_data already has the expected structure
            message = AgentMessage(sender="user", recipient=self.name, data=input_data['data'])
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

        if "skills" not in parsed_resume or not isinstance(
            parsed_resume["skills"], list
        ):
            logging.warning(
                "No skills found in parsed resume or skills not in list format"
            )
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
            response = self.generate_ai_response(prompt)

            # Parse the AI response with robust error handling
            if isinstance(response, dict) and "responses" in response:
                # If we have multiple AI responses, try each one
                for provider in self.provider_priority:
                    if provider in response["responses"]:
                        try:
                            provider_response = response["responses"][provider]
                            # Try to extract JSON if wrapped in text
                            json_match = re.search(
                                r"{.*}", provider_response, re.DOTALL
                            )
                            if json_match:
                                provider_response = json_match.group(0)
                            matched = json.loads(provider_response)
                            break
                        except Exception as e:
                            logging.warning(f"Failed to parse {provider} response: {e}")
                            continue
                else:
                    # If none of the responses parsed, use fallback
                    matched = self.fallback_matching(parsed_resume)
            else:
                # Try to parse the response as JSON
                try:
                    # If response is string, try to extract JSON if wrapped in text
                    if isinstance(response, str):
                        json_match = re.search(r"{.*}", response, re.DOTALL)
                        if json_match:
                            response = json_match.group(0)
                    matched = json.loads(response)
                except Exception as e:
                    logging.warning(f"Failed to parse job matcher JSON response: {e}")
                    matched = self.fallback_matching(parsed_resume)
        except Exception as e:
            logging.error(f"Job matcher AI response generation failed: {e}")
            matched = self.fallback_matching(parsed_resume)

        # Validate the matched data to ensure all fields are present
        matched = self._validate_matched_data(matched)

        return AgentMessage(self.name, msg.sender, matched).to_json()

    def fallback_matching(self, parsed_resume):
        """Fallback method if AI matching fails"""
        skills = parsed_resume.get("skills", [])
        if not isinstance(skills, list):
            skills = []  # Convert skills to lowercase for case-insensitive matching
        skills_lower = [s.lower() if isinstance(s, str) else s for s in skills]

        # Find matched skills (case-insensitive)
        matched_skills = []
        for skill in skills:
            if isinstance(skill, str) and any(
                req.lower() == skill.lower() for req in self.required_skills
            ):
                matched_skills.append(skill)

        # If no matches found using exact match, try partial matching
        if not matched_skills:
            for skill in skills:
                if isinstance(skill, str):
                    for req in self.required_skills:
                        if req.lower() in skill.lower() or skill.lower() in req.lower():
                            matched_skills.append(skill)
                            break

        skill_score = len(matched_skills)
        match_percent = min(
            100,
            int((skill_score / len(self.required_skills)) * 100)
            if self.required_skills
            else 0,
        )

        # Find best matching job roles
        job_matches = {}
        for role, role_skills in self.job_roles.items():
            role_skills_lower = [s.lower() for s in role_skills]
            matching_count = sum(1 for s in skills_lower if s in role_skills_lower)
            if matching_count > 0:
                job_matches[role] = matching_count / len(role_skills)

        # Sort job matches by score and take top 3
        sorted_jobs = sorted(job_matches.items(), key=lambda x: x[1], reverse=True)
        recommended_jobs = [job for job, _ in sorted_jobs[:3]]

        # If no jobs matched, recommend default options
        if not recommended_jobs:
            if match_percent > 50:
                recommended_jobs = ["Data Scientist", "ML Engineer"]
            else:
                recommended_jobs = ["Junior Developer", "Data Analyst"]

        # Generate suggested skills - skills from required set that aren't in the resume
        suggested = [
            s
            for s in self.required_skills
            if not any(req.lower() == s.lower() for req in skills)
        ]

        return {
            "matched_skills": matched_skills,
            "match_percent": match_percent,
            "suggested_skills": suggested if skills else list(self.required_skills),
            "job_roles": recommended_jobs,
        }

    def _validate_matched_data(self, matched):
        """Ensure all required fields are present and properly formatted"""
