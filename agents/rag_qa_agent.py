"""
RAG QA Agent - Semantic Search and Question Answering
Provides intelligent Q&A over resume database using vector embeddings
"""

from agents.multi_ai_base import MultiAIAgent
from agents.message_protocol import AgentMessage
import json
import logging
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

# Vector DB and embeddings (will be installed with new requirements)
try:
    import faiss
    import numpy as np
    from sentence_transformers import SentenceTransformer
    VECTOR_AVAILABLE = True
except ImportError:
    VECTOR_AVAILABLE = False
    logging.warning("Vector search dependencies not available. Install faiss-cpu and sentence-transformers.")

class RAGQAAgent(MultiAIAgent):
    def __init__(self):
        super().__init__(
            name="RAGQAAgent",
            use_gemini=True,
            use_mistral=True,
            return_mode="best"
        )
        
        # Initialize vector components if available
        if VECTOR_AVAILABLE:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            self.vector_dim = 384  # MiniLM embedding dimension
            self.index = faiss.IndexFlatIP(self.vector_dim)  # Inner product for cosine similarity
            self.resume_database = []  # Store resume metadata
            self.document_chunks = []  # Store text chunks
        else:
            self.embedding_model = None
            self.index = None
            self.resume_database = []
            self.document_chunks = []
        
        # Initialize with some sample data for demo
        self._initialize_sample_data()

    def run(self, message_json):
        """Handle QA requests"""
        msg = AgentMessage.from_json(message_json)
        request_data = msg.data
        
        if isinstance(request_data, str):
            # Simple question format
            question = request_data
            context = {}
        elif isinstance(request_data, dict):
            question = request_data.get("question", "")
            context = request_data.get("context", {})
        else:
            return AgentMessage(self.name, msg.sender, self._get_error_response()).to_json()

        try:
            # Process the question
            qa_result = self._answer_question(question, context)
            return AgentMessage(self.name, msg.sender, qa_result).to_json()
            
        except Exception as e:
            logging.error(f"QA processing failed: {e}")
            return AgentMessage(self.name, msg.sender, self._get_fallback_answer(question)).to_json()

    def add_resume_to_index(self, resume_data: Dict[str, Any]) -> bool:
        """Add a resume to the searchable index"""
        if not VECTOR_AVAILABLE:
            # Store in simple list for fallback search
            self.resume_database.append(resume_data)
            return True
        
        try:
            # Extract text content for embedding
            text_content = self._extract_searchable_text(resume_data)
            
            # Create chunks for better retrieval
            chunks = self._create_text_chunks(text_content, resume_data)
            
            # Generate embeddings
            embeddings = self.embedding_model.encode([chunk["text"] for chunk in chunks])
            
            # Normalize for cosine similarity
            faiss.normalize_L2(embeddings)
            
            # Add to index
            self.index.add(embeddings)
            
            # Store metadata
            for chunk in chunks:
                self.document_chunks.append(chunk)
            
            self.resume_database.append(resume_data)
            
            logging.info(f"Added resume to index: {resume_data.get('name', 'Unknown')}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to add resume to index: {e}")
            return False

    def _answer_question(self, question: str, context: Dict = None) -> Dict[str, Any]:
        """Answer a question using RAG pipeline"""
        
        if not question.strip():
            return self._get_error_response("Empty question provided")
        
        # Retrieve relevant documents
        relevant_docs = self._retrieve_relevant_documents(question, top_k=5)
        
        if not relevant_docs:
            return self._get_fallback_answer(question)
        
        # Generate answer using retrieved context
        answer = self._generate_answer_with_context(question, relevant_docs, context)
        
        return {
            "question": question,
            "answer": answer["response"],
            "sources": [doc["source"] for doc in relevant_docs],
            "confidence": answer.get("confidence", 0.8),
            "retrieved_chunks": len(relevant_docs),
            "timestamp": datetime.now().isoformat(),
            "method": "rag_pipeline"
        }

    def _retrieve_relevant_documents(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve relevant document chunks"""
        
        if not VECTOR_AVAILABLE or self.index.ntotal == 0:
            # Fallback to simple text search
            return self._fallback_text_search(query, top_k)
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query])
            faiss.normalize_L2(query_embedding)
            
            # Search index
            scores, indices = self.index.search(query_embedding, min(top_k, self.index.ntotal))
            
            # Retrieve relevant chunks
            relevant_docs = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.document_chunks) and score > 0.3:  # Similarity threshold
                    chunk = self.document_chunks[idx].copy()
                    chunk["similarity_score"] = float(score)
                    relevant_docs.append(chunk)
            
            return relevant_docs
            
        except Exception as e:
            logging.error(f"Vector search failed: {e}")
            return self._fallback_text_search(query, top_k)

    def _fallback_text_search(self, query: str, top_k: int) -> List[Dict]:
        """Simple text-based search fallback"""
        query_words = query.lower().split()
        scored_docs = []
        
        for i, resume in enumerate(self.resume_database):
            text_content = self._extract_searchable_text(resume).lower()
            
            # Simple word matching score
            score = sum(1 for word in query_words if word in text_content)
            
            if score > 0:
                scored_docs.append({
                    "text": text_content[:500] + "...",  # Truncate for display
                    "source": f"Resume: {resume.get('name', f'Document {i}')}",
                    "resume_data": resume,
                    "similarity_score": score / len(query_words)
                })
        
        # Sort by score and return top_k
        scored_docs.sort(key=lambda x: x["similarity_score"], reverse=True)
        return scored_docs[:top_k]

    def _generate_answer_with_context(self, question: str, relevant_docs: List[Dict], context: Dict = None) -> Dict:
        """Generate answer using retrieved context"""
        
        # Prepare context from retrieved documents
        context_text = "\n\n".join([
            f"Source: {doc['source']}\nContent: {doc['text'][:300]}..."
            for doc in relevant_docs
        ])
        
        # Create prompt for answer generation
        prompt = f"""
        Based on the following resume information, answer the user's question accurately and concisely.

        Context from Resume Database:
        {context_text}

        Question: {question}

        Instructions:
        1. Answer based only on the provided context
        2. If the information is not available in the context, say so
        3. Cite specific sources when possible
        4. Keep the answer concise but informative
        5. If asking about specific candidates, mention their names

        Answer:
        """

        try:
            # Generate AI response
            ai_response = self.generate_ai_response(prompt)
            
            # Handle different response formats
            if isinstance(ai_response, dict) and "responses" in ai_response:
                # Use the best available response
                for provider in self.provider_priority:
                    if provider in ai_response["responses"]:
                        response_text = ai_response["responses"][provider]
                        break
                else:
                    response_text = "Unable to generate response from available AI providers."
            else:
                response_text = str(ai_response)
            
            return {
                "response": response_text,
                "confidence": 0.8 if len(relevant_docs) > 2 else 0.6
            }
            
        except Exception as e:
            logging.error(f"Answer generation failed: {e}")
            return {
                "response": f"I found {len(relevant_docs)} relevant documents but couldn't generate a comprehensive answer. Please try rephrasing your question.",
                "confidence": 0.3
            }

    def _extract_searchable_text(self, resume_data: Dict) -> str:
        """Extract searchable text from resume data"""
        text_parts = []
        
        # Handle different resume data formats
        if "resume_text" in resume_data:
            text_parts.append(resume_data["resume_text"])
        
        if "parsed_data" in resume_data:
            parsed = resume_data["parsed_data"]
            
            if "name" in parsed:
                text_parts.append(f"Candidate: {parsed['name']}")
            
            if "skills" in parsed:
                skills = parsed["skills"]
                if isinstance(skills, list):
                    text_parts.append(f"Skills: {', '.join(skills)}")
                else:
                    text_parts.append(f"Skills: {skills}")
            
            if "experience" in parsed:
                text_parts.append(f"Experience: {parsed['experience']}")
            
            if "education" in parsed:
                text_parts.append(f"Education: {parsed['education']}")
            
            if "years_of_experience" in parsed:
                text_parts.append(f"Years of Experience: {parsed['years_of_experience']}")
        
        return "\n".join(text_parts)

    def _create_text_chunks(self, text: str, resume_data: Dict, chunk_size: int = 200) -> List[Dict]:
        """Create overlapping text chunks for better retrieval"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size // 2):  # 50% overlap
            chunk_words = words[i:i + chunk_size]
            chunk_text = " ".join(chunk_words)
            
            chunks.append({
                "text": chunk_text,
                "source": f"Resume: {resume_data.get('parsed_data', {}).get('name', 'Unknown')}",
                "resume_id": resume_data.get("id", f"resume_{len(self.resume_database)}"),
                "chunk_index": len(chunks)
            })
        
        return chunks

    def _initialize_sample_data(self):
        """Initialize with sample resume data for demo"""
        sample_resumes = [
            {
                "id": "sample_1",
                "parsed_data": {
                    "name": "John Smith",
                    "skills": ["Python", "Machine Learning", "AWS", "Docker", "SQL"],
                    "experience": "Senior Software Engineer at TechCorp (2020-2023), Data Scientist at DataInc (2018-2020)",
                    "education": "M.S. Computer Science, Stanford University",
                    "years_of_experience": 5
                }
            },
            {
                "id": "sample_2", 
                "parsed_data": {
                    "name": "Sarah Johnson",
                    "skills": ["React", "Node.js", "JavaScript", "MongoDB", "GraphQL"],
                    "experience": "Full Stack Developer at WebSolutions (2021-2023), Frontend Developer at StartupXYZ (2019-2021)",
                    "education": "B.S. Computer Science, MIT",
                    "years_of_experience": 4
                }
            }
        ]
        
        for resume in sample_resumes:
            self.add_resume_to_index(resume)

    def _get_fallback_answer(self, question: str) -> Dict[str, Any]:
        """Provide fallback answer when retrieval fails"""
        return {
            "question": question,
            "answer": "I don't have enough information in the resume database to answer that question accurately. Please try asking about specific skills, experience, or candidate qualifications.",
            "sources": [],
            "confidence": 0.2,
            "retrieved_chunks": 0,
            "timestamp": datetime.now().isoformat(),
            "method": "fallback"
        }

    def _get_error_response(self, error_msg: str = "Invalid request format") -> Dict[str, Any]:
        """Return error response"""
        return {
            "error": error_msg,
            "answer": "Unable to process the question due to an error.",
            "sources": [],
            "confidence": 0.0,
            "timestamp": datetime.now().isoformat()
        }

    def get_database_stats(self) -> Dict[str, Any]:
        """Get statistics about the resume database"""
        return {
            "total_resumes": len(self.resume_database),
            "total_chunks": len(self.document_chunks),
            "vector_search_available": VECTOR_AVAILABLE,
            "embedding_model": "all-MiniLM-L6-v2" if VECTOR_AVAILABLE else None,
            "index_size": self.index.ntotal if VECTOR_AVAILABLE and self.index else 0
        }
