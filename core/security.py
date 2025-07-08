"""
Security utilities for file validation and sanitization
"""
import os
import magic
import hashlib
from typing import List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

# Allowed file types and their MIME types
ALLOWED_FILE_TYPES = {
    'pdf': ['application/pdf'],
    'doc': ['application/msword'],
    'docx': ['application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
    'txt': ['text/plain'],
    'rtf': ['application/rtf', 'text/rtf']
}

# Maximum file size (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

class SecurityValidator:
    """Handles file security validation and sanitization"""
    
    @staticmethod
    def validate_file(file_path: str, allowed_extensions: List[str] = None) -> Tuple[bool, str]:
        """
        Validate uploaded file for security
        
        Args:
            file_path: Path to the file
            allowed_extensions: List of allowed file extensions
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            if not os.path.exists(file_path):
                return False, "File does not exist"
            
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > MAX_FILE_SIZE:
                return False, f"File size ({file_size} bytes) exceeds maximum allowed size ({MAX_FILE_SIZE} bytes)"
            
            if file_size == 0:
                return False, "File is empty"
            
            # Get file extension
            _, ext = os.path.splitext(file_path)
            ext = ext.lower().lstrip('.')
            
            # Check allowed extensions
            if allowed_extensions and ext not in allowed_extensions:
                return False, f"File type '{ext}' not allowed. Allowed types: {', '.join(allowed_extensions)}"
            
            # Validate MIME type
            try:
                mime_type = magic.from_file(file_path, mime=True)
                if ext in ALLOWED_FILE_TYPES:
                    if mime_type not in ALLOWED_FILE_TYPES[ext]:
                        return False, f"File MIME type '{mime_type}' doesn't match extension '{ext}'"
            except Exception as e:
                logger.warning(f"Could not determine MIME type: {e}")
            
            # Check for malicious content patterns
            if SecurityValidator._scan_for_malicious_content(file_path):
                return False, "File contains potentially malicious content"
            
            return True, "File is valid"
            
        except Exception as e:
            logger.error(f"Error validating file: {e}")
            return False, f"Validation error: {str(e)}"
    
    @staticmethod
    def _scan_for_malicious_content(file_path: str) -> bool:
        """
        Basic scan for malicious content patterns
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if malicious content detected
        """
        try:
            # Read first 1KB for basic pattern matching
            with open(file_path, 'rb') as f:
                content = f.read(1024)
            
            # Check for suspicious patterns
            suspicious_patterns = [
                b'<script',
                b'javascript:',
                b'vbscript:',
                b'onload=',
                b'onerror=',
                b'eval(',
                b'exec(',
                b'system(',
                b'shell_exec'
            ]
            
            content_lower = content.lower()
            for pattern in suspicious_patterns:
                if pattern in content_lower:
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error scanning file content: {e}")
            return True  # Err on the side of caution
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename to prevent path traversal attacks
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename
        """
        # Remove path components
        filename = os.path.basename(filename)
        
        # Remove or replace dangerous characters
        dangerous_chars = ['..', '/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in dangerous_chars:
            filename = filename.replace(char, '_')
        
        # Limit length
        if len(filename) > 255:
            name, ext = os.path.splitext(filename)
            filename = name[:250] + ext
        
        return filename
    
    @staticmethod
    def generate_secure_filename(original_filename: str) -> str:
        """
        Generate a secure filename with hash
        
        Args:
            original_filename: Original filename
            
        Returns:
            Secure filename with hash
        """
        # Sanitize original filename
        safe_name = SecurityValidator.sanitize_filename(original_filename)
        
        # Generate hash
        hash_obj = hashlib.md5(safe_name.encode())
        file_hash = hash_obj.hexdigest()[:8]
        
        # Combine with timestamp
        import time
        timestamp = str(int(time.time()))
        
        name, ext = os.path.splitext(safe_name)
        return f"{name}_{timestamp}_{file_hash}{ext}"