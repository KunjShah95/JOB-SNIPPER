"""
JobSniper AI - AI Agents Package
================================

Advanced AI agent system for JobSniper AI platform.
Includes specialized agents for resume analysis, job matching,
skill recommendations, and multi-agent orchestration.

Agents:
- BaseAgent: Foundation class for all agents
- ResumeParserAgent: Advanced resume parsing and analysis
- JobMatcherAgent: Intelligent job matching with ML
- SkillRecommenderAgent: Personalized skill recommendations
- OrchestratorAgent: Multi-agent coordination and workflow

Features:
- Sophisticated prompt engineering
- Multi-model AI support (OpenAI, Gemini, Anthropic)
- Performance monitoring and caching
- Error handling and fallback strategies
- Real-time processing and streaming
"""

from .base.agent import BaseAgent
from .base.prompt_engine import PromptEngine
from .base.model_manager import ModelManager

# Import specialized agents
try:
    from .resume.parser import ResumeParserAgent
    from .jobs.matcher import JobMatcherAgent
    from .skills.recommender import SkillRecommenderAgent
    from .orchestrator.coordinator import OrchestratorAgent
    
    AGENTS_AVAILABLE = True
except ImportError:
    AGENTS_AVAILABLE = False

# Agent registry for dynamic loading
AGENT_REGISTRY = {
    "resume_parser": "src.agents.resume.parser.ResumeParserAgent",
    "job_matcher": "src.agents.jobs.matcher.JobMatcherAgent",
    "skill_recommender": "src.agents.skills.recommender.SkillRecommenderAgent",
    "orchestrator": "src.agents.orchestrator.coordinator.OrchestratorAgent"
}

def get_agent(agent_type: str, **kwargs):
    """Get agent instance by type"""
    if agent_type not in AGENT_REGISTRY:
        raise ValueError(f"Unknown agent type: {agent_type}")
    
    module_path = AGENT_REGISTRY[agent_type]
    module_name, class_name = module_path.rsplit(".", 1)
    
    try:
        import importlib
        module = importlib.import_module(module_name)
        agent_class = getattr(module, class_name)
        return agent_class(**kwargs)
    except ImportError as e:
        raise ImportError(f"Failed to import agent {agent_type}: {e}")

def list_available_agents():
    """List all available agent types"""
    return list(AGENT_REGISTRY.keys())

__all__ = [
    "BaseAgent",
    "PromptEngine", 
    "ModelManager",
    "get_agent",
    "list_available_agents",
    "AGENT_REGISTRY",
    "AGENTS_AVAILABLE"
]

# Add conditional exports if agents are available
if AGENTS_AVAILABLE:
    __all__.extend([
        "ResumeParserAgent",
        "JobMatcherAgent", 
        "SkillRecommenderAgent",
        "OrchestratorAgent"
    ])