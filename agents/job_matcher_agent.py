from agents.multi_ai_base import MultiAIAgent
from agents.message_protocol import AgentMessage
import json
import logging
import re


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
        if not isinstance(matched, dict):
            return self.fallback_matching({"skills": []})

        # Ensure all required fields exist
        required_fields = {
            "matched_skills": [],
            "match_percent": 0,
            "suggested_skills": [],
            "job_roles": [],
        }

        for field, default in required_fields.items():
            if field not in matched or matched[field] is None:
                matched[field] = default

        # Ensure match_percent is an integer between 0-100
        try:
            matched["match_percent"] = int(matched["match_percent"])
            matched["match_percent"] = max(0, min(100, matched["match_percent"]))
        except (ValueError, TypeError):
            matched["match_percent"] = 0

        # Ensure all list fields are actually lists
        for field in ["matched_skills", "suggested_skills", "job_roles"]:
            if not isinstance(matched[field], list):
                if isinstance(matched[field], str):
                    matched[field] = [
                        item.strip()
                        for item in matched[field].split(",")
                        if item.strip()
                    ]
                else:
                    matched[field] = []

        return matched

    def get_fallback_response(self, parsed_resume_json):
        """Provide a dynamic fallback response based on actual resume data"""
        try:
            resume = json.loads(parsed_resume_json)
            skills = resume.get("skills", [])
            years_exp = resume.get("years_of_experience", 0)

            # Calculate dynamic match based on actual skills
            skill_matches = 0
            matched_skills_list = []

            # Check each skill against our required skills (case-insensitive)
            for skill in skills:
                if isinstance(skill, str):
                    for req_skill in self.required_skills:
                        if (
                            req_skill.lower() in skill.lower()
                            or skill.lower() in req_skill.lower()
                        ):
                            skill_matches += 1
                            matched_skills_list.append(skill)
                            break

            # Calculate dynamic match percentage based on actual skills and experience
            base_match = min(85, skill_matches * 15)  # 15% per matching skill
            experience_bonus = min(15, years_exp * 3)  # 3% per year of experience
            final_match = min(100, base_match + experience_bonus)

            # If no skills matched, provide a lower but realistic score
            if final_match < 20:
                final_match = 35  # Minimum baseline score
                matched_skills_list = (
                    skills[:3]
                    if skills
                    else ["Python", "Communication", "Problem Solving"]
                )

            # Generate dynamic suggestions based on what's missing
            all_tech_skills = [
                "Python",
                "SQL",
                "AI",
                "ML",
                "NLP",
                "TensorFlow",
                "PyTorch",
                "AWS",
                "Docker",
                "Kubernetes",
                "React",
                "JavaScript",
                "Java",
                "C++",
            ]
            suggested_skills = [
                skill for skill in all_tech_skills if skill not in matched_skills_list
            ][:5]

            # Generate job roles based on skills
            job_roles = []
            if any(
                skill.lower() in ["python", "ai", "ml", "data"]
                for skill in matched_skills_list
            ):
                job_roles.extend(["Data Scientist", "ML Engineer"])
            if any(
                skill.lower() in ["sql", "database", "analytics"]
                for skill in matched_skills_list
            ):
                job_roles.extend(["Data Analyst", "Business Intelligence Analyst"])
            if any(
                skill.lower() in ["javascript", "react", "web", "frontend"]
                for skill in matched_skills_list
            ):
                job_roles.extend(["Frontend Developer", "Full Stack Developer"])
            if any(
                skill.lower() in ["java", "backend", "api"]
                for skill in matched_skills_list
            ):
                job_roles.extend(["Backend Developer", "Software Engineer"])

            # Default job roles if none matched
            if not job_roles:
                job_roles = ["Software Developer", "Technical Analyst", "IT Specialist"]

            return {
                "matched_skills": matched_skills_list[:5],  # Limit to top 5
                "match_percent": final_match,
                "suggested_skills": suggested_skills,
                "job_roles": job_roles[:4],  # Limit to top 4
            }

        except Exception as e:
            logging.warning(f"Error in dynamic fallback response generation: {e}")
            # Fallback to static response if parsing fails
            return {
                "matched_skills": ["Python", "Problem Solving", "Communication"],
                "match_percent": 45,
                "suggested_skills": ["SQL", "AI", "ML", "AWS", "Docker"],
                "job_roles": [
                    "Junior Developer",
                    "Technical Analyst",
                    "Software Engineer",
                ],
            }
