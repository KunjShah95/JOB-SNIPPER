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

def main():
    """Main setup function"""
    print("🚀 Setting up JobSniper AI...")
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create environment file
    create_env_file()
    
    # Setup database
    if not setup_database():
        return False
    
    print("\n✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your API keys")
    print("2. Run: python run.py")
    print("3. Or run: streamlit run ui/app.py")
    
    return True

if __name__ == "__main__":
    main()