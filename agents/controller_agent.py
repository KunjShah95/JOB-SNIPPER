from agents.message_protocol import AgentMessage
from agents.resume_parser_agent import ResumeParserAgent
from agents.job_matcher_agent import JobMatcherAgent
from agents.feedback_agent import FeedbackAgent
from agents.resume_tailor_agent import ResumeTailorAgent
from agents.title_generator_agent import TitleGeneratorAgent
from agents.jd_generator_agent import JDGeneratorAgent
from utils.sqlite_logger import save_to_db
import json
import logging


class ControllerAgent:
    def __init__(self):
        self.parser = ResumeParserAgent()
        self.matcher = JobMatcherAgent()
        self.feedback = FeedbackAgent()
        self.tailor = ResumeTailorAgent()
        self.title_gen = TitleGeneratorAgent()
        self.jd_gen = JDGeneratorAgent()

    def run(self, resume_text, job_title=None):
        """
        Main method to run all agents in sequence with improved error handling
        """
        result = {}

        # Step 1: Parse Resume
        try:
            msg_parser = AgentMessage(
                "Controller", "ResumeParserAgent", resume_text
            ).to_json()
            parsed_json = self.parser.run(msg_parser)
            parsed_msg = AgentMessage.from_json(parsed_json)
            parsed = parsed_msg.data
            result["parsed_data"] = parsed
        except Exception as e:
            logging.error(f"Error in resume parsing: {e}")
            result["parsed_data"] = self.parser.fallback_parsing(resume_text)

        # Step 2: Match Skills
        try:
            msg_match = AgentMessage(
                "Controller",
                "JobMatcherAgent",
                json.dumps(result.get("parsed_data", {})),
            ).to_json()
            matched_json = self.matcher.run(msg_match)
            matched_msg = AgentMessage.from_json(matched_json)
            matched = matched_msg.data
            result["match_result"] = matched
        except Exception as e:
            logging.error(f"Error in job matching: {e}")
            result["match_result"] = self.matcher.fallback_matching(
                result.get("parsed_data", {})
            )

        # Step 3: Feedback
        try:
            msg_feedback = AgentMessage(
                "Controller", "FeedbackAgent", resume_text
            ).to_json()
            feedback_json = self.feedback.run(msg_feedback)
            feedback_msg = AgentMessage.from_json(feedback_json)
            feedback = feedback_msg.data
            result["feedback"] = feedback
        except Exception as e:
            logging.error(f"Error in feedback generation: {e}")
            result["feedback"] = self.feedback.get_fallback_response(resume_text)

        # Step 4: Save to DB
        try:
            save_to_db(result.get("parsed_data", {}), result.get("match_result", {}))
        except Exception as e:
            logging.error(f"Error saving to database: {e}")

        # Step 5: Job Titles
        try:
            msg_title = AgentMessage(
                "Controller", "TitleGeneratorAgent", resume_text
            ).to_json()
            title_json = self.title_gen.run(msg_title)
            title_msg = AgentMessage.from_json(title_json)
            titles = title_msg.data
            result["job_titles"] = titles
        except Exception as e:
            logging.error(f"Error in job title generation: {e}")
            result["job_titles"] = self.title_gen.get_fallback_response("")

        # Step 6: Resume Tailoring Suggestions (optional)
        result["tailoring"] = ""
        if job_title:
            try:
                tailor_payload = {"resume": resume_text, "job_title": job_title}
                msg_tailor = AgentMessage(
                    "Controller", "ResumeTailorAgent", tailor_payload
                ).to_json()
                tailor_json = self.tailor.run(msg_tailor)
                tailor_msg = AgentMessage.from_json(tailor_json)
                tailoring = tailor_msg.data
                result["tailoring"] = tailoring
            except Exception as e:
                logging.error(f"Error in resume tailoring: {e}")
                result["tailoring"] = self.tailor.get_fallback_response(job_title)

        # Step 7: Job Description
        try:
            msg_jd = AgentMessage(
                "Controller", "JDGeneratorAgent", resume_text
            ).to_json()
            jd_json = self.jd_gen.run(msg_jd)
            jd_msg = AgentMessage.from_json(jd_json)
            jd = jd_msg.data
            result["job_description"] = jd
        except Exception as e:
            logging.error(f"Error in job description generation: {e}")
            result["job_description"] = self.jd_gen.get_fallback_response("")

        # Validate result to ensure all keys exist
        self._validate_result(result)

        return result

    def _validate_result(self, result):
        """Ensure all expected keys are present with empty fallback values"""
        if "parsed_data" not in result or not result["parsed_data"]:
            result["parsed_data"] = {}

        if "match_result" not in result:
            result["match_result"] = {}

        if "feedback" not in result or not result["feedback"]:
            result["feedback"] = ""

        if "job_titles" not in result or not result["job_titles"]:
            result["job_titles"] = []

        if "job_description" not in result or not result["job_description"]:
            result["job_description"] = ""

        if "tailoring" not in result or not result["tailoring"]:
            result["tailoring"] = ""

        if "match_result" in result and "match_percent" not in result["match_result"]:
            result["match_result"]["match_percent"] = 100

        # Ensure 'job_roles' key exists in match_result
        if "match_result" in result and "job_roles" not in result["match_result"]:
            result["match_result"]["job_roles"] = []

        # Ensure 'suggested_skills' key exists in match_result
        if (
            "match_result" in result
            and "suggested_skills" not in result["match_result"]
        ):
            result["match_result"]["suggested_skills"] = []
