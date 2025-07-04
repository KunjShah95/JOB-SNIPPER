"""
JobSniper AI - Utility Helper Functions
======================================

Common utility functions used throughout the JobSniper AI platform.
Includes data processing, validation, formatting, and other helper utilities.
"""

import re
import hashlib
import secrets
import string
import json
import base64
import mimetypes
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union, Tuple
from pathlib import Path
import unicodedata
from urllib.parse import urlparse, urljoin
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def generate_id(length: int = 8) -> str:
    """Generate a random ID string"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_session_id() -> str:
    """Generate a unique session ID"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_part = generate_id(8)
    return f"{timestamp}_{random_part}"

def hash_string(text: str, algorithm: str = "sha256") -> str:
    """Hash a string using specified algorithm"""
    if algorithm == "md5":
        return hashlib.md5(text.encode()).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(text.encode()).hexdigest()
    elif algorithm == "sha256":
        return hashlib.sha256(text.encode()).hexdigest()
    else:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove control characters
    filename = ''.join(char for char in filename if ord(char) >= 32)
    
    # Normalize unicode
    filename = unicodedata.normalize('NFKD', filename)
    
    # Limit length
    if len(filename) > 255:
        name, ext = Path(filename).stem, Path(filename).suffix
        max_name_length = 255 - len(ext)
        filename = name[:max_name_length] + ext
    
    return filename

def validate_email(email: str) -> bool:
    """Validate email address format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    
    # Check if it's a valid length (7-15 digits)
    return 7 <= len(digits_only) <= 15

def validate_url(url: str) -> bool:
    """Validate URL format"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def extract_domain(url: str) -> Optional[str]:
    """Extract domain from URL"""
    try:
        parsed = urlparse(url)
        return parsed.netloc.lower()
    except Exception:
        return None

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format currency amount"""
    if currency == "USD":
        return f"${amount:,.2f}"
    elif currency == "EUR":
        return f"€{amount:,.2f}"
    elif currency == "GBP":
        return f"£{amount:,.2f}"
    else:
        return f"{amount:,.2f} {currency}"

def format_percentage(value: float, decimal_places: int = 1) -> str:
    """Format percentage value"""
    return f"{value:.{decimal_places}f}%"

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def format_duration(seconds: float) -> str:
    """Format duration in human readable format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove control characters
    text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text

def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """Extract keywords from text"""
    # Convert to lowercase and split into words
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    
    # Filter by minimum length and remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
        'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
        'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
    }
    
    keywords = [word for word in words 
                if len(word) >= min_length and word not in stop_words]
    
    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = []
    for keyword in keywords:
        if keyword not in seen:
            seen.add(keyword)
            unique_keywords.append(keyword)
    
    return unique_keywords

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate text similarity using Jaccard similarity"""
    words1 = set(extract_keywords(text1))
    words2 = set(extract_keywords(text2))
    
    if not words1 and not words2:
        return 1.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0

def encode_base64(data: Union[str, bytes]) -> str:
    """Encode data to base64 string"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    return base64.b64encode(data).decode('utf-8')

def decode_base64(encoded_data: str) -> bytes:
    """Decode base64 string to bytes"""
    return base64.b64decode(encoded_data)

def safe_json_loads(json_string: str, default: Any = None) -> Any:
    """Safely load JSON string with fallback"""
    try:
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError):
        return default

def safe_json_dumps(data: Any, default: Any = None) -> str:
    """Safely dump data to JSON string"""
    try:
        return json.dumps(data, default=str, ensure_ascii=False)
    except (TypeError, ValueError):
        return json.dumps(default) if default is not None else "{}"

def get_file_type(filename: str) -> Tuple[str, str]:
    """Get file type and MIME type from filename"""
    mime_type, _ = mimetypes.guess_type(filename)
    
    if mime_type:
        file_type = mime_type.split('/')[0]
    else:
        # Fallback based on extension
        ext = Path(filename).suffix.lower()
        if ext in ['.pdf']:
            file_type, mime_type = 'application', 'application/pdf'
        elif ext in ['.doc', '.docx']:
            file_type, mime_type = 'application', 'application/msword'
        elif ext in ['.txt']:
            file_type, mime_type = 'text', 'text/plain'
        elif ext in ['.jpg', '.jpeg', '.png', '.gif']:
            file_type, mime_type = 'image', f'image/{ext[1:]}'
        else:
            file_type, mime_type = 'unknown', 'application/octet-stream'
    
    return file_type, mime_type

def is_safe_file(filename: str, allowed_extensions: List[str]) -> bool:
    """Check if file is safe based on extension"""
    ext = Path(filename).suffix.lower().lstrip('.')
    return ext in [ext.lower() for ext in allowed_extensions]

def create_pagination(total_items: int, page: int, per_page: int) -> Dict[str, Any]:
    """Create pagination information"""
    total_pages = (total_items + per_page - 1) // per_page
    
    return {
        "total_items": total_items,
        "total_pages": total_pages,
        "current_page": page,
        "per_page": per_page,
        "has_prev": page > 1,
        "has_next": page < total_pages,
        "prev_page": page - 1 if page > 1 else None,
        "next_page": page + 1 if page < total_pages else None,
        "start_item": (page - 1) * per_page + 1,
        "end_item": min(page * per_page, total_items)
    }

def retry_with_backoff(func, max_retries: int = 3, base_delay: float = 1.0):
    """Retry function with exponential backoff"""
    import time
    
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            
            delay = base_delay * (2 ** attempt)
            time.sleep(delay)

def batch_process(items: List[Any], batch_size: int = 100):
    """Process items in batches"""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

def deep_merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge two dictionaries"""
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result

def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """Flatten nested dictionary"""
    items = []
    
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    
    return dict(items)

def get_nested_value(data: Dict[str, Any], key_path: str, default: Any = None) -> Any:
    """Get nested value from dictionary using dot notation"""
    keys = key_path.split('.')
    current = data
    
    try:
        for key in keys:
            current = current[key]
        return current
    except (KeyError, TypeError):
        return default

def set_nested_value(data: Dict[str, Any], key_path: str, value: Any) -> None:
    """Set nested value in dictionary using dot notation"""
    keys = key_path.split('.')
    current = data
    
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    
    current[keys[-1]] = value

# Export all utility functions
__all__ = [
    'generate_id', 'generate_session_id', 'hash_string', 'sanitize_filename',
    'validate_email', 'validate_phone', 'validate_url', 'extract_domain',
    'format_currency', 'format_percentage', 'format_file_size', 'format_duration',
    'truncate_text', 'clean_text', 'extract_keywords', 'calculate_similarity',
    'encode_base64', 'decode_base64', 'safe_json_loads', 'safe_json_dumps',
    'get_file_type', 'is_safe_file', 'create_pagination', 'retry_with_backoff',
    'batch_process', 'deep_merge_dicts', 'flatten_dict', 'get_nested_value',
    'set_nested_value'
]