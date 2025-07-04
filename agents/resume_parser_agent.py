from agents.multi_ai_base import MultiAIAgent
from agents.message_protocol import AgentMessage
import json
import re
import logging
from typing import Dict, Any


class ResumeParserAgent(MultiAIAgent):
    def __init__(self):
        super().__init__(
            name="ResumeParserAgent",
            use_gemini=True,
            use_mistral=True,
            return_mode="compare"
        )
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Implementation of abstract process method from Agent base class"""
        try:
            if isinstance(input_data, dict):
                resume_text = input_data.get('data', input_data.get('resume_text', str(input_data)))
            else:
                resume_text = str(input_data)
            
            message = AgentMessage(sender="user", recipient=self.name, data=resume_text)
            result_json = self.run(message.to_json())
            result = json.loads(result_json) if isinstance(result_json, str) else result_json
            
            if isinstance(result, dict) and 'data' in result:
                return result['data']
            else:
                return result
                
        except Exception as e:
            logging.error(f"Error in ResumeParserAgent.process: {e}")
            return self.fallback_parsing(str(input_data))

    def run(self, message_json):
        msg = AgentMessage.from_json(message_json)
        resume_text = msg.data

        if not resume_text or len(resume_text) < 10:
            logging.warning("Resume text is too short or empty")
            parsed = self.fallback_parsing(resume_text)
        else:
            try:
                parsed = self.parse_resume_with_ai(resume_text)
            except Exception as e:
                logging.error(f"AI parsing failed: {e}")
                parsed = self.fallback_parsing(resume_text)

        response = AgentMessage(
            sender=self.name,
            recipient=msg.sender,
            data=parsed
        )
        return response.to_json()

    def parse_resume_with_ai(self, resume_text):
        """Parse resume using AI models"""
        prompt = """
        Parse the following resume and extract structured information in JSON format.
        
        Resume Text:
        """ + resume_text + """
        
        Please extract and return ONLY a valid JSON object with these fields:
        {
            "personal_info": {
                "name": "Full Name",
                "email": "email@example.com",
                "phone": "phone number",
                "location": "city, state/country",
                "linkedin": "linkedin profile url",
                "github": "github profile url"
            },
            "summary": "Professional summary or objective",
            "experience": [
                {
                    "company": "Company Name",
                    "position": "Job Title",
                    "duration": "Start Date - End Date",
                    "description": "Job description and achievements"
                }
            ],
            "education": [
                {
                    "institution": "School/University Name",
                    "degree": "Degree Type and Major",
                    "graduation_year": "Year",
                    "gpa": "GPA if mentioned"
                }
            ],
            "skills": [
                "skill1", "skill2", "skill3"
            ],
            "certifications": [
                "certification1", "certification2"
            ],
            "projects": [
                {
                    "name": "Project Name",
                    "description": "Project description",
                    "technologies": ["tech1", "tech2"]
                }
            ]
        }
        
        Return ONLY the JSON object, no additional text or formatting.
        """

        try:
            ai_response = self.generate_ai_response(prompt)
            cleaned_response = self.clean_json_response(ai_response)
            parsed_data = json.loads(cleaned_response)
            return self.validate_and_clean_parsed_data(parsed_data)
            
        except Exception as e:
            logging.error(f"AI parsing failed: {e}")
            return self.fallback_parsing(resume_text)

    def clean_json_response(self, response):
        """Clean AI response to extract valid JSON"""
        if not response:
            raise ValueError("Empty response")
        
        response = re.sub(r'```json\s*', '', response)
        response = re.sub(r'```\s*$', '', response)
        
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json_match.group(0)
        else:
            raise ValueError("No JSON object found in response")

    def validate_and_clean_parsed_data(self, data):
        """Validate and clean parsed data"""
        if not isinstance(data, dict):
            raise ValueError("Parsed data is not a dictionary")
        
        required_fields = ['personal_info', 'summary', 'experience', 'education', 'skills']
        for field in required_fields:
            if field not in data:
                data[field] = [] if field in ['experience', 'education', 'skills'] else {}
        
        if not isinstance(data['personal_info'], dict):
            data['personal_info'] = {}
        
        for list_field in ['experience', 'education', 'skills', 'certifications', 'projects']:
            if list_field in data and not isinstance(data[list_field], list):
                data[list_field] = []
        
        return data

    def fallback_parsing(self, resume_text):
        """Fallback parsing using regex patterns"""
        logging.info("Using fallback parsing method")
        
        parsed = {
            "personal_info": {},
            "summary": "",
            "experience": [],
            "education": [],
            "skills": [],
            "certifications": [],
            "projects": []
        }
        
        if not resume_text:
            return parsed
        
        try:
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, resume_text)
            if emails:
                parsed["personal_info"]["email"] = emails[0]
            
            phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
            phones = re.findall(phone_pattern, resume_text)
            if phones:
                parsed["personal_info"]["phone"] = ''.join(phones[0]) if isinstance(phones[0], tuple) else phones[0]
            
            skill_keywords = [
                'Python', 'Java', 'JavaScript', 'C++', 'C#', 'SQL', 'HTML', 'CSS',
                'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'Spring',
                'Machine Learning', 'Data Science', 'AI', 'AWS', 'Azure', 'Docker',
                'Kubernetes', 'Git', 'Linux', 'Windows', 'MongoDB', 'PostgreSQL'
            ]
            
            found_skills = []
            for skill in skill_keywords:
                if skill.lower() in resume_text.lower():
                    found_skills.append(skill)
            
            parsed["skills"] = found_skills[:10]
            
            lines = resume_text.split('\n')
            for line in lines[:5]:
                line = line.strip()
                if len(line) > 2 and len(line) < 50 and ' ' in line:
                    words = line.split()
                    if 2 <= len(words) <= 4 and not any(char.isdigit() for char in line):
                        parsed["personal_info"]["name"] = line
                        break
            
        except Exception as e:
            logging.error(f"Error in fallback parsing: {e}")
        
        return parsed

    def get_fallback_response(self, resume_text=""):
        """Get fallback response when all parsing fails"""
        return {
            "personal_info": {
                "name": "Unable to extract",
                "email": "Unable to extract",
                "phone": "Unable to extract"
            },
            "summary": "Unable to extract summary from resume",
            "experience": [],
            "education": [],
            "skills": ["Unable to extract skills"],
            "certifications": [],
            "projects": []
        }