"""
Validation utilities for JobSniper AI
=====================================

File validation, data validation, and input sanitization functions.
"""

import os
import mimetypes
from typing import Dict, List, Any, Tuple
import streamlit as st

# Try to import python-magic, but handle gracefully if not available
try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False


def validate_resume_upload(file_path: str) -> Dict[str, Any]:
    """
    Validate uploaded resume file for security and format compliance.
    
    Args:
        file_path (str): Path to the uploaded file
        
    Returns:
        Dict containing validation results with 'valid' boolean and 'errors' list
    """
    validation_result = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'file_info': {}
    }
    
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            validation_result['valid'] = False
            validation_result['errors'].append("File does not exist")
            return validation_result
        
        # Get file info
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1].lower()
        
        validation_result['file_info'] = {
            'name': file_name,
            'size': file_size,
            'extension': file_ext
        }
        
        # Validate file size (max 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if file_size > max_size:
            validation_result['valid'] = False
            validation_result['errors'].append(f"File size ({file_size:,} bytes) exceeds maximum allowed size ({max_size:,} bytes)")
        
        # Validate file extension
        allowed_extensions = ['.pdf', '.doc', '.docx', '.txt']
        if file_ext not in allowed_extensions:
            validation_result['valid'] = False
            validation_result['errors'].append(f"File extension '{file_ext}' not allowed. Allowed: {', '.join(allowed_extensions)}")
        
        # Validate MIME type
        try:
            mime_type, _ = mimetypes.guess_type(file_path)
            allowed_mime_types = [
                'application/pdf',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'text/plain'
            ]
            
            if mime_type not in allowed_mime_types:
                validation_result['warnings'].append(f"MIME type '{mime_type}' may not be supported")
        except Exception as e:
            validation_result['warnings'].append(f"Could not determine MIME type: {str(e)}")
        
        # Check for empty file
        if file_size == 0:
            validation_result['valid'] = False
            validation_result['errors'].append("File is empty")
        
        # Additional security checks
        if file_size < 100:  # Very small files are suspicious
            validation_result['warnings'].append("File is very small and may not contain meaningful content")
        
        # Check file magic number (if python-magic is available)
        if MAGIC_AVAILABLE:
            try:
                file_type = magic.from_file(file_path)
                validation_result['file_info']['detected_type'] = file_type

                # Basic magic number validation
                if file_ext == '.pdf' and 'PDF' not in file_type:
                    validation_result['warnings'].append("File extension doesn't match detected file type")
                elif file_ext in ['.doc', '.docx'] and 'Microsoft' not in file_type and 'Office' not in file_type:
                    validation_result['warnings'].append("File extension doesn't match detected file type")

            except Exception as e:
                validation_result['warnings'].append(f"File type detection failed: {str(e)}")
        else:
            # python-magic not available, skip magic number check
            validation_result['warnings'].append("Advanced file type detection not available")
    
    except Exception as e:
        validation_result['valid'] = False
        validation_result['errors'].append(f"Validation error: {str(e)}")
    
    return validation_result


def validate_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    import re
    
    if not email or not isinstance(email, str):
        return False
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email.strip()) is not None


def validate_phone_number(phone: str) -> bool:
    """
    Validate phone number format.
    
    Args:
        phone (str): Phone number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    import re
    
    if not phone or not isinstance(phone, str):
        return False
    
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    
    # Check if it's a valid length (7-15 digits)
    return 7 <= len(digits_only) <= 15


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal and other security issues.
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Sanitized filename
    """
    import re
    
    if not filename:
        return "unnamed_file"
    
    # Remove path components
    filename = os.path.basename(filename)
    
    # Replace dangerous characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing dots and spaces
    filename = filename.strip('. ')
    
    # Ensure it's not empty after sanitization
    if not filename:
        return "unnamed_file"
    
    return filename


def validate_job_application_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate job application data.
    
    Args:
        data (Dict): Job application data to validate
        
    Returns:
        Dict: Validation results
    """
    validation_result = {
        'valid': True,
        'errors': [],
        'warnings': []
    }
    
    required_fields = ['job_title', 'company', 'status']
    
    for field in required_fields:
        if field not in data or not data[field]:
            validation_result['valid'] = False
            validation_result['errors'].append(f"Required field '{field}' is missing or empty")
    
    # Validate email if provided
    if 'contact_email' in data and data['contact_email']:
        if not validate_email(data['contact_email']):
            validation_result['warnings'].append("Invalid email format")
    
    # Validate phone if provided
    if 'contact_phone' in data and data['contact_phone']:
        if not validate_phone_number(data['contact_phone']):
            validation_result['warnings'].append("Invalid phone number format")
    
    return validation_result


def validate_user_input(input_text: str, max_length: int = 1000, allow_html: bool = False) -> Dict[str, Any]:
    """
    Validate and sanitize user input.
    
    Args:
        input_text (str): User input to validate
        max_length (int): Maximum allowed length
        allow_html (bool): Whether to allow HTML tags
        
    Returns:
        Dict: Validation results with sanitized text
    """
    validation_result = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'sanitized_text': input_text
    }
    
    if not isinstance(input_text, str):
        validation_result['valid'] = False
        validation_result['errors'].append("Input must be a string")
        return validation_result
    
    # Check length
    if len(input_text) > max_length:
        validation_result['valid'] = False
        validation_result['errors'].append(f"Input exceeds maximum length of {max_length} characters")
    
    # Sanitize HTML if not allowed
    if not allow_html:
        import html
        sanitized = html.escape(input_text)
        if sanitized != input_text:
            validation_result['warnings'].append("HTML characters were escaped")
            validation_result['sanitized_text'] = sanitized
    
    return validation_result
