"""
User Pydantic schemas for request/response validation.
Input sanitization prevents SQL injection and XSS attacks.
"""
from pydantic import EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID
import re

from app.schemas.base import BaseSchema, TimestampSchema, ResponseBase


class UserBase(BaseSchema):
    """Base user schema with common fields."""
    email: EmailStr
    company_name: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=50)
    full_name: Optional[str] = Field(None, max_length=255)
    
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Validate phone number format."""
        if v is None:
            return v
        # Remove non-numeric characters except + and -
        cleaned = re.sub(r'[^\d+\-\s()]', '', v)
        if len(cleaned) < 10:
            raise ValueError("Phone number must be at least 10 digits")
        return cleaned
    
    @field_validator("company_name", "full_name")
    @classmethod
    def sanitize_string(cls, v: Optional[str]) -> Optional[str]:
        """Sanitize string inputs to prevent injection."""
        if v is None:
            return v
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>{}]', '', v)
        return sanitized.strip()


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=6, max_length=100)
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isalpha() for char in v):
            raise ValueError("Password must contain at least one letter")
        return v


class UserUpdate(BaseSchema):
    """Schema for updating user information."""
    company_name: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=50)
    full_name: Optional[str] = Field(None, max_length=255)
    
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Validate phone number format."""
        if v is None:
            return v
        cleaned = re.sub(r'[^\d+\-\s()]', '', v)
        if len(cleaned) < 10:
            raise ValueError("Phone number must be at least 10 digits")
        return cleaned


class UserResponse(UserBase, ResponseBase, TimestampSchema):
    """Schema for user response."""
    is_active: bool
    is_verified: bool
    last_login: Optional[datetime] = None


class UserLogin(BaseSchema):
    """Schema for user login."""
    email: EmailStr
    password: str = Field(..., min_length=6)


class Token(BaseSchema):
    """Schema for authentication token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseSchema):
    """Schema for JWT token payload."""
    sub: UUID
    exp: int
    type: str
