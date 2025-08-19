# JobSniper AI - Complete Architecture

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│  Streamlit UI   │◄──►│ Orchestrator A2A │◄──►│ Resume Parser Agent │
│  (Upload + QA)  │    │                  │    │ (ADK + MCP PDF)     │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
                                │
                                ▼
                       ┌─────────────────────┐
                       │ Resume Scorer Agent │
                       │ (ADK + AI Scoring)  │
                       └─────────────────────┘
                                │
                                ▼
                       ┌─────────────────────┐
                       │ Indexing Agent      │
                       │ (ADK + Vector DB)   │
                       └─────────────────────┘
                                │
                                ▼
                       ┌─────────────────────┐
                       │ QA Agent            │
                       │ (ADK + RAG)         │
                       └─────────────────────┘
```

## 🔧 Technology Stack

### Core Framework
- **Google ADK**: Agent framework
- **MCP**: Model Context Protocol for tools
- **A2A**: Agent-to-Agent communication

### Free/Open Source Components
- **Vector DB**: FAISS/Chroma (local)
- **Embeddings**: SentenceTransformers (MiniLM)
- **LLM**: Gemini (free tier) / Llama2 (local)
- **PDF Parsing**: pdfplumber / LlamaParse
- **UI**: Streamlit
- **Orchestration**: Docker Compose

## 🚀 Data Flow

1. **Upload**: User uploads PDF via Streamlit
2. **Parse**: Orchestrator → Parser Agent → MCP PDF Server
3. **Score**: Parsed data → Scorer Agent → AI evaluation
4. **Index**: Structured data → Indexing Agent → Vector DB
5. **QA**: User questions → QA Agent → RAG retrieval → Response

## 📊 Resume Scoring Engine

### Scoring Criteria
- **Technical Skills Match**: 0-25 points
- **Experience Relevance**: 0-25 points  
- **Education Alignment**: 0-20 points
- **Format & Structure**: 0-15 points
- **Keywords Density**: 0-15 points

### Output Format
```json
{
  "overall_score": 85,
  "breakdown": {
    "technical_skills": 22,
    "experience": 20,
    "education": 18,
    "format": 12,
    "keywords": 13
  },
  "recommendations": [
    "Add cloud computing skills",
    "Quantify achievements with metrics"
  ]
}
```

## 🔄 Agent Communication (A2A)

Each agent exposes:
- `/.well-known/agent.json` - Agent capabilities
- `/tasks` - Task execution endpoint
- `/status` - Health check

## 🐳 Deployment

```bash
docker-compose up -d
# Starts all agents + UI + vector DB
```

## 📈 Scalability

- **Horizontal**: Add more agent instances
- **Vertical**: Upgrade vector DB to cloud (Pinecone/Weaviate)
- **Performance**: Cache embeddings, async processing
