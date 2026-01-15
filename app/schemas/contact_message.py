"""
Contact message Pydantic schemas.
"""
from pydantic import EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID
import re

from app.schemas.base import BaseSchema, ResponseBase
from app.models.contact_message import MessageStatus


class ContactMessageBase(BaseSchema):
    """Base contact message schema."""
    name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=50)
    subject: str = Field(..., min_length=5, max_length=500)
    message: str = Field(..., min_length=10, max_length=5000)
    
    @field_validator("name", "subject")
    @classmethod
    def sanitize_string(cls, v: str) -> str:
        """Sanitize string fields to prevent injection."""
        sanitized = re.sub(r'[<>{}]', '', v)
        return sanitized.strip()
    
    @field_validator("message")
    @classmethod
    def sanitize_message(cls, v: str) -> str:
        """Sanitize message content."""
        # Remove script tags and potentially dangerous content
        sanitized = re.sub(r'<script[^>]*>.*?</script>', '', v, flags=re.IGNORECASE | re.DOTALL)
        sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
        return sanitized.strip()
    
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Validate phone number."""
        if v is None:
            return v
        cleaned = re.sub(r'[^\d+\-\s()]', '', v)
        if len(cleaned) < 10:
            raise ValueError("Phone number must be at least 10 digits")
        return cleaned


class ContactMessageCreate(ContactMessageBase):
    """Schema for creating a contact message."""
    pass


class ContactMessageUpdate(BaseSchema):
    """Schema for updating contact message (admin only)."""
    status: Optional[MessageStatus] = None
    admin_notes: Optional[str] = Field(None, max_length=2000)


class ContactMessageResponse(ContactMessageBase, ResponseBase):
    """Schema for contact message response."""
    status: MessageStatus
    admin_notes: Optional[str] = None
    created_at: datetime
    read_at: Optional[datetime] = None
    responded_at: Optional[datetime] = None


class ContactMessageListResponse(BaseSchema):
    """Schema for paginated contact message list."""
    items: List[ContactMessageResponse]
    total: int
    page: int
    page_size: int
    pages: int
