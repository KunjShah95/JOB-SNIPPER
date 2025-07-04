"""
JobSniper AI - Advanced Logging System
======================================

Comprehensive logging system with structured logging, performance tracking,
and integration with monitoring systems.
"""

import logging
import logging.handlers
import sys
import json
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Union
from contextlib import contextmanager
import time
import functools

class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured JSON"""
        
        # Base log data
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add exception information if present
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": traceback.format_exception(*record.exc_info)
            }
        
        # Add extra fields
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)
        
        # Add performance metrics if present
        if hasattr(record, "performance"):
            log_data["performance"] = record.performance
        
        # Add user context if present
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        
        if hasattr(record, "session_id"):
            log_data["session_id"] = record.session_id
        
        return json.dumps(log_data, default=str)

class PerformanceLogger:
    """Logger for performance metrics and timing"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    @contextmanager
    def timer(self, operation: str, **kwargs):
        """Context manager for timing operations"""
        start_time = time.time()
        start_memory = self._get_memory_usage()
        
        try:
            yield
            success = True
            error = None
        except Exception as e:
            success = False
            error = str(e)
            raise
        finally:
            end_time = time.time()
            end_memory = self._get_memory_usage()
            
            performance_data = {
                "operation": operation,
                "duration_ms": round((end_time - start_time) * 1000, 2),
                "memory_start_mb": round(start_memory / 1024 / 1024, 2),
                "memory_end_mb": round(end_memory / 1024 / 1024, 2),
                "memory_delta_mb": round((end_memory - start_memory) / 1024 / 1024, 2),
                "success": success,
                "error": error,
                **kwargs
            }
            
            # Log performance data
            extra = {"performance": performance_data}
            if success:
                self.logger.info(f"Performance: {operation}", extra=extra)
            else:
                self.logger.error(f"Performance: {operation} failed", extra=extra)
    
    def _get_memory_usage(self) -> int:
        """Get current memory usage in bytes"""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss
        except ImportError:
            return 0

class JobSniperLogger:
    """Main logger class for JobSniper AI"""
    
    def __init__(self, name: str = "jobsniper"):
        self.name = name
        self.logger = logging.getLogger(name)
        self.performance = PerformanceLogger(self.logger)
        self._setup_logger()
    
    def _setup_logger(self):
        """Setup logger with appropriate handlers and formatters"""
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Set log level from environment or default to INFO
        import os
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        self.logger.setLevel(getattr(logging, log_level, logging.INFO))
        
        # Console handler with structured formatting
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(StructuredFormatter())
        self.logger.addHandler(console_handler)
        
        # File handler for persistent logging
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / "jobsniper.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(StructuredFormatter())
        self.logger.addHandler(file_handler)
        
        # Error file handler for errors only
        error_handler = logging.handlers.RotatingFileHandler(
            log_dir / "jobsniper_errors.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(StructuredFormatter())
        self.logger.addHandler(error_handler)
        
        # Prevent propagation to root logger
        self.logger.propagate = False
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self._log(logging.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self._log(logging.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self._log(logging.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        self._log(logging.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self._log(logging.CRITICAL, message, **kwargs)
    
    def exception(self, message: str, **kwargs):
        """Log exception with traceback"""
        kwargs["exc_info"] = True
        self._log(logging.ERROR, message, **kwargs)
    
    def _log(self, level: int, message: str, **kwargs):
        """Internal logging method"""
        extra = {}
        
        # Extract special fields
        if "user_id" in kwargs:
            extra["user_id"] = kwargs.pop("user_id")
        
        if "session_id" in kwargs:
            extra["session_id"] = kwargs.pop("session_id")
        
        if "extra_fields" in kwargs:
            extra["extra_fields"] = kwargs.pop("extra_fields")
        
        # Add remaining kwargs as extra fields
        if kwargs:
            extra["extra_fields"] = kwargs
        
        self.logger.log(level, message, extra=extra)
    
    def log_api_request(self, method: str, endpoint: str, status_code: int, 
                       duration_ms: float, user_id: Optional[str] = None):
        """Log API request"""
        self.info(
            f"API Request: {method} {endpoint}",
            extra_fields={
                "api_method": method,
                "api_endpoint": endpoint,
                "api_status_code": status_code,
                "api_duration_ms": duration_ms
            },
            user_id=user_id
        )
    
    def log_ai_request(self, model: str, tokens_used: int, cost: float, 
                      duration_ms: float, success: bool = True):
        """Log AI model request"""
        level = logging.INFO if success else logging.ERROR
        self._log(
            level,
            f"AI Request: {model}",
            extra_fields={
                "ai_model": model,
                "ai_tokens_used": tokens_used,
                "ai_cost": cost,
                "ai_duration_ms": duration_ms,
                "ai_success": success
            }
        )
    
    def log_user_action(self, action: str, user_id: str, session_id: str, 
                       details: Optional[Dict[str, Any]] = None):
        """Log user action"""
        self.info(
            f"User Action: {action}",
            user_id=user_id,
            session_id=session_id,
            extra_fields={
                "user_action": action,
                "action_details": details or {}
            }
        )
    
    def log_performance_metric(self, metric_name: str, value: Union[int, float], 
                             unit: str = "", tags: Optional[Dict[str, str]] = None):
        """Log performance metric"""
        self.info(
            f"Performance Metric: {metric_name}",
            extra_fields={
                "metric_name": metric_name,
                "metric_value": value,
                "metric_unit": unit,
                "metric_tags": tags or {}
            }
        )
    
    def log_business_event(self, event_type: str, event_data: Dict[str, Any], 
                          user_id: Optional[str] = None):
        """Log business event"""
        self.info(
            f"Business Event: {event_type}",
            user_id=user_id,
            extra_fields={
                "event_type": event_type,
                "event_data": event_data
            }
        )

def get_logger(name: str = "jobsniper") -> JobSniperLogger:
    """Get or create a logger instance"""
    return JobSniperLogger(name)

def log_execution_time(func):
    """Decorator to log function execution time"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        
        with logger.performance.timer(
            operation=f"{func.__module__}.{func.__name__}",
            function=func.__name__,
            module=func.__module__
        ):
            return func(*args, **kwargs)
    
    return wrapper

def log_api_call(func):
    """Decorator to log API calls"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            duration_ms = (time.time() - start_time) * 1000
            
            logger.log_api_request(
                method=getattr(func, "__method__", "UNKNOWN"),
                endpoint=getattr(func, "__endpoint__", func.__name__),
                status_code=200,
                duration_ms=duration_ms
            )
            
            return result
        
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            logger.log_api_request(
                method=getattr(func, "__method__", "UNKNOWN"),
                endpoint=getattr(func, "__endpoint__", func.__name__),
                status_code=500,
                duration_ms=duration_ms
            )
            
            logger.exception(f"API call failed: {func.__name__}")
            raise
    
    return wrapper

# Global logger instance
logger = get_logger()

# Export main components
__all__ = [
    "JobSniperLogger",
    "PerformanceLogger",
    "StructuredFormatter",
    "get_logger",
    "log_execution_time",
    "log_api_call",
    "logger"
]