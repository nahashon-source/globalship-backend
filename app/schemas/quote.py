"""
Quote Pydantic schemas for request/response validation.
"""
from pydantic import Field, field_validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from decimal import Decimal
import re

from app.schemas.base import BaseSchema, TimestampSchema, ResponseBase
from app.models.quote import QuoteStatus


class QuoteBase(BaseSchema):
    """Base quote schema."""
    origin: str = Field(..., min_length=2, max_length=255)
    destination: str = Field(..., min_length=2, max_length=255)
    service_type: str = Field(..., min_length=2, max_length=50)
    weight: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    dimensions: Optional[str] = Field(None, max_length=255)
    package_count: Decimal = Field(default=1, ge=1)
    special_requirements: Optional[str] = Field(None, max_length=2000)
    
    @field_validator("origin", "destination", "service_type")
    @classmethod
    def sanitize_string(cls, v: str) -> str:
        """Sanitize string fields."""
        sanitized = re.sub(r'[<>{}]', '', v)
        return sanitized.strip()


class QuoteCreate(QuoteBase):
    """Schema for creating a quote request."""
    pass


class QuoteUpdate(BaseSchema):
    """Schema for updating quote (admin only)."""
    estimated_cost: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    status: Optional[QuoteStatus] = None
    notes: Optional[str] = Field(None, max_length=2000)


class QuoteResponse(QuoteBase, ResponseBase, TimestampSchema):
    """Schema for quote response."""
    user_id: UUID
    estimated_cost: Optional[Decimal] = None
    currency: str
    status: QuoteStatus
    notes: Optional[str] = None
    expires_at: Optional[datetime] = None


class QuoteListResponse(BaseSchema):
    """Schema for paginated quote list."""
    items: List[QuoteResponse]
    total: int
    page: int
    page_size: int
    pages: int
