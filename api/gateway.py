"""
API Gateway - External API access for JobSniper AI
Provides REST API endpoints for external integrations
"""

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import asyncio
import logging
import os
from datetime import datetime
import tempfile

# Import your existing agents
from agents.enhanced_orchestrator import EnhancedOrchestrator
from agents.resume_scorer_agent import ResumeScorerAgent
from agents.rag_qa_agent import RAGQAAgent

# API Models
class ResumeUploadRequest(BaseModel):
    user_id: Optional[str] = None
    job_title: Optional[str] = None
    target_role: Optional[str] = None

class ResumeAnalysisResponse(BaseModel):
    workflow_id: str
    status: str
    parsed_data: Dict[str, Any]
    scoring_result: Dict[str, Any]
    match_result: Dict[str, Any]
    feedback: str
    timestamp: str

class QARequest(BaseModel):
    question: str
    user_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class QAResponse(BaseModel):
    question: str
    answer: str
    sources: List[str]
    confidence: float
    timestamp: str

class BulkProcessRequest(BaseModel):
    user_id: str
    job_description: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None

# Initialize FastAPI app
app = FastAPI(
    title="JobSniper AI API",
    description="AI-powered resume analysis and job matching API",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Initialize agents
orchestrator = EnhancedOrchestrator()
scorer = ResumeScorerAgent()
qa_agent = RAGQAAgent()

logger = logging.getLogger("APIGateway")

# Authentication dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Validate API token"""
    token = credentials.credentials
    
    # TODO: Implement proper token validation
    # For now, accept any token for demo purposes
    if not token or len(token) < 10:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    
    return {"user_id": "api_user", "token": token}

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "services": {
            "orchestrator": "online",
            "scorer": "online",
            "qa_agent": "online"
        }
    }

# Resume analysis endpoints
@app.post("/api/v2/resume/analyze", response_model=ResumeAnalysisResponse)
async def analyze_resume(
    file: UploadFile = File(...),
    request: ResumeUploadRequest = Depends(),
    current_user: dict = Depends(get_current_user)
):
    """Analyze uploaded resume with full pipeline"""
    
    if not file.filename.lower().endswith(('.pdf', '.docx', '.txt')):
        raise HTTPException(status_code=400, detail="Unsupported file format")
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        # Extract text from file
        resume_text = extract_text_from_file(tmp_path)
        
        if not resume_text:
            raise HTTPException(status_code=400, detail="Could not extract text from file")
        
        # Process with enhanced orchestrator
        result = await orchestrator.process_resume_complete(
            resume_text=resume_text,
            job_title=request.job_title,
            user_id=request.user_id or current_user["user_id"]
        )
        
        return ResumeAnalysisResponse(
            workflow_id=result["workflow_id"],
            status=result["status"],
            parsed_data=result.get("parsed_data", {}),
            scoring_result=result.get("scoring_result", {}),
            match_result=result.get("match_result", {}),
            feedback=result.get("feedback", ""),
            timestamp=result["timestamp"]
        )
        
    except Exception as e:
        logger.error(f"Resume analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
    finally:
        # Clean up temporary file
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)

@app.post("/api/v2/resume/score")
async def score_resume(
    file: UploadFile = File(...),
    target_role: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Score resume only (faster endpoint)"""
    
    try:
        # Save and extract text
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        resume_text = extract_text_from_file(tmp_path)
        
        if not resume_text:
            raise HTTPException(status_code=400, detail="Could not extract text from file")
        
        # Score only
        scoring_result = await orchestrator._score_resume(resume_text, {})
        
        return {
            "status": "success",
            "scoring_result": scoring_result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Resume scoring failed: {e}")
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")
    
    finally:
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)

# QA endpoints
@app.post("/api/v2/qa/query", response_model=QAResponse)
async def query_resumes(
    request: QARequest,
    current_user: dict = Depends(get_current_user)
):
    """Query resume database with natural language"""
    
    try:
        result = await orchestrator.handle_qa_request(
            question=request.question,
            context=request.context,
            user_id=request.user_id or current_user["user_id"]
        )
        
        return QAResponse(
            question=result["question"],
            answer=result["answer"],
            sources=result.get("sources", []),
            confidence=result.get("confidence", 0.0),
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"QA query failed: {e}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

@app.get("/api/v2/qa/stats")
async def get_qa_stats(current_user: dict = Depends(get_current_user)):
    """Get QA database statistics"""
    
    try:
        stats = qa_agent.get_database_stats()
        return {
            "status": "success",
            "stats": stats,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Stats retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Stats failed: {str(e)}")

# Bulk processing endpoints
@app.post("/api/v2/bulk/process")
async def bulk_process_resumes(
    request: BulkProcessRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """Start bulk processing of multiple resumes"""
    
    # Add background task for bulk processing
    background_tasks.add_task(
        process_bulk_resumes,
        request.user_id,
        request.job_description,
        request.filters
    )
    
    return {
        "status": "accepted",
        "message": "Bulk processing started",
        "user_id": request.user_id,
        "timestamp": datetime.now().isoformat()
    }

async def process_bulk_resumes(user_id: str, job_description: str, filters: Dict):
    """Background task for bulk processing"""
    logger.info(f"Starting bulk processing for user: {user_id}")
    
    # TODO: Implement bulk processing logic
    # This would typically:
    # 1. Fetch resumes from database/storage
    # 2. Process each resume through the pipeline
    # 3. Store results
    # 4. Send notification when complete
    
    await asyncio.sleep(5)  # Simulate processing
    logger.info(f"Bulk processing completed for user: {user_id}")

# Analytics endpoints
@app.get("/api/v2/analytics/overview")
async def get_analytics_overview(current_user: dict = Depends(get_current_user)):
    """Get system analytics overview"""
    
    try:
        analytics = await orchestrator.get_resume_analytics(
            user_id=current_user["user_id"]
        )
        
        return {
            "status": "success",
            "analytics": analytics,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Analytics retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analytics failed: {str(e)}")

# Webhook endpoints
@app.post("/api/v2/webhooks/resume-processed")
async def resume_processed_webhook(
    workflow_id: str,
    status: str,
    results: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """Webhook for resume processing completion"""
    
    logger.info(f"Resume processing webhook: {workflow_id} - {status}")
    
    # TODO: Implement webhook logic
    # This could:
    # 1. Update external systems
    # 2. Send notifications
    # 3. Trigger downstream processes
    
    return {
        "status": "received",
        "workflow_id": workflow_id,
        "timestamp": datetime.now().isoformat()
    }

# Utility functions
def extract_text_from_file(file_path: str) -> str:
    """Extract text from uploaded file"""
    try:
        if file_path.endswith('.pdf'):
            from utils.pdf_reader import extract_text_from_pdf
            return extract_text_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            from docx import Document
            doc = Document(file_path)
            return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        elif file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return ""
    except Exception as e:
        logger.error(f"Text extraction failed: {e}")
        return ""

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "error": exc.detail,
        "status_code": exc.status_code,
        "timestamp": datetime.now().isoformat()
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return {
        "error": "Internal server error",
        "status_code": 500,
        "timestamp": datetime.now().isoformat()
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("JobSniper AI API Gateway starting up...")
    
    # Initialize agents and connections
    try:
        # Test agent connections
        await orchestrator.get_resume_analytics()
        logger.info("All agents initialized successfully")
    except Exception as e:
        logger.error(f"Agent initialization failed: {e}")

# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.gateway:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )
