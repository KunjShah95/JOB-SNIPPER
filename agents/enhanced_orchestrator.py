"""
Enhanced Orchestrator - Integrates ADK + A2A with existing JobSniper AI agents
Extends the current controller_agent.py with new capabilities
"""

from agents.controller_agent import ControllerAgent
from agents.resume_scorer_agent import ResumeScorerAgent
from agents.rag_qa_agent import RAGQAAgent
from agents.message_protocol import AgentMessage
from utils.sqlite_logger import save_to_db
import json
import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime

class EnhancedOrchestrator:
    def __init__(self):
        # Initialize existing controller
        self.controller = ControllerAgent()
        
        # Initialize new agents
        self.scorer = ResumeScorerAgent()
        self.qa_agent = RAGQAAgent()
        
        # Agent registry for A2A-style communication
        self.agents = {
            # Existing agents (via controller)
            "parser": self.controller.parser,
            "matcher": self.controller.matcher,
            "feedback": self.controller.feedback,
            "tailor": self.controller.tailor,
            "title_gen": self.controller.title_gen,
            "jd_gen": self.controller.jd_gen,
            
            # New enhanced agents
            "scorer": self.scorer,
            "qa": self.qa_agent,
            
            # Controller itself
            "controller": self.controller
        }
        
        self.logger = logging.getLogger("EnhancedOrchestrator")

    async def process_resume_complete(self, resume_text: str, job_title: str = None, user_id: str = None) -> Dict[str, Any]:
        """
        Complete resume processing pipeline with scoring and indexing
        """
        workflow_id = f"resume_{user_id or 'anonymous'}_{int(datetime.now().timestamp())}"
        
        try:
            self.logger.info(f"Starting enhanced resume processing: {workflow_id}")
            
            # Step 1: Run existing controller pipeline
            controller_result = self.controller.run(resume_text, job_title)
            
            # Step 2: Score the resume
            scoring_result = await self._score_resume(resume_text, controller_result.get("parsed_data", {}))
            
            # Step 3: Add to QA index for future searches
            indexing_result = await self._index_resume_for_qa(resume_text, controller_result.get("parsed_data", {}))
            
            # Step 4: Compile comprehensive result
            enhanced_result = {
                "workflow_id": workflow_id,
                "status": "completed",
                "timestamp": datetime.now().isoformat(),
                
                # Existing results
                "parsed_data": controller_result.get("parsed_data", {}),
                "match_result": controller_result.get("match_result", {}),
                "feedback": controller_result.get("feedback", ""),
                "job_titles": controller_result.get("job_titles", []),
                "job_description": controller_result.get("job_description", ""),
                "tailoring": controller_result.get("tailoring", ""),
                
                # New enhanced results
                "scoring_result": scoring_result,
                "indexing_result": indexing_result,
                
                # Metadata
                "processing_method": "enhanced_pipeline",
                "agents_used": ["parser", "matcher", "feedback", "scorer", "qa_indexer"]
            }
            
            # Save enhanced results to database
            try:
                await self._save_enhanced_results(enhanced_result)
            except Exception as e:
                self.logger.error(f"Failed to save enhanced results: {e}")
            
            self.logger.info(f"Enhanced resume processing completed: {workflow_id}")
            return enhanced_result
            
        except Exception as e:
            self.logger.error(f"Enhanced resume processing failed: {workflow_id}, error: {str(e)}")
            return {
                "workflow_id": workflow_id,
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "fallback_result": self.controller.run(resume_text, job_title)  # Fallback to basic processing
            }

    async def _score_resume(self, resume_text: str, parsed_data: Dict) -> Dict[str, Any]:
        """Score resume using the new scoring agent"""
        try:
            # Prepare scoring input
            scoring_input = {
                "resume_text": resume_text,
                "parsed_data": parsed_data
            }
            
            # Create message for scorer agent
            msg = AgentMessage("EnhancedOrchestrator", "ResumeScorerAgent", scoring_input)
            
            # Run scoring agent
            scoring_response = self.scorer.run(msg.to_json())
            scoring_msg = AgentMessage.from_json(scoring_response)
            
            return scoring_msg.data
            
        except Exception as e:
            self.logger.error(f"Resume scoring failed: {e}")
            return {
                "error": str(e),
                "overall_score": 0,
                "method": "failed"
            }

    async def _index_resume_for_qa(self, resume_text: str, parsed_data: Dict) -> Dict[str, Any]:
        """Add resume to QA searchable index"""
        try:
            # Prepare resume data for indexing
            resume_data = {
                "resume_text": resume_text,
                "parsed_data": parsed_data,
                "indexed_at": datetime.now().isoformat()
            }
            
            # Add to QA agent's index
            success = self.qa_agent.add_resume_to_index(resume_data)
            
            return {
                "indexed": success,
                "method": "vector_embedding" if success else "fallback",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Resume indexing failed: {e}")
            return {
                "indexed": False,
                "error": str(e),
                "method": "failed"
            }

    async def handle_qa_request(self, question: str, context: Dict = None, user_id: str = None) -> Dict[str, Any]:
        """Handle QA requests using the RAG agent"""
        try:
            # Prepare QA input
            qa_input = {
                "question": question,
                "context": context or {},
                "user_id": user_id
            }
            
            # Create message for QA agent
            msg = AgentMessage("EnhancedOrchestrator", "RAGQAAgent", qa_input)
            
            # Run QA agent
            qa_response = self.qa_agent.run(msg.to_json())
            qa_msg = AgentMessage.from_json(qa_response)
            
            return qa_msg.data
            
        except Exception as e:
            self.logger.error(f"QA request failed: {e}")
            return {
                "question": question,
                "answer": f"Sorry, I encountered an error processing your question: {str(e)}",
                "sources": [],
                "confidence": 0.0,
                "error": str(e)
            }

    async def get_resume_analytics(self, user_id: str = None) -> Dict[str, Any]:
        """Get analytics about processed resumes"""
        try:
            # Get QA database stats
            qa_stats = self.qa_agent.get_database_stats()
            
            # Compile analytics
            analytics = {
                "database_stats": qa_stats,
                "processing_stats": {
                    "total_processed": qa_stats.get("total_resumes", 0),
                    "vector_search_enabled": qa_stats.get("vector_search_available", False),
                    "last_updated": datetime.now().isoformat()
                },
                "available_features": {
                    "resume_parsing": True,
                    "job_matching": True,
                    "resume_scoring": True,
                    "qa_search": qa_stats.get("vector_search_available", False),
                    "feedback_generation": True
                }
            }
            
            return analytics
            
        except Exception as e:
            self.logger.error(f"Analytics generation failed: {e}")
            return {
                "error": str(e),
                "available_features": {
                    "resume_parsing": True,
                    "job_matching": True,
                    "basic_features": True
                }
            }

    async def _save_enhanced_results(self, result: Dict[str, Any]):
        """Save enhanced results to database"""
        try:
            # Use existing database save function
            save_to_db(
                result.get("parsed_data", {}),
                result.get("match_result", {})
            )
            
            # TODO: Extend database schema to store scoring and QA results
            # For now, just log the enhanced data
            self.logger.info(f"Enhanced results saved for workflow: {result.get('workflow_id')}")
            
        except Exception as e:
            self.logger.error(f"Database save failed: {e}")
            raise

    def run_agent(self, agent_name: str, *args, **kwargs) -> Any:
        """
        Run a specific agent (compatible with existing orchestrator interface)
        """
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
                return None
                
        except Exception as e:
            self.logger.error(f"Error running agent '{agent_name}': {e}")
            return None

    def list_agents(self) -> List[str]:
        """List all available agents"""
        return list(self.agents.keys())

    def get_agent_capabilities(self) -> Dict[str, Dict[str, Any]]:
        """Get capabilities of all agents (A2A-style discovery)"""
        capabilities = {}
        
        for agent_name, agent in self.agents.items():
            capabilities[agent_name] = {
                "name": agent_name,
                "type": type(agent).__name__,
                "methods": [method for method in dir(agent) if not method.startswith('_')],
                "description": getattr(agent, '__doc__', 'No description available'),
                "status": "available"
            }
        
        return capabilities

    # Backward compatibility methods
    def run(self, resume_text: str, job_title: str = None) -> Dict[str, Any]:
        """
        Synchronous version for backward compatibility
        """
        try:
            # Run async method in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self.process_resume_complete(resume_text, job_title)
            )
            loop.close()
            return result
        except Exception as e:
            self.logger.error(f"Sync processing failed: {e}")
            # Fallback to basic controller
            return self.controller.run(resume_text, job_title)

# Factory function for easy integration
def create_enhanced_orchestrator() -> EnhancedOrchestrator:
    """Create and return an enhanced orchestrator instance"""
    return EnhancedOrchestrator()

# Backward compatibility - can be used as drop-in replacement for ControllerAgent
class EnhancedControllerAgent(EnhancedOrchestrator):
    """
    Drop-in replacement for ControllerAgent with enhanced capabilities
    """
    pass
