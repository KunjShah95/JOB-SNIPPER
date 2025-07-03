"""Centralized error handling for JobSniper AI

Provides consistent error handling, logging, and user-friendly
error messages across the entire application.
"""

import logging
import traceback
import streamlit as st
from typing import Dict, Any, Optional, Callable
from datetime import datetime
from functools import wraps
import json


class JobSniperError(Exception):
    """Base exception class for JobSniper AI"""
    def __init__(self, message: str, error_code: str = None, details: Dict = None):
        self.message = message
        self.error_code = error_code or "GENERAL_ERROR"
        self.details = details or {}
        self.timestamp = datetime.now()
        super().__init__(self.message)


class AIProviderError(JobSniperError):
    """Error related to AI provider issues"""
    def __init__(self, provider: str, message: str, details: Dict = None):
        self.provider = provider
        super().__init__(
            message=f"AI Provider ({provider}) Error: {message}",
            error_code="AI_PROVIDER_ERROR",
            details=details
        )


class ValidationError(JobSniperError):
    """Error related to input validation"""
    def __init__(self, field: str, message: str, details: Dict = None):
        self.field = field
        super().__init__(
            message=f"Validation Error ({field}): {message}",
            error_code="VALIDATION_ERROR",
            details=details
        )


class FileProcessingError(JobSniperError):
    """Error related to file processing"""
    def __init__(self, filename: str, message: str, details: Dict = None):
        self.filename = filename
        super().__init__(
            message=f"File Processing Error ({filename}): {message}",
            error_code="FILE_PROCESSING_ERROR",
            details=details
        )


class DatabaseError(JobSniperError):
    """Error related to database operations"""
    def __init__(self, operation: str, message: str, details: Dict = None):
        self.operation = operation
        super().__init__(
            message=f"Database Error ({operation}): {message}",
            error_code="DATABASE_ERROR",
            details=details
        )


