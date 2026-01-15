"""
Shipment model for tracking shipments.
All queries use SQLAlchemy ORM for SQL injection protection.
"""
import uuid
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Numeric, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base import Base


class ServiceType(str, enum.Enum):
    """Service type enumeration."""
    AIR = "air"
    SEA = "sea"
    ROAD = "road"
    WAREHOUSING = "warehousing"
    CUSTOMS = "customs"


class ShipmentStatus(str, enum.Enum):
    """Shipment status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    CUSTOMS = "customs"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    ON_HOLD = "on_hold"


class Shipment(Base):
    """Shipment database model."""
    
    __tablename__ = "shipments"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Tracking information
    tracking_number = Column(String(50), unique=True, index=True, nullable=False)
    
    # Foreign key to user
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Origin information
    origin_city = Column(String(100), nullable=False)
    origin_country = Column(String(100), nullable=False)
    origin_address = Column(String(500), nullable=True)
    origin_postal_code = Column(String(20), nullable=True)
    
    # Destination information
    destination_city = Column(String(100), nullable=False)
    destination_country = Column(String(100), nullable=False)
    destination_address = Column(String(500), nullable=True)
    destination_postal_code = Column(String(20), nullable=True)
    
    # Shipment details
    service_type = Column(Enum(ServiceType), nullable=False, default=ServiceType.AIR)
    status = Column(Enum(ShipmentStatus), nullable=False, default=ShipmentStatus.PENDING, index=True)
    
    # Package information
    weight = Column(Numeric(10, 2), nullable=True)  # in kg
    dimensions = Column(JSON, nullable=True)  # {"length": 10, "width": 20, "height": 30}
    package_count = Column(Numeric(10, 0), default=1, nullable=False)
    
    # Pricing
    estimated_cost = Column(Numeric(10, 2), nullable=True)
    actual_cost = Column(Numeric(10, 2), nullable=True)
    currency = Column(String(3), default="USD", nullable=False)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    estimated_delivery = Column(DateTime, nullable=True)
    actual_delivery = Column(DateTime, nullable=True)
    
    # Additional information
    special_instructions = Column(String(1000), nullable=True)
    insurance = Column(Boolean, default=False, nullable=False)
    signature_required = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="shipments")
    events = relationship("ShipmentEvent", back_populates="shipment", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Shipment {self.tracking_number}>"
