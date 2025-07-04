"""
JobSniper AI - Core Package
===========================

Core functionality for the JobSniper AI platform including:
- Configuration management
- Database operations
- Utility functions
- Security and authentication
- Logging and monitoring

This package provides the foundation for all other components.
"""

from .config.settings import Settings
from .utils.logger import get_logger
from .utils.helpers import *

# Initialize core components
settings = Settings()
logger = get_logger(__name__)

__all__ = [
    "settings",
    "logger",
    "Settings",
    "get_logger"
]