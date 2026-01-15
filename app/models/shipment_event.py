"""
Shipment event/timeline model for tracking shipment history.
"""
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class ShipmentEvent(Base):
    """Shipment event/timeline database model."""
    
    __tablename__ = "shipment_events"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign key to shipment
    shipment_id = Column(UUID(as_uuid=True), ForeignKey("shipments.id"), nullable=False, index=True)
    
    # Event information
    event_type = Column(String(100), nullable=False)  # e.g., "picked_up", "in_transit", "delivered"
    location = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    
    # Timestamps
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    shipment = relationship("Shipment", back_populates="events")
    
    def __repr__(self):
        return f"<ShipmentEvent {self.event_type} at {self.timestamp}>"
