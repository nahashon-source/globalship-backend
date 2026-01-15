"""
Shipment event Pydantic schemas.
"""
from pydantic import Field, field_validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID
import re

from app.schemas.base import BaseSchema, ResponseBase


class ShipmentEventBase(BaseSchema):
    """Base shipment event schema."""
    event_type: str = Field(..., min_length=2, max_length=100)
    location: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    timestamp: datetime
    
    @field_validator("event_type", "location")
    @classmethod
    def sanitize_string(cls, v: Optional[str]) -> Optional[str]:
        """Sanitize string fields."""
        if v is None:
            return v
        sanitized = re.sub(r'[<>{}]', '', v)
        return sanitized.strip()


class ShipmentEventCreate(ShipmentEventBase):
    """Schema for creating a shipment event."""
    shipment_id: UUID


class ShipmentEventResponse(ShipmentEventBase, ResponseBase):
    """Schema for shipment event response."""
    shipment_id: UUID
    created_at: datetime


class ShipmentTimelineResponse(BaseSchema):
    """Schema for complete shipment timeline."""
    tracking_number: str
    events: List[ShipmentEventResponse]
