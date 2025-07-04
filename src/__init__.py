"""
JobSniper AI - Source Package
=============================

This package contains the core source code for JobSniper AI,
a next-generation career intelligence platform.

Modules:
- agents: AI agent system for resume analysis and job matching
- ui: User interface components and pages
- core: Core functionality and utilities
- analytics: Analytics and reporting system
- api: REST API endpoints and WebSocket handlers

Version: 2.0.0
Author: JobSniper AI Team
License: MIT
"""

__version__ = "2.0.0"
__author__ = "JobSniper AI Team"
__license__ = "MIT"

# Package metadata
PACKAGE_INFO = {
    "name": "jobsniper-ai",
    "version": __version__,
    "description": "Next-generation career intelligence platform",
    "author": __author__,
    "license": __license__,
    "python_requires": ">=3.8",
    "keywords": ["ai", "career", "resume", "job-matching", "ml"],
    "url": "https://github.com/KunjShah95/JOB-SNIPPER"
}

# Import core components
try:
    from .core.config import settings
    from .core.utils import logger
    
    logger.info(f"JobSniper AI v{__version__} initialized")
    
except ImportError:
    # Graceful handling if core components aren't available yet
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info(f"JobSniper AI v{__version__} - Core components loading...")

# Export main components
__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "PACKAGE_INFO"
]