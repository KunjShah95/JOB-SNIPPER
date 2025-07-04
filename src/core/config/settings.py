"""
JobSniper AI - Configuration Settings
====================================

Centralized configuration management for the JobSniper AI platform.
Handles environment variables, feature flags, and application settings.
"""

import os
from typing import Optional, List, Dict, Any
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum

class Environment(str, Enum):
    """Application environment types"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"

class LogLevel(str, Enum):
    """Logging levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

@dataclass
class DatabaseConfig:
    """Database configuration"""
    url: str = "sqlite:///jobsniper.db"
    pool_size: int = 10
    max_overflow: int = 20
    pool_timeout: int = 30
    pool_recycle: int = 3600
    echo: bool = False

@dataclass
class RedisConfig:
    """Redis configuration for caching"""
    url: str = "redis://localhost:6379"
    db: int = 0
    max_connections: int = 10
    socket_timeout: int = 5
    socket_connect_timeout: int = 5

@dataclass
class AIConfig:
    """AI model configuration"""
    openai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Model settings
    max_tokens: int = 4000
    temperature: float = 0.7
    top_p: float = 0.9
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    
    # Timeout settings
    request_timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0

@dataclass
class UIConfig:
    """UI configuration"""
    theme: str = "modern"
    items_per_page: int = 20
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: List[str] = field(default_factory=lambda: ["pdf", "doc", "docx", "txt"])
    
    # Feature flags
    enable_dark_mode: bool = True
    enable_analytics: bool = True
    enable_export: bool = True
    enable_real_time: bool = True

@dataclass
class SecurityConfig:
    """Security configuration"""
    secret_key: str = "your-secret-key-change-in-production"
    jwt_secret: str = "your-jwt-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration: int = 3600  # 1 hour
    
    # Password requirements
    min_password_length: int = 8
    require_uppercase: bool = True
    require_lowercase: bool = True
    require_numbers: bool = True
    require_special_chars: bool = True
    
    # Rate limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600  # 1 hour

@dataclass
class EmailConfig:
    """Email configuration"""
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    use_tls: bool = True
    use_ssl: bool = False
    
    # Email settings
    from_email: Optional[str] = None
    from_name: str = "JobSniper AI"
    reply_to: Optional[str] = None