class ErrorHandler:
    """Centralized error handling and logging"""
    
    def __init__(self, logger_name: str = "JobSniper"):
        self.logger = logging.getLogger(logger_name)
        self.error_counts = {}
        
    def log_error(self, error: Exception, context: str = "", 
                  user_data: Dict = None, show_user: bool = True) -> Dict[str, Any]:
        """Log error with context and return user-friendly response"""
        
        error_id = f"ERR_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # Count error types
        error_type = type(error).__name__
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        
        # Prepare error details
        error_details = {
            'error_id': error_id,
            'error_type': error_type,
            'message': str(error),
            'context': context,
            'timestamp': datetime.now().isoformat(),
            'traceback': traceback.format_exc(),
            'user_data': user_data or {}
        }
        
        # Log the error
        self.logger.error(f"Error {error_id}: {error_details}")
        
        # Show user-friendly message in Streamlit
        if show_user:
            self._show_user_error(error, error_id, context)
        
        return {
            'success': False,
            'error_id': error_id,
            'error_type': error_type,
            'message': self._get_user_message(error),
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_user_message(self, error: Exception) -> str:
        """Get user-friendly error message"""
        
        if isinstance(error, AIProviderError):
            return f"AI service temporarily unavailable ({error.provider}). Please try again or use demo mode."
        
        elif isinstance(error, ValidationError):
            return f"Please check your input: {error.message}"
        
        elif isinstance(error, FileProcessingError):
            return f"Could not process file '{error.filename}'. Please ensure it's a valid resume file."
        
        elif isinstance(error, DatabaseError):
            return "Database temporarily unavailable. Your data has not been saved."
        
        elif "API key" in str(error).lower():
            return "API configuration issue. Please check your API keys in settings."
        
        elif "network" in str(error).lower() or "connection" in str(error).lower():
            return "Network connection issue. Please check your internet connection and try again."
        
        elif "timeout" in str(error).lower():
            return "Request timed out. Please try again with a smaller file or simpler request."
        
        else:
            return "An unexpected error occurred. Please try again or contact support if the issue persists."
    
    def _show_user_error(self, error: Exception, error_id: str, context: str):
        """Show user-friendly error in Streamlit interface"""
        
        user_message = self._get_user_message(error)
        
        if isinstance(error, (AIProviderError, ValidationError)):
            st.warning(f"⚠️ {user_message}")
        else:
            st.error(f"❌ {user_message}")
        
        # Show error ID for support
        with st.expander("🔍 Error Details (for support)"):
            st.code(f"Error ID: {error_id}")
            if context:
                st.code(f"Context: {context}")
            
            # Show suggestions based on error type
            if isinstance(error, AIProviderError):
                st.info("💡 **Suggestions:**\n- Check your API key configuration\n- Try using demo mode\n- Wait a few minutes and try again")
            elif isinstance(error, FileProcessingError):
                st.info("💡 **Suggestions:**\n- Ensure file is a PDF, DOC, or DOCX\n- Check file is not corrupted\n- Try a different file")
            elif isinstance(error, ValidationError):
                st.info("💡 **Suggestions:**\n- Check all required fields are filled\n- Verify email format is correct\n- Ensure file meets requirements")
    
    def get_error_stats(self) -> Dict[str, Any]:
        """Get error statistics"""
        total_errors = sum(self.error_counts.values())
        return {
            'total_errors': total_errors,
            'error_types': dict(self.error_counts),
            'most_common': max(self.error_counts.items(), key=lambda x: x[1]) if self.error_counts else None
        }


def handle_errors(context: str = "", show_user: bool = True, 
                 fallback_result: Any = None):
    """Decorator for automatic error handling"""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_handler = ErrorHandler()
                error_result = error_handler.log_error(
                    error=e,
                    context=context or func.__name__,
                    show_user=show_user
                )
                
                if fallback_result is not None:
                    return fallback_result
                else:
                    return error_result
        return wrapper
    return decorator


def safe_execute(func: Callable, *args, context: str = "", 
                fallback_result: Any = None, **kwargs) -> Any:
    """Safely execute a function with error handling"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        error_handler = ErrorHandler()
        error_handler.log_error(
            error=e,
            context=context or func.__name__,
            show_user=True
        )
        return fallback_result


def validate_and_execute(validation_func: Callable, 
                        execution_func: Callable,
                        data: Any,
                        context: str = "") -> Dict[str, Any]:
    """Validate data and execute function with error handling"""
    try:
        # Validate first
        validation_result = validation_func(data)
        if not validation_result.get('valid', False):
            raise ValidationError(
                field="input_data",
                message="; ".join(validation_result.get('errors', ['Validation failed'])),
                details=validation_result
            )
        
        # Execute if validation passes
        result = execution_func(data)
        return {
            'success': True,
            'result': result,
            'validation': validation_result
        }
        
    except Exception as e:
        error_handler = ErrorHandler()
        return error_handler.log_error(
            error=e,
            context=context,
            user_data={'input_data_type': type(data).__name__}
        )


# Global error handler instance
global_error_handler = ErrorHandler()


# Convenience functions
def log_error(error: Exception, context: str = "", show_user: bool = True) -> Dict[str, Any]:
    """Quick error logging"""
    return global_error_handler.log_error(error, context, show_user=show_user)


def show_success(message: str, details: str = ""):
    """Show success message in Streamlit"""
    st.success(f"✅ {message}")
    if details:
        with st.expander("📋 Details"):
            st.info(details)


def show_warning(message: str, details: str = ""):
    """Show warning message in Streamlit"""
    st.warning(f"⚠️ {message}")
    if details:
        with st.expander("ℹ️ More Information"):
            st.info(details)


def show_info(message: str, details: str = ""):
    """Show info message in Streamlit"""
    st.info(f"ℹ️ {message}")
    if details:
        with st.expander("📖 Details"):
            st.write(details)