"""
Quote model for shipment quote requests.
"""
import uuid
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base import Base


class QuoteStatus(str, enum.Enum):
    """Quote status enumeration."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class Quote(Base):
    """Quote database model."""
    
    __tablename__ = "quotes"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign key to user
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Quote information
    origin = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    service_type = Column(String(50), nullable=False)
    
    # Package details
    weight = Column(Numeric(10, 2), nullable=True)
    dimensions = Column(String(255), nullable=True)
    package_count = Column(Numeric(10, 0), default=1, nullable=False)
    
    # Pricing
    estimated_cost = Column(Numeric(10, 2), nullable=True)
    currency = Column(String(3), default="USD", nullable=False)
    
    # Status
    status = Column(Enum(QuoteStatus), default=QuoteStatus.PENDING, nullable=False, index=True)
    
    # Additional information
    special_requirements = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="quotes")
    
    def __repr__(self):
        return f"<Quote {self.id} - {self.status}>"
