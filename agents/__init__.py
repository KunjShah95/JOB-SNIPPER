"""JobSniper AI Agents Package

This package contains all AI agents for resume analysis, job matching,
skill recommendations, and career intelligence.
"""

# Core agents
from .controller_agent import ControllerAgent
from .job_matcher_agent import JobMatcherAgent
from .resume_parser_agent import ResumeParserAgent
from .feedback_agent import FeedbackAgent
from .resume_tailor_agent import ResumeTailorAgent
from .title_generator_agent import TitleGeneratorAgent
from .jd_generator_agent import JDGeneratorAgent

# Advanced agents
from .auto_apply_agent import AutoApplyAgent
from .recruiter_view_agent import RecruiterViewAgent
from .skill_recommendation_agent import SkillRecommendationAgent
from .salary_negotiation_agent import SalaryNegotiationAgent

# Base classes
from .agent_base import Agent
from .multi_ai_base import MultiAIAgent
from .message_protocol import AgentMessage

# Enhanced agents (optional imports)
try:
    from .web_scraper_agent import WebScraperAgent
    from .resume_builder_agent import ResumeBuilderAgent
    from .advanced_interview_prep_agent import AdvancedInterviewPrepAgent
    from .career_path_agent import CareerPathAgent
    from .interview_prep_agent import InterviewPrepAgent
    WEB_FEATURES_AVAILABLE = True
except ImportError:
    WEB_FEATURES_AVAILABLE = False

__all__ = [
    # Core agents
    'ControllerAgent',
    'JobMatcherAgent', 
    'ResumeParserAgent',
    'FeedbackAgent',
    'ResumeTailorAgent',
    'TitleGeneratorAgent',
    'JDGeneratorAgent',
    
    # Advanced agents
    'AutoApplyAgent',
    'RecruiterViewAgent',
    'SkillRecommendationAgent',
    'SalaryNegotiationAgent',
    
    # Base classes
    'Agent',
    'MultiAIAgent',
    'AgentMessage',
    
    # Feature flag
    'WEB_FEATURES_AVAILABLE'
]

# Add enhanced agents to __all__ if available
if WEB_FEATURES_AVAILABLE:
    __all__.extend([
        'WebScraperAgent',
        'ResumeBuilderAgent', 
        'AdvancedInterviewPrepAgent',
        'CareerPathAgent',
        'InterviewPrepAgent'
    ])
