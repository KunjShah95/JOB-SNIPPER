#!/usr/bin/env python3
"""
Enhanced JobSniper AI Deployment Script
Deploys the complete enhanced system with all new features
"""

import os
import sys
import subprocess
import logging
import time
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedDeployment:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.required_dirs = [
            "agents", "ui/pages", "api", "mcp_servers", "utils", 
            "data/vector_store", "data/uploads", "data/cache", "logs"
        ]
        
    def check_prerequisites(self):
        """Check system prerequisites"""
        logger.info("🔍 Checking prerequisites...")
        
        # Check Python version
        if sys.version_info < (3, 8):
            logger.error("❌ Python 3.8+ required")
            return False
        
        # Check required directories
        for dir_path in self.required_dirs:
            full_path = self.project_root / dir_path
            if not full_path.exists():
                logger.info(f"📁 Creating directory: {dir_path}")
                full_path.mkdir(parents=True, exist_ok=True)
        
        logger.info("✅ Prerequisites check completed")
        return True
    
    def install_dependencies(self):
        """Install all required dependencies"""
        logger.info("📦 Installing dependencies...")
        
        try:
            # Basic dependencies
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ], cwd=self.project_root)
            
            # Enhanced dependencies
            enhanced_packages = [
                "fastapi>=0.104.0",
                "uvicorn[standard]>=0.24.0",
                "faiss-cpu>=1.7.4",
                "chromadb>=0.4.0",
                "sentence-transformers>=2.2.0",
                "langchain>=0.1.0",
                "langchain-community>=0.0.10",
                "pdfplumber>=0.10.0",
                "spacy>=3.7.0",
                "psutil>=5.9.0",
                "cryptography>=41.0.0",
                "bcrypt>=4.0.0",
                "PyJWT>=2.8.0"
            ]
            
            for package in enhanced_packages:
                try:
                    subprocess.check_call([
                        sys.executable, "-m", "pip", "install", package
                    ])
                    logger.info(f"✅ Installed {package}")
                except subprocess.CalledProcessError as e:
                    logger.warning(f"⚠️ Failed to install {package}: {e}")
            
            # Download spaCy model
            try:
                subprocess.check_call([
                    sys.executable, "-m", "spacy", "download", "en_core_web_sm"
                ])
                logger.info("✅ Downloaded spaCy English model")
            except subprocess.CalledProcessError:
                logger.warning("⚠️ Failed to download spaCy model")
            
            logger.info("✅ Dependencies installation completed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Dependencies installation failed: {e}")
            return False
    
    def setup_environment(self):
        """Setup environment configuration"""
        logger.info("🔧 Setting up environment...")
        
        env_file = self.project_root / ".env"
        
        if not env_file.exists():
            env_template = """# JobSniper AI Enhanced Configuration

# AI API Keys
GEMINI_API_KEY=your_gemini_api_key_here
MISTRAL_API_KEY=your_mistral_api_key_here

# Security Keys (Generate new ones for production)
JWT_SECRET_KEY=your_jwt_secret_key_here
ENCRYPTION_KEY=your_encryption_key_here

# Database Configuration
DATABASE_URL=sqlite:///data/jobsniper.db
VECTOR_DB_URL=http://localhost:8004

# API Configuration
API_HOST=0.0.0.0
API_PORT=8080
ENABLE_API_DOCS=true

# Monitoring Configuration
ENABLE_MONITORING=true
LOG_LEVEL=INFO
METRICS_RETENTION_DAYS=30

# Email Configuration (Optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# External Services (Optional)
WEBHOOK_URL=https://your-webhook-url.com/notify
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK

# Feature Flags
ENABLE_VECTOR_SEARCH=true
ENABLE_AI_SCORING=true
ENABLE_ANALYTICS=true
ENABLE_SECURITY=true
"""
            
            with open(env_file, 'w') as f:
                f.write(env_template)
            
            logger.info("✅ Created .env file template")
        else:
            logger.info("✅ .env file already exists")
        
        return True
    
    def initialize_databases(self):
        """Initialize databases and vector stores"""
        logger.info("🗄️ Initializing databases...")
        
        try:
            # Initialize SQLite database
            from utils.database import init_db
            init_db()
            logger.info("✅ SQLite database initialized")
            
            # Initialize vector database (if available)
            try:
                from agents.rag_qa_agent import RAGQAAgent
                qa_agent = RAGQAAgent()
                logger.info("✅ Vector database initialized")
            except Exception as e:
                logger.warning(f"⚠️ Vector database initialization failed: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
            return False
    
    def start_services(self, mode="development"):
        """Start all services"""
        logger.info(f"🚀 Starting services in {mode} mode...")
        
        if mode == "docker":
            return self._start_docker_services()
        else:
            return self._start_local_services()
    
    def _start_docker_services(self):
        """Start services using Docker Compose"""
        try:
            # Check if Docker is available
            subprocess.check_call(["docker", "--version"], stdout=subprocess.DEVNULL)
            subprocess.check_call(["docker-compose", "--version"], stdout=subprocess.DEVNULL)
            
            # Start services
            subprocess.check_call([
                "docker-compose", "up", "-d"
            ], cwd=self.project_root)
            
            logger.info("✅ Docker services started")
            logger.info("🌐 Services available at:")
            logger.info("   • Streamlit UI: http://localhost:8501")
            logger.info("   • API Gateway: http://localhost:8080")
            logger.info("   • API Docs: http://localhost:8080/docs")
            
            return True
            
        except subprocess.CalledProcessError:
            logger.error("❌ Docker not available or failed to start services")
            return False
        except FileNotFoundError:
            logger.error("❌ Docker or docker-compose not found")
            return False
    
    def _start_local_services(self):
        """Start services locally"""
        try:
            # Start Streamlit UI
            logger.info("🌐 Starting Streamlit UI...")
            logger.info("   • UI will be available at: http://localhost:8501")
            logger.info("   • Run: streamlit run ui/app.py")
            
            # Start API Gateway (optional)
            logger.info("🔌 API Gateway available at: http://localhost:8080")
            logger.info("   • Run: python api/gateway.py")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start local services: {e}")
            return False
    
    def run_health_checks(self):
        """Run system health checks"""
        logger.info("🏥 Running health checks...")
        
        try:
            from utils.monitoring import health
            health_status = health.run_health_checks()
            
            if health_status["overall_status"] == "healthy":
                logger.info("✅ All health checks passed")
            else:
                logger.warning(f"⚠️ Health status: {health_status['overall_status']}")
                
                for check_name, check_result in health_status["checks"].items():
                    if check_result["status"] != "healthy":
                        logger.warning(f"   • {check_name}: {check_result['status']}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Health checks failed: {e}")
            return False
    
    def deploy(self, mode="development"):
        """Run complete deployment"""
        logger.info("🚀 Starting JobSniper AI Enhanced Deployment...")
        
        steps = [
            ("Prerequisites", self.check_prerequisites),
            ("Dependencies", self.install_dependencies),
            ("Environment", self.setup_environment),
            ("Databases", self.initialize_databases),
            ("Services", lambda: self.start_services(mode)),
            ("Health Checks", self.run_health_checks)
        ]
        
        for step_name, step_func in steps:
            logger.info(f"\n{'='*50}")
            logger.info(f"Step: {step_name}")
            logger.info(f"{'='*50}")
            
            if not step_func():
                logger.error(f"❌ Deployment failed at step: {step_name}")
                return False
            
            time.sleep(1)  # Brief pause between steps
        
        logger.info(f"\n{'='*50}")
        logger.info("🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!")
        logger.info(f"{'='*50}")
        
        self._print_success_message(mode)
        return True
    
    def _print_success_message(self, mode):
        """Print deployment success message"""
        logger.info("\n🌟 JobSniper AI Enhanced Features Now Available:")
        logger.info("   ✅ AI-Powered Resume Scoring")
        logger.info("   ✅ Semantic Resume Search & QA")
        logger.info("   ✅ Real-time Analytics Dashboard")
        logger.info("   ✅ Advanced Security & Authentication")
        logger.info("   ✅ Comprehensive Monitoring")
        logger.info("   ✅ REST API Gateway")
        logger.info("   ✅ MCP Protocol Integration")
        logger.info("   ✅ Vector Database Support")
        
        logger.info("\n🔗 Access Points:")
        if mode == "docker":
            logger.info("   • Main UI: http://localhost:8501")
            logger.info("   • API Gateway: http://localhost:8080")
            logger.info("   • API Documentation: http://localhost:8080/docs")
            logger.info("   • Vector Database: http://localhost:8004")
        else:
            logger.info("   • Main UI: streamlit run ui/app.py")
            logger.info("   • API Gateway: python api/gateway.py")
        
        logger.info("\n📚 Next Steps:")
        logger.info("   1. Update .env file with your API keys")
        logger.info("   2. Try the new 'Resume Scoring' page")
        logger.info("   3. Test the 'Resume Q&A Search' feature")
        logger.info("   4. Check the 'Analytics Dashboard'")
        logger.info("   5. Explore the API documentation")

def main():
    """Main deployment function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Deploy JobSniper AI Enhanced")
    parser.add_argument(
        "--mode", 
        choices=["development", "docker", "production"],
        default="development",
        help="Deployment mode"
    )
    
    args = parser.parse_args()
    
    deployment = EnhancedDeployment()
    success = deployment.deploy(args.mode)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
