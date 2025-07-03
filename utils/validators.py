"""Input validation utilities for JobSniper AI

Provides comprehensive validation for user inputs, file uploads,
API keys, and other data to ensure security and reliability.
"""

import re
import os
import magic
from typing import Dict, List, Optional, Tuple, Any
from email_validator import validate_email, EmailNotValidError
import logging

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class FileValidator:
    """Validates uploaded files for security and format compliance"""
    
    ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_MIME_TYPES = {
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain'
    }
    
    @classmethod
    def validate_resume_file(cls, file_path: str, file_content: bytes = None) -> Dict[str, Any]:
        """Validate resume file upload"""
        result = {
            'valid': False,
            'errors': [],
            'warnings': [],
            'file_info': {}
        }
        
        try:
            # Check file existence
            if not os.path.exists(file_path):
                result['errors'].append("File does not exist")
                return result
            
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > cls.MAX_FILE_SIZE:
                result['errors'].append(f"File too large: {file_size} bytes (max: {cls.MAX_FILE_SIZE})")
                return result
            
            if file_size == 0:
                result['errors'].append("File is empty")
                return result
            
            # Check file extension
            _, ext = os.path.splitext(file_path.lower())
            if ext not in cls.ALLOWED_EXTENSIONS:
                result['errors'].append(f"Invalid file extension: {ext}")
                return result
            
            # Check MIME type using python-magic
            try:
                mime_type = magic.from_file(file_path, mime=True)
                if mime_type not in cls.ALLOWED_MIME_TYPES:
                    result['errors'].append(f"Invalid file type: {mime_type}")
                    return result
            except Exception as e:
                result['warnings'].append(f"Could not verify MIME type: {e}")
            
            # File info
            result['file_info'] = {
                'size': file_size,
                'extension': ext,
                'mime_type': mime_type if 'mime_type' in locals() else 'unknown'
            }
            
            result['valid'] = True
            return result
            
        except Exception as e:
            result['errors'].append(f"Validation error: {str(e)}")
            return result


class APIKeyValidator:
    """Validates API keys for various services"""
    
    @staticmethod
    def validate_gemini_key(api_key: str) -> bool:
        """Validate Google Gemini API key format"""
        if not api_key or not isinstance(api_key, str):
            return False
        
        # Gemini keys start with "AIza" and are typically 39 characters
        pattern = r'^AIza[A-Za-z0-9_-]{35}$'
        return bool(re.match(pattern, api_key.strip()))
    
    @staticmethod
    def validate_mistral_key(api_key: str) -> bool:
        """Validate Mistral AI API key format"""
        if not api_key or not isinstance(api_key, str):
            return False
        
        # Mistral keys are typically longer and alphanumeric
        return len(api_key.strip()) >= 20 and api_key.strip().replace('-', '').replace('_', '').isalnum()
    
    @staticmethod
    def validate_firecrawl_key(api_key: str) -> bool:
        """Validate Firecrawl API key format"""
        if not api_key or not isinstance(api_key, str):
            return False
        
        # Basic validation for Firecrawl keys
        return len(api_key.strip()) >= 10


class EmailValidator:
    """Validates email addresses and configurations"""
    
    @staticmethod
    def validate_email_address(email: str) -> Tuple[bool, str]:
        """Validate email address format"""
        try:
            # Validate and get info about the email
            valid = validate_email(email)
            return True, valid.email
        except EmailNotValidError as e:
            return False, str(e)
    
    @staticmethod
    def validate_email_config(email: str, password: str) -> Dict[str, Any]:
        """Validate email configuration"""
        result = {
            'valid': False,
            'errors': [],
            'warnings': []
        }
        
        # Validate email format
        email_valid, email_msg = EmailValidator.validate_email_address(email)
        if not email_valid:
            result['errors'].append(f"Invalid email: {email_msg}")
        
        # Validate password
        if not password or len(password.strip()) < 8:
            result['errors'].append("Password too short (minimum 8 characters)")
        
        # Check for common placeholder values
        if email in ['your_gmail@gmail.com', 'your_email@gmail.com']:
            result['errors'].append("Please replace placeholder email with actual email")
        
        if password in ['your_app_password', 'your_password']:
            result['errors'].append("Please replace placeholder password with actual password")
        
        result['valid'] = len(result['errors']) == 0
        return result


