"""
Enhanced Setup script for JobSniper AI
Provides comprehensive setup, validation, and testing capabilities
"""

import shutil
import subprocess
import sys
import os
from pathlib import Path
import argparse


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def create_env_file():
    """Create .env file from template if it doesn't exist"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        if env_example.exists():
            shutil.copy(env_example, env_file)
            print("✅ Created .env file from template")
            print("📝 Please edit .env file with your actual API keys")
        else:
            print("⚠️ No .env.example found. Creating basic .env file...")
            create_basic_env_file(env_file)
    else:
        print("ℹ️ .env file already exists")


def create_basic_env_file(env_file):
    """Create a basic .env file with placeholders"""
    basic_env_content = """# JobSniper AI Configuration
# Replace these placeholders with your actual values

# AI API Keys (at least one required)
GEMINI_API_KEY=your_actual_gemini_api_key_here
MISTRAL_API_KEY=your_actual_mistral_api_key_here

# Email Configuration (optional)
SENDER_EMAIL=your_gmail@gmail.com
SENDER_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Optional Services
FIRECRAWL_API_KEY=your_firecrawl_api_key_here

# Security
COOKIE_KEY=your_secure_random_cookie_key_here

# Application Settings
DEBUG=False
LOG_LEVEL=INFO
"""
    
    with open(env_file, 'w') as f:
        f.write(basic_env_content)
    print("✅ Created basic .env file")


def install_dependencies(dev=False):
    """Install required dependencies"""
    try:
        print("📦 Installing dependencies...")
        cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        
        if dev:
            print("📦 Installing development dependencies...")
            # Add development-specific packages if needed
            
        subprocess.check_call(cmd)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        print("💡 Try running: pip install --upgrade pip")
        return False
    except FileNotFoundError:
        print("❌ requirements.txt not found")
        return False


def setup_database():
    """Initialize the database"""
    try:
        print("🗄️ Initializing database...")
        from utils.sqlite_logger import init_db
        init_db()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False


def validate_setup():
    """Validate the setup configuration"""
    try:
        print("🔍 Validating setup...")
        from utils.config import load_config, validate_config
        
        config = load_config()
        validation = validate_config(config)
        
        if validation['valid']:
            print("✅ Configuration is valid")
            print(f"🤖 AI Providers: {', '.join(validation['ai_providers'])}")
            print(f"🔧 Features enabled: {len(validation['features_enabled'])}")
        else:
            print("⚠️ Configuration has issues:")
            for issue in validation['issues']:
                print(f"   - {issue}")
            print("💡 You can still use demo mode")
        
        return validation['valid']
    except Exception as e:
        print(f"❌ Error validating setup: {e}")
        return False


def run_tests():
    """Run the test suite"""
    try:
        print("🧪 Running tests...")
        result = subprocess.run([sys.executable, "-m", "pytest"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All tests passed")
        else:
            print("❌ Some tests failed")
            print(result.stdout)
            print(result.stderr)
        
        return result.returncode == 0
    except FileNotFoundError:
        print("❌ pytest not found. Install with: pip install pytest")
        return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False


def check_system_requirements():
    """Check system requirements"""
    print("🔍 Checking system requirements...")
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check pip
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"], 
                            stdout=subprocess.DEVNULL)
        print("✅ pip is available")
    except subprocess.CalledProcessError:
        print("❌ pip is not available")
        return False
    
    # Check git (optional)
    try:
        subprocess.check_call(["git", "--version"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ git is available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️ git not found (optional for development)")
    
    return True


def main():
    """Main setup function"""
    parser = argparse.ArgumentParser(description="JobSniper AI Setup")
    parser.add_argument("--dev", action="store_true", help="Development setup")
    parser.add_argument("--test", action="store_true", help="Run tests after setup")
    parser.add_argument("--validate-only", action="store_true", help="Only validate configuration")
    parser.add_argument("--skip-deps", action="store_true", help="Skip dependency installation")
    
    args = parser.parse_args()
    
    print("🚀 Setting up JobSniper AI...")
    print("=" * 50)
    
    # Check system requirements
    if not check_system_requirements():
        print("❌ System requirements not met")
        return False
    
    if args.validate_only:
        return validate_setup()
    
    success = True
    
    # Install dependencies
    if not args.skip_deps:
        if not install_dependencies(dev=args.dev):
            success = False
    
    # Create environment file
    create_env_file()
    
    # Setup database
    if not setup_database():
        success = False
    
    # Validate setup
    config_valid = validate_setup()
    
    # Run tests if requested
    if args.test:
        if not run_tests():
            success = False
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Setup completed successfully!")
    else:
        print("⚠️ Setup completed with some issues")
    
    print("\n📋 Next steps:")
    if not config_valid:
        print("1. Edit .env file with your API keys")
    print("2. Run: python run.py")
    print("3. Or run: streamlit run ui/app.py")
    
    if args.dev:
        print("\n🔧 Development commands:")
        print("- Run tests: pytest")
        print("- Run with coverage: pytest --cov")
        print("- Format code: black .")
        print("- Lint code: flake8")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
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