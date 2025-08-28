"""
Advanced Security Module for JobSniper AI
Handles authentication, authorization, data encryption, and security monitoring
"""

import hashlib
import secrets
import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import logging
from cryptography.fernet import Fernet
from functools import wraps
import streamlit as st
import re
import time

logger = logging.getLogger("Security")

class SecurityManager:
    def __init__(self):
        self.secret_key = self._get_or_create_secret_key()
        self.cipher_suite = Fernet(self._get_or_create_encryption_key())
        self.failed_attempts = {}  # Track failed login attempts
        self.active_sessions = {}  # Track active user sessions
        
    def _get_or_create_secret_key(self) -> str:
        """Get or create JWT secret key"""
        import os
        key = os.getenv("JWT_SECRET_KEY")
        if not key:
            key = secrets.token_urlsafe(32)
            logger.warning("JWT_SECRET_KEY not found in environment, using generated key")
        return key
    
    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key"""
        import os
        key = os.getenv("ENCRYPTION_KEY")
        if not key:
            key = Fernet.generate_key()
            logger.warning("ENCRYPTION_KEY not found in environment, using generated key")
        else:
            key = key.encode()
        return key
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def generate_token(self, user_data: Dict[str, Any], expires_hours: int = 24) -> str:
        """Generate JWT token"""
        payload = {
            'user_id': user_data.get('user_id'),
            'email': user_data.get('email'),
            'role': user_data.get('role', 'user'),
            'exp': datetime.utcnow() + timedelta(hours=expires_hours),
            'iat': datetime.utcnow(),
            'jti': secrets.token_urlsafe(16)  # JWT ID for token revocation
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        
        # Store active session
        self.active_sessions[payload['jti']] = {
            'user_id': payload['user_id'],
            'created_at': datetime.utcnow(),
            'expires_at': payload['exp']
        }
        
        return token
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            
            # Check if session is still active
            jti = payload.get('jti')
            if jti not in self.active_sessions:
                logger.warning(f"Token with JTI {jti} not found in active sessions")
                return None
            
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None
    
    def revoke_token(self, token: str) -> bool:
        """Revoke a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            jti = payload.get('jti')
            
            if jti in self.active_sessions:
                del self.active_sessions[jti]
                logger.info(f"Token {jti} revoked successfully")
                return True
            
            return False
            
        except jwt.InvalidTokenError:
            return False
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        return encrypted_data.decode()
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        decrypted_data = self.cipher_suite.decrypt(encrypted_data.encode())
        return decrypted_data.decode()
    
    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """Validate password strength"""
        issues = []
        score = 0
        
        if len(password) >= 8:
            score += 1
        else:
            issues.append("Password must be at least 8 characters long")
        
        if re.search(r'[A-Z]', password):
            score += 1
        else:
            issues.append("Password must contain at least one uppercase letter")
        
        if re.search(r'[a-z]', password):
            score += 1
        else:
            issues.append("Password must contain at least one lowercase letter")
        
        if re.search(r'\d', password):
            score += 1
        else:
            issues.append("Password must contain at least one number")
        
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
        else:
            issues.append("Password must contain at least one special character")
        
        strength_levels = {
            0: "Very Weak",
            1: "Weak", 
            2: "Fair",
            3: "Good",
            4: "Strong",
            5: "Very Strong"
        }
        
        return {
            "score": score,
            "strength": strength_levels[score],
            "is_valid": score >= 3,
            "issues": issues
        }
    
    def check_rate_limit(self, identifier: str, max_attempts: int = 5, window_minutes: int = 15) -> bool:
        """Check if identifier is rate limited"""
        current_time = time.time()
        window_start = current_time - (window_minutes * 60)
        
        if identifier not in self.failed_attempts:
            self.failed_attempts[identifier] = []
        
        # Remove old attempts outside the window
        self.failed_attempts[identifier] = [
            attempt_time for attempt_time in self.failed_attempts[identifier]
            if attempt_time > window_start
        ]
        
        # Check if rate limit exceeded
        return len(self.failed_attempts[identifier]) < max_attempts
    
    def record_failed_attempt(self, identifier: str):
        """Record a failed authentication attempt"""
        current_time = time.time()
        
        if identifier not in self.failed_attempts:
            self.failed_attempts[identifier] = []
        
        self.failed_attempts[identifier].append(current_time)
        logger.warning(f"Failed authentication attempt recorded for {identifier}")
    
    def sanitize_input(self, input_text: str) -> str:
        """Sanitize user input to prevent injection attacks"""
        if not isinstance(input_text, str):
            return str(input_text)
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', input_text)
        
        # Limit length
        sanitized = sanitized[:1000]
        
        return sanitized.strip()
    
    def validate_file_upload(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Validate uploaded file for security"""
        validation_result = {
            "is_safe": True,
            "issues": [],
            "file_info": {}
        }
        
        # Check file size (max 10MB)
        max_size = 10 * 1024 * 1024
        if len(file_content) > max_size:
            validation_result["is_safe"] = False
            validation_result["issues"].append(f"File too large: {len(file_content)} bytes (max: {max_size})")
        
        # Check file extension
        allowed_extensions = ['.pdf', '.docx', '.txt', '.doc']
        file_ext = '.' + filename.split('.')[-1].lower() if '.' in filename else ''
        
        if file_ext not in allowed_extensions:
            validation_result["is_safe"] = False
            validation_result["issues"].append(f"File type not allowed: {file_ext}")
        
        # Check for suspicious content patterns
        content_str = str(file_content)
        suspicious_patterns = [
            r'<script',
            r'javascript:',
            r'vbscript:',
            r'onload=',
            r'onerror=',
            r'eval\(',
            r'exec\('
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, content_str, re.IGNORECASE):
                validation_result["is_safe"] = False
                validation_result["issues"].append(f"Suspicious content detected: {pattern}")
        
        validation_result["file_info"] = {
            "filename": filename,
            "size": len(file_content),
            "extension": file_ext
        }
        
        return validation_result
    
    def generate_api_key(self, user_id: str, permissions: List[str] = None) -> str:
        """Generate API key for external access"""
        key_data = {
            "user_id": user_id,
            "permissions": permissions or ["read"],
            "created_at": datetime.utcnow().isoformat(),
            "key_id": secrets.token_urlsafe(8)
        }
        
        # Create API key with prefix
        api_key = f"js_{''.join(secrets.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(32))}"
        
        # Store key data (in production, store in database)
        # For now, just log it
        logger.info(f"API key generated for user {user_id}: {key_data['key_id']}")
        
        return api_key
    
    def audit_log(self, user_id: str, action: str, resource: str, details: Dict[str, Any] = None):
        """Log security-relevant actions"""
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "details": details or {},
            "ip_address": self._get_client_ip(),
            "user_agent": self._get_user_agent()
        }
        
        # In production, store in secure audit log database
        logger.info(f"AUDIT: {audit_entry}")
    
    def _get_client_ip(self) -> str:
        """Get client IP address"""
        # In Streamlit, this would need to be implemented differently
        return "127.0.0.1"  # Placeholder
    
    def _get_user_agent(self) -> str:
        """Get client user agent"""
        return "Unknown"  # Placeholder

# Global security manager instance
security_manager = SecurityManager()

# Decorators for authentication and authorization
def require_auth(func):
    """Decorator to require authentication"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "authenticated" not in st.session_state or not st.session_state.authenticated:
            st.error("🔒 Authentication required")
            st.stop()
        return func(*args, **kwargs)
    return wrapper

def require_role(required_role: str):
    """Decorator to require specific role"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_role = st.session_state.get("user_role", "guest")
            if user_role != required_role and user_role != "admin":
                st.error(f"🚫 Access denied. Required role: {required_role}")
                st.stop()
            return func(*args, **kwargs)
        return wrapper
    return decorator

def rate_limit(max_attempts: int = 10, window_minutes: int = 5):
    """Decorator for rate limiting"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = st.session_state.get("user_id", "anonymous")
            
            if not security_manager.check_rate_limit(user_id, max_attempts, window_minutes):
                st.error(f"🚫 Rate limit exceeded. Try again in {window_minutes} minutes.")
                st.stop()
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Streamlit authentication components
def render_login_form():
    """Render login form with security features"""
    st.markdown("### 🔐 Secure Login")
    
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="your.email@example.com")
        password = st.text_input("Password", type="password")
        remember_me = st.checkbox("Remember me")
        
        submitted = st.form_submit_button("Login", type="primary")
        
        if submitted:
            # Sanitize inputs
            email = security_manager.sanitize_input(email)
            
            # Check rate limiting
            if not security_manager.check_rate_limit(email):
                st.error("🚫 Too many failed attempts. Please try again later.")
                return
            
            # Validate credentials (mock implementation)
            if authenticate_user(email, password):
                # Generate session token
                user_data = {"user_id": email, "email": email, "role": "user"}
                token = security_manager.generate_token(user_data)
                
                # Store in session
                st.session_state.authenticated = True
                st.session_state.user_id = email
                st.session_state.user_role = "user"
                st.session_state.auth_token = token
                
                # Audit log
                security_manager.audit_log(email, "login", "system", {"success": True})
                
                st.success("✅ Login successful!")
                st.rerun()
            else:
                # Record failed attempt
                security_manager.record_failed_attempt(email)
                security_manager.audit_log(email, "login", "system", {"success": False})
                
                st.error("❌ Invalid credentials")

