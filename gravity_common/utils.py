"""
Common utility functions used across microservices.
"""

import hashlib
import secrets
import string
from typing import Any, Dict, Optional
from datetime import datetime, timezone


def generate_random_string(length: int = 32) -> str:
    """
    Generate a random string.
    
    Args:
        length: Length of the string
        
    Returns:
        Random string
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_hash(data: str, algorithm: str = "sha256") -> str:
    """
    Generate hash of a string.
    
    Args:
        data: Data to hash
        algorithm: Hash algorithm (sha256, sha512, md5)
        
    Returns:
        Hexadecimal hash string
    """
    hasher = hashlib.new(algorithm)
    hasher.update(data.encode('utf-8'))
    return hasher.hexdigest()


def utc_now() -> datetime:
    """
    Get current UTC datetime.
    
    Returns:
        Current UTC datetime
    """
    return datetime.now(timezone.utc)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to remove dangerous characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove path separators and other dangerous chars
    dangerous_chars = ['/', '\\', '..', '\0']
    sanitized = filename
    
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '_')
    
    return sanitized


def dict_to_query_string(params: Dict[str, Any]) -> str:
    """
    Convert dictionary to URL query string.
    
    Args:
        params: Dictionary of parameters
        
    Returns:
        Query string
    """
    return '&'.join([f"{k}={v}" for k, v in params.items() if v is not None])


def mask_sensitive_data(data: str, visible_chars: int = 4) -> str:
    """
    Mask sensitive data for logging.
    
    Args:
        data: Sensitive string to mask
        visible_chars: Number of characters to keep visible
        
    Returns:
        Masked string
    """
    if len(data) <= visible_chars:
        return '*' * len(data)
    
    return data[:visible_chars] + '*' * (len(data) - visible_chars)


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string (e.g., "1.5 MB")
    """
    size: float = float(size_bytes)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"