class InputSanitizer:
    """Sanitizes user inputs to prevent injection attacks"""
    
    @staticmethod
    def sanitize_text(text: str, max_length: int = 10000) -> str:
        """Sanitize text input"""
        if not isinstance(text, str):
            return ""
        
        # Remove null bytes and control characters
        text = text.replace('\x00', '').replace('\r', '\n')
        
        # Limit length
        if len(text) > max_length:
            text = text[:max_length]
        
        # Remove potentially dangerous patterns
        dangerous_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'vbscript:',
            r'onload=',
            r'onerror=',
        ]
        
        for pattern in dangerous_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.DOTALL)
        
        return text.strip()
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe storage"""
        if not isinstance(filename, str):
            return "unknown_file"
        
        # Remove path separators and dangerous characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = re.sub(r'\.\.+', '.', filename)
        
        # Limit length
        if len(filename) > 255:
            name, ext = os.path.splitext(filename)
            filename = name[:250] + ext
        
        return filename.strip()


class ConfigValidator:
    """Validates application configuration"""
    
    @staticmethod
    def validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate complete application configuration"""
        result = {
            'valid': False,
            'errors': [],
            'warnings': [],
            'ai_providers': [],
            'features_enabled': []
        }
        
        # Validate AI providers
        if config.get('gemini_api_key'):
            if APIKeyValidator.validate_gemini_key(config['gemini_api_key']):
                result['ai_providers'].append('gemini')
            else:
                result['warnings'].append("Invalid Gemini API key format")
        
        if config.get('mistral_api_key'):
            if APIKeyValidator.validate_mistral_key(config['mistral_api_key']):
                result['ai_providers'].append('mistral')
            else:
                result['warnings'].append("Invalid Mistral API key format")
        
        # Check if at least one AI provider is available
        if not result['ai_providers']:
            result['errors'].append("No valid AI providers configured")
        
        # Validate email configuration
        if config.get('sender_email') and config.get('sender_password'):
            email_validation = EmailValidator.validate_email_config(
                config['sender_email'], 
                config['sender_password']
            )
            if email_validation['valid']:
                result['features_enabled'].append('email_reports')
            else:
                result['warnings'].extend(email_validation['errors'])
        
        # Validate optional features
        if config.get('firecrawl_api_key'):
            if APIKeyValidator.validate_firecrawl_key(config['firecrawl_api_key']):
                result['features_enabled'].append('web_scraping')
            else:
                result['warnings'].append("Invalid Firecrawl API key format")
        
        # Check cookie key
        if not config.get('cookie_key') or len(config.get('cookie_key', '')) < 16:
            result['warnings'].append("Cookie key should be at least 16 characters for security")
        
        result['valid'] = len(result['errors']) == 0
        return result


# Convenience functions for common validations
def validate_resume_upload(file_path: str) -> Dict[str, Any]:
    """Quick validation for resume uploads"""
    return FileValidator.validate_resume_file(file_path)


def validate_api_keys(gemini_key: str = None, mistral_key: str = None) -> Dict[str, bool]:
    """Quick validation for API keys"""
    return {
        'gemini_valid': APIKeyValidator.validate_gemini_key(gemini_key) if gemini_key else False,
        'mistral_valid': APIKeyValidator.validate_mistral_key(mistral_key) if mistral_key else False
    }


def sanitize_user_input(text: str) -> str:
    """Quick sanitization for user text input"""
    return InputSanitizer.sanitize_text(text)