def authenticate_user(email: str, password: str) -> bool:
    """Authenticate user credentials (mock implementation)"""
    # In production, check against secure database
    # For demo, accept any email with password "password123"
    return password == "password123"

def render_password_strength_meter(password: str):
    """Render password strength meter"""
    if password:
        strength_info = security_manager.validate_password_strength(password)
        
        # Color coding
        colors = {
            "Very Weak": "red",
            "Weak": "orange", 
            "Fair": "yellow",
            "Good": "lightgreen",
            "Strong": "green",
            "Very Strong": "darkgreen"
        }
        
        color = colors.get(strength_info["strength"], "gray")
        
        st.markdown(f"""
        <div style="margin: 10px 0;">
            <div style="background: {color}; height: 10px; width: {strength_info['score'] * 20}%; border-radius: 5px;"></div>
            <small>Password Strength: <strong>{strength_info['strength']}</strong></small>
        </div>
        """, unsafe_allow_html=True)
        
        if strength_info["issues"]:
            with st.expander("Password Requirements"):
                for issue in strength_info["issues"]:
                    st.write(f"• {issue}")

# Security monitoring functions
def get_security_metrics() -> Dict[str, Any]:
    """Get security metrics for dashboard"""
    return {
        "active_sessions": len(security_manager.active_sessions),
        "failed_attempts_24h": sum(
            len([attempt for attempt in attempts if time.time() - attempt < 86400])
            for attempts in security_manager.failed_attempts.values()
        ),
        "rate_limited_ips": len([
            ip for ip, attempts in security_manager.failed_attempts.items()
            if len(attempts) >= 5
        ])
    }
