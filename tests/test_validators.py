"""Tests for validation utilities"""

import pytest
import tempfile
import os
from utils.validators import (
    FileValidator, APIKeyValidator, EmailValidator, 
    InputSanitizer, ConfigValidator, validate_resume_upload
)


class TestFileValidator:
    """Test file validation functionality"""
    
    def test_validate_resume_file_valid_pdf(self):
        """Test validation of valid PDF file"""
        # Create a temporary PDF-like file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            tmp.write(b'%PDF-1.4\n%Test PDF content')
            tmp_path = tmp.name
        
        try:
            result = FileValidator.validate_resume_file(tmp_path)
            assert result['valid'] == True
            assert result['file_info']['extension'] == '.pdf'
        finally:
            os.unlink(tmp_path)
    
    def test_validate_resume_file_invalid_extension(self):
        """Test validation of file with invalid extension"""
        with tempfile.NamedTemporaryFile(suffix='.exe', delete=False) as tmp:
            tmp.write(b'test content')
            tmp_path = tmp.name
        
        try:
            result = FileValidator.validate_resume_file(tmp_path)
            assert result['valid'] == False
            assert any('Invalid file extension' in error for error in result['errors'])
        finally:
            os.unlink(tmp_path)
    
    def test_validate_resume_file_too_large(self):
        """Test validation of file that's too large"""
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            # Write more than 10MB
            tmp.write(b'x' * (11 * 1024 * 1024))
            tmp_path = tmp.name
        
        try:
            result = FileValidator.validate_resume_file(tmp_path)
            assert result['valid'] == False
            assert any('File too large' in error for error in result['errors'])
        finally:
            os.unlink(tmp_path)
    
    def test_validate_resume_file_empty(self):
        """Test validation of empty file"""
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            result = FileValidator.validate_resume_file(tmp_path)
            assert result['valid'] == False
            assert any('File is empty' in error for error in result['errors'])
        finally:
            os.unlink(tmp_path)


class TestAPIKeyValidator:
    """Test API key validation"""
    
    def test_validate_gemini_key_valid(self):
        """Test valid Gemini API key"""
        valid_key = "AIzaSyDhZjKjKjKjKjKjKjKjKjKjKjKjKjKjKjK"
        assert APIKeyValidator.validate_gemini_key(valid_key) == True
    
    def test_validate_gemini_key_invalid_format(self):
        """Test invalid Gemini API key format"""
        invalid_keys = [
            "invalid_key",
            "AIza123",  # Too short
            "BIzaSyDhZjKjKjKjKjKjKjKjKjKjKjKjKjKjKjKjK",  # Wrong prefix
            "",
            None
        ]
        
        for key in invalid_keys:
            assert APIKeyValidator.validate_gemini_key(key) == False
    
    def test_validate_mistral_key_valid(self):
        """Test valid Mistral API key"""
        valid_key = "abcdefghijklmnopqrstuvwxyz123456"
        assert APIKeyValidator.validate_mistral_key(valid_key) == True
    
    def test_validate_mistral_key_invalid(self):
        """Test invalid Mistral API key"""
        invalid_keys = [
            "short",  # Too short
            "",
            None,
            "key with spaces and special chars!"
        ]
        
        for key in invalid_keys:
            assert APIKeyValidator.validate_mistral_key(key) == False


class TestEmailValidator:
    """Test email validation"""
    
    def test_validate_email_address_valid(self):
        """Test valid email addresses"""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org"
        ]
        
        for email in valid_emails:
            is_valid, _ = EmailValidator.validate_email_address(email)
            assert is_valid == True
    
    def test_validate_email_address_invalid(self):
        """Test invalid email addresses"""
        invalid_emails = [
            "invalid-email",
            "@domain.com",
            "user@",
            "user space@domain.com"
        ]
        
        for email in invalid_emails:
            is_valid, _ = EmailValidator.validate_email_address(email)
            assert is_valid == False
    
    def test_validate_email_config_valid(self):
        """Test valid email configuration"""
        result = EmailValidator.validate_email_config(
            "test@example.com", 
            "validpassword123"
        )
        assert result['valid'] == True
        assert len(result['errors']) == 0
    
    def test_validate_email_config_placeholder(self):
        """Test email config with placeholder values"""
        result = EmailValidator.validate_email_config(
            "your_gmail@gmail.com",
            "your_app_password"
        )
        assert result['valid'] == False
        assert len(result['errors']) > 0


class TestInputSanitizer:
    """Test input sanitization"""
    
    def test_sanitize_text_basic(self):
        """Test basic text sanitization"""
        text = "Normal text with some content"
        result = InputSanitizer.sanitize_text(text)
        assert result == text
    
    def test_sanitize_text_remove_scripts(self):
        """Test removal of script tags"""
        text = "Hello <script>alert('xss')</script> world"
        result = InputSanitizer.sanitize_text(text)
        assert "<script>" not in result
        assert "alert" not in result
    
    def test_sanitize_text_length_limit(self):
        """Test text length limiting"""
        long_text = "x" * 20000
        result = InputSanitizer.sanitize_text(long_text, max_length=1000)
        assert len(result) <= 1000
    
    def test_sanitize_filename_basic(self):
        """Test basic filename sanitization"""
        filename = "normal_file.pdf"
        result = InputSanitizer.sanitize_filename(filename)
        assert result == filename
    
    def test_sanitize_filename_dangerous_chars(self):
        """Test removal of dangerous characters from filename"""
        filename = "file<>:\"/\\|?*.pdf"
        result = InputSanitizer.sanitize_filename(filename)
        assert not any(char in result for char in '<>:"/\\|?*')


class TestConfigValidator:
    """Test configuration validation"""
    
    def test_validate_config_valid_gemini(self):
        """Test config validation with valid Gemini key"""
        config = {
            'gemini_api_key': 'AIzaSyDhZjKjKjKjKjKjKjKjKjKjKjKjKjKjKjK',
            'cookie_key': 'secure_cookie_key_123456'
        }
        
        result = ConfigValidator.validate_config(config)
        assert result['valid'] == True
        assert 'gemini' in result['ai_providers']
    
    def test_validate_config_no_ai_providers(self):
        """Test config validation with no AI providers"""
        config = {
            'cookie_key': 'secure_cookie_key_123456'
        }
        
        result = ConfigValidator.validate_config(config)
        assert result['valid'] == False
        assert len(result['ai_providers']) == 0
        assert any('No valid AI providers' in error for error in result['errors'])
    
    def test_validate_config_email_valid(self):
        """Test config validation with valid email"""
        config = {
            'gemini_api_key': 'AIzaSyDhZjKjKjKjKjKjKjKjKjKjKjKjKjKjKjK',
            'sender_email': 'test@example.com',
            'sender_password': 'validpassword123',
            'cookie_key': 'secure_cookie_key_123456'
        }
        
        result = ConfigValidator.validate_config(config)
        assert 'email_reports' in result['features_enabled']


# Integration tests
def test_validate_resume_upload_integration():
    """Test the convenience function for resume upload validation"""
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
        tmp.write(b'%PDF-1.4\nTest content')
        tmp_path = tmp.name
    
    try:
        result = validate_resume_upload(tmp_path)
        assert 'valid' in result
        assert 'errors' in result
        assert 'file_info' in result
    finally:
        os.unlink(tmp_path)


if __name__ == "__main__":
    pytest.main([__file__])