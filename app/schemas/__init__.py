"""
Schemas package - exports all Pydantic schemas.
"""
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    Token,
    TokenPayload,
)
from app.schemas.shipment import (
    ShipmentCreate,
    ShipmentUpdate,
    ShipmentResponse,
    ShipmentListResponse,
)
from app.schemas.shipment_event import (
    ShipmentEventCreate,
    ShipmentEventResponse,
    ShipmentTimelineResponse,
)
from app.schemas.quote import (
    QuoteCreate,
    QuoteUpdate,
    QuoteResponse,
    QuoteListResponse,
)
from app.schemas.contact_message import (
    ContactMessageCreate,
    ContactMessageUpdate,
    ContactMessageResponse,
    ContactMessageListResponse,
)
from app.schemas.dashboard import (
    DashboardStats,
    DashboardResponse,
)

__all__ = [
    # User schemas
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "Token",
    "TokenPayload",
    # Shipment schemas
    "ShipmentCreate",
    "ShipmentUpdate",
    "ShipmentResponse",
    "ShipmentListResponse",
    # Shipment event schemas
    "ShipmentEventCreate",
    "ShipmentEventResponse",
    "ShipmentTimelineResponse",
    # Quote schemas
    "QuoteCreate",
    "QuoteUpdate",
    "QuoteResponse",
    "QuoteListResponse",
    # Contact message schemas
    "ContactMessageCreate",
    "ContactMessageUpdate",
    "ContactMessageResponse",
    "ContactMessageListResponse",
    # Dashboard schemas
    "DashboardStats",
    "DashboardResponse",
]
