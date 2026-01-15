"""
Shipment Pydantic schemas for request/response validation.
"""
from pydantic import Field, field_validator, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID
from decimal import Decimal
import re

from app.schemas.base import BaseSchema, TimestampSchema, ResponseBase
from app.models.shipment import ServiceType, ShipmentStatus


class ShipmentBase(BaseSchema):
    """Base shipment schema."""
    origin_city: str = Field(..., min_length=2, max_length=100)
    origin_country: str = Field(..., min_length=2, max_length=100)
    origin_address: Optional[str] = Field(None, max_length=500)
    origin_postal_code: Optional[str] = Field(None, max_length=20)
    
    destination_city: str = Field(..., min_length=2, max_length=100)
    destination_country: str = Field(..., min_length=2, max_length=100)
    destination_address: Optional[str] = Field(None, max_length=500)
    destination_postal_code: Optional[str] = Field(None, max_length=20)
    
    service_type: ServiceType
    weight: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    dimensions: Optional[Dict[str, Any]] = None
    package_count: Decimal = Field(default=1, ge=1)
    
    special_instructions: Optional[str] = Field(None, max_length=1000)
    insurance: bool = False
    signature_required: bool = False
    
    @field_validator("origin_city", "origin_country", "destination_city", "destination_country")
    @classmethod
    def sanitize_location(cls, v: str) -> str:
        """Sanitize location fields."""
        sanitized = re.sub(r'[<>{}]', '', v)
        return sanitized.strip()
    
    @field_validator("dimensions")
    @classmethod
    def validate_dimensions(cls, v: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Validate dimensions format."""
        if v is None:
            return v
        
        required_keys = ["length", "width", "height"]
        if not all(key in v for key in required_keys):
            raise ValueError(f"Dimensions must include: {', '.join(required_keys)}")
        
        for key in required_keys:
            if not isinstance(v[key], (int, float)) or v[key] <= 0:
                raise ValueError(f"{key} must be a positive number")
        
        return v


class ShipmentCreate(ShipmentBase):
    """Schema for creating a new shipment."""
    estimated_delivery: Optional[datetime] = None


class ShipmentUpdate(BaseSchema):
    """Schema for updating shipment information."""
    status: Optional[ShipmentStatus] = None
    actual_cost: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    actual_delivery: Optional[datetime] = None
    special_instructions: Optional[str] = Field(None, max_length=1000)


class ShipmentResponse(ShipmentBase, ResponseBase, TimestampSchema):
    """Schema for shipment response."""
    tracking_number: str
    user_id: UUID
    status: ShipmentStatus
    estimated_cost: Optional[Decimal] = None
    actual_cost: Optional[Decimal] = None
    currency: str
    estimated_delivery: Optional[datetime] = None
    actual_delivery: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class ShipmentListResponse(BaseSchema):
    """Schema for paginated shipment list."""
    items: List[ShipmentResponse]
    total: int
    page: int
    page_size: int
    pages: int