class Settings:
    """Main settings class for JobSniper AI"""
    
    def __init__(self):
        self.load_from_environment()
    
    def load_from_environment(self):
        """Load settings from environment variables"""
        
        # Application settings
        self.app_name: str = os.getenv("APP_NAME", "JobSniper AI")
        self.version: str = os.getenv("APP_VERSION", "2.0.0")
        self.environment: Environment = Environment(os.getenv("ENVIRONMENT", "development"))
        self.debug: bool = os.getenv("DEBUG", "false").lower() == "true"
        self.log_level: LogLevel = LogLevel(os.getenv("LOG_LEVEL", "INFO"))
        
        # Server settings
        self.host: str = os.getenv("HOST", "0.0.0.0")
        self.port: int = int(os.getenv("PORT", "8501"))
        self.workers: int = int(os.getenv("WORKERS", "1"))
        
        # Database configuration
        self.database = DatabaseConfig(
            url=os.getenv("DATABASE_URL", "sqlite:///jobsniper.db"),
            pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
            max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "20")),
            echo=os.getenv("DB_ECHO", "false").lower() == "true"
        )
        
        # Redis configuration
        self.redis = RedisConfig(
            url=os.getenv("REDIS_URL", "redis://localhost:6379"),
            db=int(os.getenv("REDIS_DB", "0")),
            max_connections=int(os.getenv("REDIS_MAX_CONNECTIONS", "10"))
        )
        
        # AI configuration
        self.ai = AIConfig(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            gemini_api_key=os.getenv("GEMINI_API_KEY"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            max_tokens=int(os.getenv("AI_MAX_TOKENS", "4000")),
            temperature=float(os.getenv("AI_TEMPERATURE", "0.7")),
            request_timeout=int(os.getenv("AI_TIMEOUT", "30"))
        )
        
        # UI configuration
        self.ui = UIConfig(
            theme=os.getenv("UI_THEME", "modern"),
            items_per_page=int(os.getenv("UI_ITEMS_PER_PAGE", "20")),
            max_file_size=int(os.getenv("UI_MAX_FILE_SIZE", str(10 * 1024 * 1024))),
            enable_analytics=os.getenv("UI_ENABLE_ANALYTICS", "true").lower() == "true",
            enable_export=os.getenv("UI_ENABLE_EXPORT", "true").lower() == "true"
        )
        
        # Security configuration
        self.security = SecurityConfig(
            secret_key=os.getenv("SECRET_KEY", "your-secret-key-change-in-production"),
            jwt_secret=os.getenv("JWT_SECRET", "your-jwt-secret-change-in-production"),
            jwt_expiration=int(os.getenv("JWT_EXPIRATION", "3600")),
            rate_limit_requests=int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
        )
        
        # Email configuration
        self.email = EmailConfig(
            smtp_host=os.getenv("SMTP_HOST", "smtp.gmail.com"),
            smtp_port=int(os.getenv("SMTP_PORT", "587")),
            smtp_user=os.getenv("SMTP_USER"),
            smtp_password=os.getenv("SMTP_PASSWORD"),
            from_email=os.getenv("FROM_EMAIL"),
            from_name=os.getenv("FROM_NAME", "JobSniper AI")
        )
        
        # Feature flags
        self.features = {
            "enable_ai_agents": os.getenv("ENABLE_AI_AGENTS", "true").lower() == "true",
            "enable_job_matching": os.getenv("ENABLE_JOB_MATCHING", "true").lower() == "true",
            "enable_skill_recommendations": os.getenv("ENABLE_SKILL_RECOMMENDATIONS", "true").lower() == "true",
            "enable_analytics": os.getenv("ENABLE_ANALYTICS", "true").lower() == "true",
            "enable_export": os.getenv("ENABLE_EXPORT", "true").lower() == "true",
            "enable_api": os.getenv("ENABLE_API", "true").lower() == "true",
            "enable_websockets": os.getenv("ENABLE_WEBSOCKETS", "false").lower() == "true",
            "enable_caching": os.getenv("ENABLE_CACHING", "true").lower() == "true",
            "enable_monitoring": os.getenv("ENABLE_MONITORING", "true").lower() == "true"
        }
        
        # Performance settings
        self.performance = {
            "cache_ttl": int(os.getenv("CACHE_TTL", "3600")),
            "max_concurrent_requests": int(os.getenv("MAX_CONCURRENT_REQUESTS", "100")),
            "request_timeout": int(os.getenv("REQUEST_TIMEOUT", "30")),
            "max_file_size": int(os.getenv("MAX_FILE_SIZE", str(10 * 1024 * 1024))),
            "enable_compression": os.getenv("ENABLE_COMPRESSION", "true").lower() == "true"
        }
    
    def get_database_url(self) -> str:
        """Get database URL with proper formatting"""
        return self.database.url
    
    def get_redis_url(self) -> str:
        """Get Redis URL with proper formatting"""
        return self.redis.url
    
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.environment == Environment.DEVELOPMENT
    
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.environment == Environment.PRODUCTION
    
    def is_testing(self) -> bool:
        """Check if running in testing mode"""
        return self.environment == Environment.TESTING
    
    def get_ai_config(self) -> Dict[str, Any]:
        """Get AI configuration as dictionary"""
        return {
            "openai_api_key": self.ai.openai_api_key,
            "gemini_api_key": self.ai.gemini_api_key,
            "anthropic_api_key": self.ai.anthropic_api_key,
            "max_tokens": self.ai.max_tokens,
            "temperature": self.ai.temperature,
            "timeout": self.ai.request_timeout
        }
    
    def validate_settings(self) -> List[str]:
        """Validate settings and return list of issues"""
        issues = []
        
        # Check required API keys in production
        if self.is_production():
            if not self.ai.openai_api_key and not self.ai.gemini_api_key:
                issues.append("At least one AI API key is required in production")
            
            if self.security.secret_key == "your-secret-key-change-in-production":
                issues.append("Secret key must be changed in production")
            
            if self.security.jwt_secret == "your-jwt-secret-change-in-production":
                issues.append("JWT secret must be changed in production")
        
        # Check database URL format
        if not self.database.url:
            issues.append("Database URL is required")
        
        # Check email configuration if email features are enabled
        if self.features.get("enable_export") and not self.email.smtp_user:
            issues.append("SMTP configuration required for email features")
        
        return issues
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary (excluding sensitive data)"""
        return {
            "app_name": self.app_name,
            "version": self.version,
            "environment": self.environment.value,
            "debug": self.debug,
            "features": self.features,
            "ui_theme": self.ui.theme,
            "log_level": self.log_level.value
        }

# Global settings instance
settings = Settings()

# Validate settings on import
validation_issues = settings.validate_settings()
if validation_issues and settings.is_production():
    import warnings
    for issue in validation_issues:
        warnings.warn(f"Configuration issue: {issue}", UserWarning)