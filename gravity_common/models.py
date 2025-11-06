"""
Common Pydantic models and schemas.

These base models ensure consistency across all microservices
while keeping each service completely independent.
"""

from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel as PydanticBaseModel, Field, ConfigDict


class BaseModel(PydanticBaseModel):
    """
    Base Pydantic model with common configuration.
    
    All microservices can use this as a foundation for their models.
    """
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=True,
    )


class TimestampMixin(BaseModel):
    """Mixin for models with timestamp fields."""
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


class IDMixin(BaseModel):
    """Mixin for models with ID field."""
    
    id: int = Field(..., description="Unique identifier")


T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    """
    Generic API response wrapper.
    
    Ensures consistent response format across all microservices.
    
    Example:
        ApiResponse[UserSchema](
            success=True,
            data=user,
            message="User retrieved successfully"
        )
    """
    
    success: bool = Field(default=True, description="Request success status")
    data: Optional[T] = Field(default=None, description="Response data")
    message: str = Field(default="", description="Response message")
    errors: Optional[List[str]] = Field(default=None, description="Error messages")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Generic paginated response.
    
    Use this for list endpoints that support pagination.
    """
    
    items: List[T] = Field(default_factory=list, description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there's a next page")
    has_previous: bool = Field(..., description="Whether there's a previous page")


class PaginationParams(BaseModel):
    """Common pagination parameters."""
    
    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=10, ge=1, le=100, description="Items per page")
    
    @property
    def offset(self) -> int:
        """Calculate offset for database queries."""
        return (self.page - 1) * self.page_size


class HealthCheckResponse(BaseModel):
    """Standard health check response."""
    
    status: str = Field(..., description="Service status (healthy/unhealthy)")
    service_name: str = Field(..., description="Name of the service")
    version: str = Field(..., description="Service version")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    dependencies: Optional[Dict[str, str]] = Field(default=None, description="Status of dependencies")


class ErrorResponse(BaseModel):
    """Standard error response."""
    
    success: bool = Field(default=False)
    error: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(default=None, description="Error code")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
