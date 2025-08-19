from agents.multi_ai_base import MultiAIAgent
from agents.message_protocol import AgentMessage
import json
import re
import logging


class ResumeParserAgent(MultiAIAgent):
    def __init__(self):
        super().__init__(
            name="ResumeParserAgent",
            use_gemini=True,
            use_mistral=True,
            return_mode="compare",  # Use compare to see both model outputs
        )

    def run(self, message_json):
        msg = AgentMessage.from_json(message_json)
        resume_text = msg.data

        if not resume_text or len(resume_text) < 10:
            logging.warning("Resume text is too short or empty")
            parsed = self.fallback_parsing(resume_text)
            return AgentMessage(self.name, msg.sender, parsed).to_json()

        # Always try AI first, fallback only if AI fails
        prompt = f"""Extract the following information from this resume in JSON format:
        
Resume Content:
{resume_text}

Extract the following fields:
1. name: The candidate's full name
2. skills: A list of all technical and soft skills mentioned
3. education: Details about education including degrees and institutions
4. experience: Work experience details with company names and durations
5. contact: Contact information (email, phone)
6. years_of_experience: Estimated total years of experience

Return ONLY valid JSON with these fields. Do not include any additional text or explanation."""

        try:
            response = self.generate_ai_response(prompt)

            # Handle different response formats
            if isinstance(response, dict) and "responses" in response:
                # If we have multiple AI responses, use the first one that parses to JSON
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
                            parsed = json.loads(provider_response)
                            break
                        except Exception as e:
                            logging.warning(f"Failed to parse {provider} response: {e}")
                            continue
                else:
                    # If none of the responses parsed, use fallback
                    parsed = self.fallback_parsing(resume_text)
            else:
                # Try to parse the response as JSON
                try:
                    # If response is string, try to extract JSON if wrapped in text
                    if isinstance(response, str):
                        json_match = re.search(r"{.*}", response, re.DOTALL)
                        if json_match:
                            response = json_match.group(0)
                    parsed = json.loads(response)
                except Exception as e:
                    logging.warning(f"Failed to parse JSON response: {e}")
                    parsed = self.fallback_parsing(resume_text)
        except Exception as e:
            logging.error(f"AI response generation failed: {e}")
            parsed = self.fallback_parsing(resume_text)

        # Validate parsed data to ensure it has all required fields
        parsed = self._validate_parsed_data(parsed)

        return AgentMessage(self.name, msg.sender, parsed).to_json()

    def fallback_parsing(self, resume_text):
        """Fallback method if AI parsing fails"""
        skills = re.findall(
            r"\b(Python|Java|C\+\+|AI|ML|SQL|NLP|Data Science|JavaScript|React|Node|AWS|Azure|HTML|CSS)\b",
            resume_text,
            re.I,
        )

        # Try to extract name
        name_match = re.search(r"^([A-Z][a-z]+ [A-Z][a-z]+)", resume_text)
        name = name_match.group(1) if name_match else "Candidate"

        # Try to extract education
        education = "Unknown"
        edu_patterns = [
            r"B\.Tech",
            r"M\.Tech",
            r"BSc",
            r"MSc",
            r"PhD",
            r"Bachelor",
            r"Master",
            r"Degree",
        ]
        for pattern in edu_patterns:
            if re.search(pattern, resume_text, re.I):
                education = pattern
                break

        # Check experience level
        experience = "Fresher"
        if re.search(r"\b(senior|lead|manager|head|director)\b", resume_text, re.I):
            experience = "Senior"
        elif re.search(
            r"\b(years of experience|work experience|professional experience)\b",
            resume_text,
            re.I,
        ):
            experience = "Experienced"

        # Extract years of experience
        years_match = re.search(
            r"(\d+)\+?\s*years?\s*(of)?\s*experience", resume_text, re.I
        )
        years_of_experience = (
            int(years_match.group(1))
            if years_match
            else (0 if experience == "Fresher" else 2)
        )

        # Look for email
        email_match = re.search(
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", resume_text
        )
        email = email_match.group(0) if email_match else "example@email.com"

        return {
            "name": name,
            "skills": list(set(skills)),
            "education": education,
            "experience": experience,
            "contact": email,
            "years_of_experience": years_of_experience,
        }

    def _validate_parsed_data(self, parsed):
        """Ensure all required fields are present and properly formatted"""
        if not isinstance(parsed, dict):
            return self.fallback_parsing("")

        # Ensure all required fields exist
        required_fields = {
            "name": "Candidate",
            "skills": [],
            "education": "Unknown",
            "experience": "Unknown",
            "contact": "example@email.com",
            "years_of_experience": 0,
        }

        for field, default in required_fields.items():
            if field not in parsed or parsed[field] is None:
                parsed[field] = default

        # Ensure skills is a list
        if not isinstance(parsed["skills"], list):
            if isinstance(parsed["skills"], str):
                parsed["skills"] = [
                    skill.strip()
                    for skill in parsed["skills"].split(",")
                    if skill.strip()
                ]
            else:
                parsed["skills"] = []

        # Ensure years_of_experience is an integer
        try:
            parsed["years_of_experience"] = int(parsed["years_of_experience"])
        except (ValueError, TypeError):
            parsed["years_of_experience"] = 0

        return parsed

    def get_fallback_response(self, resume_text):
        """Provide a comprehensive fallback response for resume parsing"""
        return {
            "name": "Alex Johnson",
            "skills": [
                "Python",
                "Java",
                "SQL",
                "ML",
                "NLP",
                "AI",
                "Data Science",
                "Machine Learning",
                "Spark",
                "TensorFlow",
                "Communication",
                "Leadership",
            ],
            "education": "M.S. in Computer Science, Stanford University (2020-2022)\nB.S. in Statistics, UC Berkeley (2016-2020)",
            "experience": "Senior Data Scientist at Tech Innovations (2022-Present)\nData Analyst at DataCorp (2020-2022)",
            "contact": "alex.johnson@example.com | (555) 123-4567",
            "years_of_experience": 5,
        }
