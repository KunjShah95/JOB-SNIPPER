"""
Setup script for JobSniper AI
"""


import shutil
import subprocess
import sys
from pathlib import Path

def create_env_file():
    """Create .env file from template if it doesn't exist"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("📝 Please edit .env file with your actual API keys")
    elif not env_file.exists():
        print("⚠️ No .env file found. Please create one with your API keys.")

def install_dependencies():
    """Install required dependencies"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    return True

def setup_database():
    """Initialize the database"""
    try:
        from utils.sqlite_logger import init_db
        init_db()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False
    return True

def setup_enhanced_features():
    """Setup enhanced features (ADK, MCP, A2A, RAG)"""
    print("\n🔧 Setting up enhanced features...")

    try:
        # Install additional dependencies for enhanced features
        enhanced_packages = [
            "faiss-cpu>=1.7.4",
            "chromadb>=0.4.0",
            "sentence-transformers>=2.2.0",
            "langchain>=0.1.0",
            "fastapi>=0.104.0",
            "uvicorn>=0.24.0",
            "pdfplumber>=0.10.0",
            "spacy>=3.7.0"
        ]

        print("📦 Installing enhanced dependencies...")
        for package in enhanced_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ Installed {package}")
            except subprocess.CalledProcessError:
                print(f"⚠️ Failed to install {package} - will use fallback mode")

        # Download spaCy model
        try:
            subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
            print("✅ Downloaded spaCy English model")
        except subprocess.CalledProcessError:
            print("⚠️ Failed to download spaCy model - some features may be limited")

        # Create vector database directory
        os.makedirs("data/vector_store", exist_ok=True)
        os.makedirs("data/uploads", exist_ok=True)
        os.makedirs("data/cache", exist_ok=True)

        print("✅ Enhanced features setup completed!")
        return True

    except Exception as e:
        print(f"❌ Enhanced features setup failed: {e}")
        print("📝 Basic features will still work without enhanced capabilities")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up JobSniper AI with Enhanced Features...")

    # Install basic dependencies
    if not install_dependencies():
        return False

    # Create environment file
    create_env_file()

    # Setup database
    if not setup_database():
        return False

    # Setup enhanced features
    enhanced_success = setup_enhanced_features()

    print("\n✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your API keys")

    if enhanced_success:
        print("2. Run enhanced version: python -m agents.enhanced_orchestrator")
        print("3. Or run UI: streamlit run ui/app.py")
        print("4. Or use Docker: docker-compose up")
        print("\n🌟 Enhanced Features Available:")
        print("   • AI-powered resume scoring")
        print("   • Semantic search & QA over resumes")
        print("   • Vector database integration")
        print("   • Advanced parsing with MCP")
    else:
        print("2. Run basic version: python run.py")
        print("3. Or run: streamlit run ui/app.py")
        print("\n📝 Note: Enhanced features not available - using basic mode")

    return True

if __name__ == "__main__":
    main()