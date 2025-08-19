"""
Orchestrator to manage all agents in the JOB-SNIPPER project.
"""
import importlib
import logging
from agents import (
    advanced_interview_prep_agent,
    agent_fallback,
    auto_apply_agent,
    career_path_agent,
    controller_agent,
    feedback_agent,
    interview_prep_agent,
    jd_generator_agent,
    job_matcher_agent,
    recruiter_view_agent,
    resume_builder_agent,
    resume_parser_agent,
    resume_tailor_agent,
    salary_negotiation_agent,
    skill_recommendation_agent,
    title_generator_agent,
    web_scraper_agent
)
from utils import error_handler

class AgentOrchestrator:
    def __init__(self):
        self.agents = {
            'advanced_interview_prep': advanced_interview_prep_agent.AdvancedInterviewPrepAgent(),
            'agent_fallback': agent_fallback.AgentFallback(),
            'auto_apply': auto_apply_agent.AutoApplyAgent(),
            'career_path': career_path_agent.CareerPathAgent(),
            'controller': controller_agent.ControllerAgent(),
            'feedback': feedback_agent.FeedbackAgent(),
            'interview_prep': interview_prep_agent.InterviewPrepAgent(),
            'jd_generator': jd_generator_agent.JDGeneratorAgent(),
            'job_matcher': job_matcher_agent.JobMatcherAgent(),
            'recruiter_view': recruiter_view_agent.RecruiterViewAgent(),
            'resume_builder': resume_builder_agent.ResumeBuilderAgent(),
            'resume_parser': resume_parser_agent.ResumeParserAgent(),
            'resume_tailor': resume_tailor_agent.ResumeTailorAgent(),
            'salary_negotiation': salary_negotiation_agent.SalaryNegotiationAgent(),
            'skill_recommendation': skill_recommendation_agent.SkillRecommendationAgent(),
            'title_generator': title_generator_agent.TitleGeneratorAgent(),
            'web_scraper': web_scraper_agent.WebScraperAgent(),
        }
        self.logger = logging.getLogger("AgentOrchestrator")

    def run_agent(self, agent_name, *args, **kwargs):
        agent = self.agents.get(agent_name)
        if not agent:
            self.logger.error(f"Agent '{agent_name}' not found.")
            return None
        try:
            if hasattr(agent, 'run'):
                return agent.run(*args, **kwargs)
            elif hasattr(agent, '__call__'):
                return agent(*args, **kwargs)
            else:
                self.logger.error(f"Agent '{agent_name}' has no 'run' or '__call__' method.")
        except Exception as e:
            error_handler.handle_exception(e)
            self.logger.error(f"Error running agent '{agent_name}': {e}")
        return None

    def list_agents(self):
        return list(self.agents.keys())

# Example usage:
# orchestrator = AgentOrchestrator()
# result = orchestrator.run_agent('resume_parser', resume_path)
# print(result)
