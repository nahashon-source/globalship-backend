"""
Dashboard Pydantic schemas for statistics and overview.
"""
from pydantic import Field
from typing import List
from decimal import Decimal

from app.schemas.base import BaseSchema
from app.schemas.shipment import ShipmentResponse


class DashboardStats(BaseSchema):
    """Schema for dashboard statistics."""
    active_shipments: int = Field(default=0, ge=0)
    delivered_shipments: int = Field(default=0, ge=0)
    total_spent: Decimal = Field(default=0, ge=0, decimal_places=2)
    pending_quotes: int = Field(default=0, ge=0)


class DashboardResponse(BaseSchema):
    """Schema for complete dashboard data."""
    stats: DashboardStats
    recent_shipments: List[ShipmentResponse]
