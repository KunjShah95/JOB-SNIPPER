"""
Resume QA Search Page - Semantic Search and Q&A over Resume Database
New page for intelligent resume search and question answering
"""

import streamlit as st
from datetime import datetime
from typing import Dict, Any, List
import time

def render():
    """Render the resume QA search page"""
    
    st.title("🔍 Resume Q&A Search")
    st.markdown("Ask questions about resumes in your database using AI-powered semantic search")
    
    # Create tabs for different QA features
    tab1, tab2, tab3 = st.tabs(["💬 Ask Questions", "📊 Database Stats", "🔧 Search Settings"])
    
    with tab1:
        render_qa_interface()
    
    with tab2:
        render_database_stats()
    
    with tab3:
        render_search_settings()

def render_qa_interface():
    """Main QA interface"""
    
    # Initialize chat history
    if "qa_messages" not in st.session_state:
        st.session_state.qa_messages = []
    
    # Display chat history
    st.markdown("### 💬 Chat with Resume Database")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.qa_messages:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(message["content"])
            else:
                with st.chat_message("assistant"):
                    st.markdown(message["content"])
                    
                    # Show sources if available
                    if message.get("sources"):
                        with st.expander("📚 Sources"):
                            for i, source in enumerate(message["sources"], 1):
                                st.markdown(f"{i}. {source}")
                    
                    # Show confidence if available
                    if message.get("confidence"):
                        confidence = message["confidence"]
                        if confidence > 0.8:
                            st.success(f"🎯 High confidence: {confidence:.1%}")
                        elif confidence > 0.6:
                            st.warning(f"⚠️ Medium confidence: {confidence:.1%}")
                        else:
                            st.error(f"❓ Low confidence: {confidence:.1%}")
    
    # Question input
    st.markdown("### ❓ Ask a Question")
    
    # Sample questions
    st.markdown("**Try these sample questions:**")
    sample_questions = [
        "Which candidates have Python experience?",
        "Who has the most years of experience?",
        "Find resumes with machine learning skills",
        "Which candidates have AWS or cloud experience?",
        "Show me senior-level candidates",
        "Who has experience with React and Node.js?"
    ]
    
    cols = st.columns(2)
    for i, question in enumerate(sample_questions):
        with cols[i % 2]:
            if st.button(question, key=f"sample_{i}"):
                handle_question(question)
    
    # Custom question input
    with st.form("qa_form"):
        user_question = st.text_area(
            "Your Question:",
            placeholder="e.g., 'Which candidates have experience with Python and machine learning?'",
            height=100
        )
        
        # Advanced options
        with st.expander("🔧 Advanced Options"):
            col1, col2 = st.columns(2)
            
            with col1:
                search_type = st.selectbox(
                    "Search Type",
                    ["Semantic Search", "Keyword Search", "Hybrid"]
                )
            
            with col2:
                max_results = st.slider("Max Results", 1, 10, 5)
        
        submitted = st.form_submit_button("🔍 Search", type="primary")
        
        if submitted and user_question.strip():
            handle_question(user_question, search_type, max_results)
        elif submitted:
            st.warning("Please enter a question to search.")

def handle_question(question: str, search_type: str = "Semantic Search", max_results: int = 5):
    """Handle user question and get AI response"""
    
    # Add user message to chat
    st.session_state.qa_messages.append({
        "role": "user",
        "content": question,
        "timestamp": datetime.now()
    })
    
    # Show thinking indicator
    with st.spinner("🤔 Searching resume database..."):
        # Simulate processing time
        time.sleep(1)
        
        # Get AI response (mock for now - will integrate with rag_qa_agent.py)
        response = get_qa_response(question, search_type, max_results)
    
    # Add assistant response to chat
    st.session_state.qa_messages.append({
        "role": "assistant",
        "content": response["answer"],
        "sources": response.get("sources", []),
        "confidence": response.get("confidence", 0.0),
        "timestamp": datetime.now()
    })
    
    # Rerun to update chat display
    st.rerun()

