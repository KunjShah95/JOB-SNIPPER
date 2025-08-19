"""
Orchestrator Agent - A2A Coordinator
Manages workflow between parser, scorer, indexing, and QA agents
"""

import asyncio
import json
from typing import Dict, Any, List
from google.adk.core import LlmAgent
from google.adk.tools.a2a_tool.a2a_toolset import A2AToolset
from shared.models import ResumeData, ScoringResult, QARequest, QAResponse
from shared.config import get_config
import logging

logger = logging.getLogger(__name__)

class OrchestratorAgent:
    def __init__(self):
        self.config = get_config()
        self.agent = LlmAgent(
            model="gemini-2.0-flash-exp",
            tools=[A2AToolset()],
            system_prompt=self._get_system_prompt()
        )
        
        # Agent registry
        self.agents = {
            "parser": "http://parser-agent:8001",
            "scorer": "http://scorer-agent:8002", 
            "indexing": "http://indexing-agent:8003",
            "qa": "http://qa-agent:8004"
        }
    
    def _get_system_prompt(self) -> str:
        return """
        You are the Orchestrator Agent for JobSniper AI Resume QA system.
        
        Your responsibilities:
        1. Coordinate resume processing workflow
        2. Manage communication between specialized agents
        3. Ensure data consistency across the pipeline
        4. Handle error recovery and retries
        
        Available agents:
        - Parser Agent: Extracts structured data from PDF resumes
        - Scorer Agent: Evaluates resume quality and provides scores
        - Indexing Agent: Creates embeddings and stores in vector DB
        - QA Agent: Handles user questions via RAG pipeline
        
        Always maintain workflow state and provide clear status updates.
        """
    
    async def process_resume(self, file_path: str, user_id: str) -> Dict[str, Any]:
        """
        Complete resume processing pipeline
        """
        workflow_id = f"resume_{user_id}_{asyncio.get_event_loop().time()}"
        
        try:
            logger.info(f"Starting resume processing workflow: {workflow_id}")
            
            # Step 1: Parse resume
            parsed_data = await self._parse_resume(file_path, workflow_id)
            if not parsed_data:
                raise Exception("Resume parsing failed")
            
            # Step 2: Score resume
            scoring_result = await self._score_resume(parsed_data, workflow_id)
            
            # Step 3: Index resume for QA
            indexing_result = await self._index_resume(parsed_data, workflow_id)
            
            # Compile results
            result = {
                "workflow_id": workflow_id,
                "status": "completed",
                "parsed_data": parsed_data,
                "scoring_result": scoring_result,
                "indexing_result": indexing_result,
                "timestamp": asyncio.get_event_loop().time()
            }
            
            logger.info(f"Resume processing completed: {workflow_id}")
            return result
            
        except Exception as e:
            logger.error(f"Resume processing failed: {workflow_id}, error: {str(e)}")
            return {
                "workflow_id": workflow_id,
                "status": "failed",
                "error": str(e),
                "timestamp": asyncio.get_event_loop().time()
            }
    
    async def _parse_resume(self, file_path: str, workflow_id: str) -> Dict[str, Any]:
        """Call parser agent to extract resume data"""
        try:
            task_data = {
                "task": "parse_resume",
                "file_path": file_path,
                "workflow_id": workflow_id
            }
            
            response = await self.agent.run(
                f"Call the parser agent at {self.agents['parser']} with task: {json.dumps(task_data)}"
            )
            
            return json.loads(response) if isinstance(response, str) else response
            
        except Exception as e:
            logger.error(f"Parser agent call failed: {str(e)}")
            return None
    
    async def _score_resume(self, parsed_data: Dict[str, Any], workflow_id: str) -> Dict[str, Any]:
        """Call scorer agent to evaluate resume"""
        try:
            task_data = {
                "task": "score_resume",
                "parsed_data": parsed_data,
                "workflow_id": workflow_id
            }
            
            response = await self.agent.run(
                f"Call the scorer agent at {self.agents['scorer']} with task: {json.dumps(task_data)}"
            )
            
            return json.loads(response) if isinstance(response, str) else response
            
        except Exception as e:
            logger.error(f"Scorer agent call failed: {str(e)}")
            return {"error": str(e)}
    
    async def _index_resume(self, parsed_data: Dict[str, Any], workflow_id: str) -> Dict[str, Any]:
        """Call indexing agent to store resume in vector DB"""
        try:
            task_data = {
                "task": "index_resume",
                "parsed_data": parsed_data,
                "workflow_id": workflow_id
            }
            
            response = await self.agent.run(
                f"Call the indexing agent at {self.agents['indexing']} with task: {json.dumps(task_data)}"
            )
            
            return json.loads(response) if isinstance(response, str) else response
            
        except Exception as e:
            logger.error(f"Indexing agent call failed: {str(e)}")
            return {"error": str(e)}
    
    async def handle_qa_request(self, question: str, user_id: str, context: Dict = None) -> QAResponse:
        """Handle user QA requests via QA agent"""
        try:
            task_data = {
                "task": "answer_question",
                "question": question,
                "user_id": user_id,
                "context": context or {}
            }
            
            response = await self.agent.run(
                f"Call the QA agent at {self.agents['qa']} with task: {json.dumps(task_data)}"
            )
            
            result = json.loads(response) if isinstance(response, str) else response
            
            return QAResponse(
                answer=result.get("answer", ""),
                sources=result.get("sources", []),
                confidence=result.get("confidence", 0.0),
                workflow_id=result.get("workflow_id", "")
            )
            
        except Exception as e:
            logger.error(f"QA agent call failed: {str(e)}")
            return QAResponse(
                answer=f"Error processing question: {str(e)}",
                sources=[],
                confidence=0.0,
                workflow_id=""
            )
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Check health status of all agents"""
        status = {
            "orchestrator": "healthy",
            "agents": {},
            "timestamp": asyncio.get_event_loop().time()
        }
        
        for agent_name, agent_url in self.agents.items():
            try:
                # Simple health check call
                response = await self.agent.run(f"Check health of {agent_name} at {agent_url}")
                status["agents"][agent_name] = "healthy"
            except Exception as e:
                status["agents"][agent_name] = f"unhealthy: {str(e)}"
        
        return status

# Agent server setup for A2A communication
if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI
    
    app = FastAPI(title="Orchestrator Agent")
    orchestrator = OrchestratorAgent()
    
    @app.post("/tasks")
    async def handle_task(task_data: Dict[str, Any]):
        task_type = task_data.get("task")
        
        if task_type == "process_resume":
            return await orchestrator.process_resume(
                task_data["file_path"], 
                task_data["user_id"]
            )
        elif task_type == "qa_request":
            return await orchestrator.handle_qa_request(
                task_data["question"],
                task_data["user_id"],
                task_data.get("context")
            )
        elif task_type == "system_status":
            return await orchestrator.get_system_status()
        else:
            return {"error": f"Unknown task type: {task_type}"}
    
    @app.get("/status")
    async def health_check():
        return {"status": "healthy", "agent": "orchestrator"}
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
