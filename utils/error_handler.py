# Simple direct-use handler for agents and UI
def handle_exception(e, context: str = "", show_user: bool = True):
    """Log and show error using the global error handler."""
    global_error_handler.log_error(e, context=context, show_user=show_user)
"""Error Handler for JobSniper AI

Provides centralized error handling, logging, and user-friendly error messages.
"""

import logging
import streamlit as st
import traceback
from datetime import datetime
from typing import Dict, Any, Optional
import json


class GlobalErrorHandler:
    """Centralized error handling system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_count = 0
        self.error_history = []
    
    def log_error(self, error: Exception, context: str = "", show_user: bool = True) -> Dict[str, Any]:
        """Log error and optionally show to user"""
        
        self.error_count += 1
        error_id = f"ERR_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self.error_count}"
        
        # Create error record
        error_record = {
            "id": error_id,
            "timestamp": datetime.now().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
            "traceback": traceback.format_exc(),
            "session_id": st.session_state.get("user_session", {}).get("session_id", "unknown")
        }
        
        # Add to history (keep last 50 errors)
        self.error_history.append(error_record)
        if len(self.error_history) > 50:
            self.error_history.pop(0)
        
        # Log to system
        self.logger.error(f"[{error_id}] {context}: {error}")
        self.logger.debug(f"[{error_id}] Traceback: {traceback.format_exc()}")
        
        # Show to user if requested
        if show_user:
            self._show_user_error(error_record)
        
        return error_record
    
    def _show_user_error(self, error_record: Dict[str, Any]):
        """Show user-friendly error message"""
        
        error_type = error_record["error_type"]
        context = error_record["context"]
        
        # Determine user-friendly message based on error type
        if "import" in str(error_record["error_message"]).lower():
            user_message = "🔧 Missing component detected. Please check your installation."
        elif "connection" in str(error_record["error_message"]).lower():
            user_message = "🌐 Connection issue. Please check your internet connection."
        elif "api" in str(error_record["error_message"]).lower():
            user_message = "🔑 API configuration issue. Please check your settings."
        elif "file" in str(error_record["error_message"]).lower():
            user_message = "📁 File access issue. Please check file permissions."
        else:
            user_message = f"⚠️ An error occurred in {context}. Please try again."
        
        # Show error to user
        st.error(f"{user_message}")
        
        # Show details in expander for debugging
        with st.expander("🔍 Error Details (for debugging)"):
            st.code(f"""
Error ID: {error_record['id']}
Type: {error_type}
Context: {context}
Message: {error_record['error_message']}
Time: {error_record['timestamp']}
            """)
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of recent errors"""
        
        if not self.error_history:
            return {"total_errors": 0, "recent_errors": []}
        
        # Get error types count
        error_types = {}
        for error in self.error_history:
            error_type = error["error_type"]
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        return {
            "total_errors": len(self.error_history),
            "error_types": error_types,
            "recent_errors": self.error_history[-5:],  # Last 5 errors
            "last_error_time": self.error_history[-1]["timestamp"] if self.error_history else None
        }
    
    def clear_error_history(self):
        """Clear error history"""
        self.error_history = []
        self.error_count = 0


# Global instance
global_error_handler = GlobalErrorHandler()


def show_warning(message: str, details: str = ""):
    """Show warning message to user"""
    st.warning(f"⚠️ {message}")
    if details:
        with st.expander("Details"):
            st.write(details)


def show_info(message: str, details: str = ""):
    """Show info message to user"""
    st.info(f"ℹ️ {message}")
    if details:
        with st.expander("Details"):
            st.write(details)


def show_success(message: str, details: str = ""):
    """Show success message to user"""
    st.success(f"✅ {message}")
    if details:
        with st.expander("Details"):
            st.write(details)


def handle_api_error(error: Exception, api_name: str = "API") -> bool:
    """Handle API-specific errors"""
    
    error_msg = str(error).lower()
    
    if "api key" in error_msg or "unauthorized" in error_msg:
        st.error(f"🔑 {api_name} authentication failed. Please check your API key in Settings.")
        return False
    elif "rate limit" in error_msg or "quota" in error_msg:
        st.warning(f"⏱️ {api_name} rate limit reached. Please try again later.")
        return False
    elif "timeout" in error_msg:
        st.warning(f"⏰ {api_name} request timed out. Please try again.")
        return False
    else:
        st.error(f"❌ {api_name} error: {error}")
        return False


def safe_execute(func, *args, fallback_result=None, show_errors=True, **kwargs):
    """Safely execute a function with error handling"""
    
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if show_errors:
            global_error_handler.log_error(
                error=e,
                context=f"Function: {func.__name__}",
                show_user=True
            )
        return fallback_result


class ErrorBoundary:
    """Context manager for error boundaries"""
    
    def __init__(self, context: str, show_user: bool = True, fallback_ui=None):
        self.context = context
        self.show_user = show_user
        self.fallback_ui = fallback_ui
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            global_error_handler.log_error(
                error=exc_val,
                context=self.context,
                show_user=self.show_user
            )
            
            if self.fallback_ui:
                self.fallback_ui()
            
            return True  # Suppress the exception
        return False


def with_error_boundary(context: str, show_user: bool = True):
    """Decorator for error boundaries"""
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                global_error_handler.log_error(
                    error=e,
                    context=f"{context}: {func.__name__}",
                    show_user=show_user
                )
                return None
        return wrapper
    return decorator