def get_qa_response(question: str, search_type: str, max_results: int) -> Dict[str, Any]:
    """Get QA response (mock implementation - will integrate with rag_qa_agent.py)"""
    
    # TODO: Integrate with enhanced_orchestrator.py and rag_qa_agent.py
    # For now, return mock responses based on question content
    
    question_lower = question.lower()
    
    # Mock responses based on question patterns
    if "python" in question_lower:
        return {
            "answer": "I found 3 candidates with Python experience:\n\n1. **John Smith** - 5 years experience, Senior Software Engineer with Python, ML, and AWS skills\n2. **Sarah Johnson** - 4 years experience, Full Stack Developer with Python and React\n3. **Mike Chen** - 3 years experience, Data Scientist with Python, TensorFlow, and SQL",
            "sources": [
                "Resume: John Smith - Senior Software Engineer",
                "Resume: Sarah Johnson - Full Stack Developer", 
                "Resume: Mike Chen - Data Scientist"
            ],
            "confidence": 0.9,
            "retrieved_chunks": 3
        }
    
    elif "machine learning" in question_lower or "ml" in question_lower:
        return {
            "answer": "I found 2 candidates with machine learning experience:\n\n1. **John Smith** - Extensive ML experience with TensorFlow, PyTorch, and scikit-learn. Has worked on recommendation systems and NLP projects.\n2. **Mike Chen** - Data Scientist with 3 years of ML experience, specializing in predictive modeling and deep learning.",
            "sources": [
                "Resume: John Smith - ML Projects Section",
                "Resume: Mike Chen - Data Science Experience"
            ],
            "confidence": 0.85,
            "retrieved_chunks": 2
        }
    
    elif "aws" in question_lower or "cloud" in question_lower:
        return {
            "answer": "I found 2 candidates with cloud/AWS experience:\n\n1. **John Smith** - AWS certified with experience in EC2, S3, Lambda, and Docker deployment\n2. **Alex Rodriguez** - Cloud architect with 4 years AWS experience, including Kubernetes and microservices",
            "sources": [
                "Resume: John Smith - Technical Skills",
                "Resume: Alex Rodriguez - Cloud Experience"
            ],
            "confidence": 0.8,
            "retrieved_chunks": 2
        }
    
    elif "senior" in question_lower or "experience" in question_lower:
        return {
            "answer": "Here are the senior-level candidates in the database:\n\n1. **John Smith** - 5 years experience, Senior Software Engineer\n2. **Alex Rodriguez** - 6 years experience, Cloud Architect\n3. **Lisa Wang** - 7 years experience, Senior Product Manager",
            "sources": [
                "Resume: John Smith - Work Experience",
                "Resume: Alex Rodriguez - Career Summary",
                "Resume: Lisa Wang - Professional Experience"
            ],
            "confidence": 0.75,
            "retrieved_chunks": 3
        }
    
    elif "react" in question_lower and "node" in question_lower:
        return {
            "answer": "I found 1 candidate with both React and Node.js experience:\n\n**Sarah Johnson** - Full Stack Developer with 4 years experience. Proficient in React for frontend development and Node.js for backend APIs. Has built several full-stack web applications.",
            "sources": [
                "Resume: Sarah Johnson - Technical Skills",
                "Resume: Sarah Johnson - Project Experience"
            ],
            "confidence": 0.9,
            "retrieved_chunks": 1
        }
    
    else:
        return {
            "answer": f"I searched the resume database for '{question}' but couldn't find specific matches. This might be because:\n\n• The information isn't available in the current database\n• Try rephrasing your question with different keywords\n• The database might need more resumes to provide better results\n\nTry asking about specific skills, experience levels, or job titles.",
            "sources": [],
            "confidence": 0.2,
            "retrieved_chunks": 0
        }

