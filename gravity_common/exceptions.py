"""
Custom exceptions for Gravity microservices.

All services can use these standardized exceptions for consistent error handling.
Each exception is completely independent and doesn't require other services.
"""

from typing import Any, Dict, Optional


class GravityException(Exception):
    """Base exception for all Gravity microservices."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class NotFoundException(GravityException):
    """Exception raised when a resource is not found."""

    def __init__(self, message: str = "Resource not found", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=404, details=details)


class BadRequestException(GravityException):
    """Exception raised for invalid requests."""

    def __init__(self, message: str = "Bad request", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=400, details=details)


class UnauthorizedException(GravityException):
    """Exception raised when authentication fails."""

    def __init__(self, message: str = "Unauthorized", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=401, details=details)


class ForbiddenException(GravityException):
    """Exception raised when user doesn't have permission."""

    def __init__(self, message: str = "Forbidden", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=403, details=details)


class ConflictException(GravityException):
    """Exception raised when there's a conflict (e.g., duplicate resource)."""

    def __init__(self, message: str = "Conflict", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=409, details=details)


class ValidationException(GravityException):
    """Exception raised when validation fails."""

    def __init__(self, message: str = "Validation error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=422, details=details)


class ServiceUnavailableException(GravityException):
    """Exception raised when a service is unavailable."""

    def __init__(self, message: str = "Service unavailable", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=503, details=details)


class DatabaseException(GravityException):
    """Exception raised for database errors."""

    def __init__(self, message: str = "Database error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=500, details=details)


class ExternalServiceException(GravityException):
    """Exception raised when external service call fails."""

    def __init__(self, message: str = "External service error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=502, details=details)
