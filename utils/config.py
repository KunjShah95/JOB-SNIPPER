import os
from dotenv import load_dotenv
import dotenv
import logging

# Load environment variables
load_dotenv()

# Get configuration values
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
COOKIE_KEY = os.getenv("COOKIE_KEY")

# Email Configuration
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

# Determine which AI provider to use
# Priority: Gemini > Mistral > Fallback Mode
GEMINI_AVAILABLE = (
    GEMINI_API_KEY
    and GEMINI_API_KEY != "your_actual_gemini_api_key_here"
    and GEMINI_API_KEY.strip() != ""
    and len(GEMINI_API_KEY.strip()) >= 30
    and GEMINI_API_KEY.startswith("AIza")
)

MISTRAL_AVAILABLE = (
    MISTRAL_API_KEY
    and MISTRAL_API_KEY != "your_actual_mistral_api_key_here"
    and MISTRAL_API_KEY.strip() != ""
    and len(MISTRAL_API_KEY.strip()) >= 20
)

# Email availability check
EMAIL_AVAILABLE = (
    SENDER_EMAIL
    and SENDER_PASSWORD
    and SENDER_EMAIL != "your_gmail@gmail.com"
    and SENDER_PASSWORD != "your_app_password"
    and SENDER_EMAIL.strip() != ""
    and SENDER_PASSWORD.strip() != ""
)

# Set AI provider priority
if GEMINI_AVAILABLE:
    AI_PROVIDER = "gemini"
elif MISTRAL_AVAILABLE:
    AI_PROVIDER = "mistral"
else:
    AI_PROVIDER = "fallback"

# Add Firecrawl configuration
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "")

# Add new feature flags
FEATURES = {
    "resume_builder": True,
    "company_research": True,
    "advanced_interview_prep": True,
    "salary_insights": True,
    "web_scraping": bool(FIRECRAWL_API_KEY)
}

def update_email_config(email, password):
    """Updates the email configuration in the .env file"""
    try:
        dotenv_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")

        # Update the .env file
        dotenv.set_key(dotenv_file, "SENDER_EMAIL", email)
        dotenv.set_key(dotenv_file, "SENDER_PASSWORD", password)

        # Also update the global variables
        global SENDER_EMAIL, SENDER_PASSWORD, EMAIL_AVAILABLE
        SENDER_EMAIL = email
        SENDER_PASSWORD = password

        # Check if email is now configured
        EMAIL_AVAILABLE = (
            SENDER_EMAIL
            and SENDER_PASSWORD
            and SENDER_EMAIL != "your_gmail@gmail.com"
            and SENDER_PASSWORD != "your_app_password"
            and SENDER_EMAIL.strip() != ""
            and SENDER_PASSWORD.strip() != ""
        )

        return EMAIL_AVAILABLE
    except Exception as e:
        logging.error(f"Error updating email config: {e}")
        return False

def load_config():
    """Load and return configuration dictionary"""
    try:
        return {
            "gemini_api_key": GEMINI_API_KEY,
            "mistral_api_key": MISTRAL_API_KEY,
            "cookie_key": COOKIE_KEY,
            "sender_email": SENDER_EMAIL,
            "sender_password": SENDER_PASSWORD,
            "smtp_server": SMTP_SERVER,
            "smtp_port": SMTP_PORT,
            "firecrawl_api_key": FIRECRAWL_API_KEY,
            "gemini_available": GEMINI_AVAILABLE,
            "mistral_available": MISTRAL_AVAILABLE,
            "email_available": EMAIL_AVAILABLE,
            "ai_provider": AI_PROVIDER,
            "features": FEATURES
        }
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        return {}

def validate_config():
def validate_config():
    """Validate configuration and return comprehensive status"""
    issues = []
    warnings = []
    ai_providers = []
    features_enabled = []
    
    # Check AI providers
    if GEMINI_AVAILABLE:
        ai_providers.append('gemini-2.5-pro')
    elif GEMINI_API_KEY:
        warnings.append('Gemini API key provided but invalid format')
    
    if MISTRAL_AVAILABLE:
        ai_providers.append('mistral')
    elif MISTRAL_API_KEY:
        warnings.append('Mistral API key provided but invalid format')
    
    if not ai_providers:
        issues.append('No valid AI provider configured. Please set GEMINI_API_KEY or MISTRAL_API_KEY')
    
    # Check email configuration
    if EMAIL_AVAILABLE:
        features_enabled.append('email_reports')
    else:
        warnings.append('Email not configured - reports will not be sent')
    
    # Check other features
    for feature, enabled in FEATURES.items():
        if enabled:
            features_enabled.append(feature)
    
    # Check cookie key
    if not COOKIE_KEY:
        warnings.append('COOKIE_KEY not set - using default (not secure for production)')
    
    return {
        'valid': len(issues) == 0,