def render_database_stats():
    """Render database statistics and analytics"""
    
    st.markdown("### 📊 Resume Database Statistics")
    
    # Mock database stats (will integrate with rag_qa_agent.py)
    stats = get_database_stats()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Resumes", stats["total_resumes"])
    
    with col2:
        st.metric("Searchable Chunks", stats["total_chunks"])
    
    with col3:
        st.metric("Vector Search", "✅ Enabled" if stats["vector_search_available"] else "❌ Disabled")
    
    with col4:
        st.metric("Last Updated", stats["last_updated"])
    
    # Database composition
    st.markdown("### 📈 Database Composition")
    
    # Skills distribution
    if stats.get("skills_distribution"):
        st.markdown("#### Top Skills in Database")
        skills_data = stats["skills_distribution"]
        
        import plotly.express as px
        fig = px.bar(
            x=list(skills_data.keys()),
            y=list(skills_data.values()),
            title="Most Common Skills",
            labels={"x": "Skills", "y": "Number of Candidates"}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Experience levels
    if stats.get("experience_levels"):
        st.markdown("#### Experience Level Distribution")
        exp_data = stats["experience_levels"]
        
        fig_pie = px.pie(
            values=list(exp_data.values()),
            names=list(exp_data.keys()),
            title="Experience Level Distribution"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Recent activity
    st.markdown("### 📅 Recent Activity")
    
    if stats.get("recent_additions"):
        for addition in stats["recent_additions"]:
            st.markdown(f"• **{addition['name']}** added on {addition['date']}")
    else:
        st.info("No recent additions to display.")

def get_database_stats() -> Dict[str, Any]:
    """Get database statistics (mock implementation)"""
    
    # TODO: Integrate with rag_qa_agent.py to get real stats
    return {
        "total_resumes": 15,
        "total_chunks": 45,
        "vector_search_available": True,
        "last_updated": "2024-01-15",
        "embedding_model": "all-MiniLM-L6-v2",
        "skills_distribution": {
            "Python": 8,
            "JavaScript": 6,
            "React": 5,
            "SQL": 7,
            "AWS": 4,
            "Machine Learning": 3,
            "Node.js": 4,
            "Java": 5
        },
        "experience_levels": {
            "Junior (0-2 years)": 4,
            "Mid-Level (3-5 years)": 7,
            "Senior (6+ years)": 4
        },
        "recent_additions": [
            {"name": "John Smith", "date": "2024-01-15"},
            {"name": "Sarah Johnson", "date": "2024-01-14"},
            {"name": "Mike Chen", "date": "2024-01-13"}
        ]
    }

def render_search_settings():
    """Render search configuration settings"""
    
    st.markdown("### 🔧 Search Configuration")
    
    # Search parameters
    st.markdown("#### Search Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        similarity_threshold = st.slider(
            "Similarity Threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.1,
            help="Minimum similarity score for search results"
        )
        
        max_chunks = st.slider(
            "Max Chunks per Query",
            min_value=1,
            max_value=20,
            value=5,
            help="Maximum number of document chunks to retrieve"
        )
    
    with col2:
        enable_reranking = st.checkbox(
            "Enable Re-ranking",
            value=True,
            help="Re-rank results for better relevance"
        )
        
        include_metadata = st.checkbox(
            "Include Metadata",
            value=True,
            help="Include resume metadata in search results"
        )
    
    # Model settings
    st.markdown("#### Model Settings")
    
    embedding_model = st.selectbox(
        "Embedding Model",
        ["all-MiniLM-L6-v2", "all-mpnet-base-v2", "sentence-t5-base"],
        help="Choose the embedding model for semantic search"
    )
    
    # Database management
    st.markdown("#### Database Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh Index"):
            st.success("Index refreshed successfully!")
    
    with col2:
        if st.button("🧹 Clear Cache"):
            st.success("Cache cleared successfully!")
    
    with col3:
        if st.button("📊 Rebuild Index"):
            with st.spinner("Rebuilding search index..."):
                time.sleep(2)
            st.success("Index rebuilt successfully!")
    
    # Export options
    st.markdown("#### Export Options")
    
    if st.button("📥 Export Search History"):
        # Mock export functionality
        st.download_button(
            label="Download Search History",
            data="timestamp,question,answer,confidence\n2024-01-15,Which candidates have Python?,Found 3 candidates,0.9\n",
            file_name="search_history.csv",
            mime="text/csv"
        )
    
    # Advanced settings
    with st.expander("🔬 Advanced Settings"):
        st.markdown("**Vector Database Settings:**")
        
        vector_dim = st.number_input("Vector Dimensions", value=384, disabled=True)
        index_type = st.selectbox("Index Type", ["Flat", "IVF", "HNSW"], disabled=True)
        
        st.markdown("**Performance Settings:**")
        
        batch_size = st.slider("Batch Size", 1, 100, 32)
        cache_size = st.slider("Cache Size (MB)", 10, 1000, 100)
        
        st.info("💡 Advanced settings require system restart to take effect.")
