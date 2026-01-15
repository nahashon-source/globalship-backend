"""
Contact message model for contact form submissions.
"""
import uuid
from sqlalchemy import Column, String, DateTime, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import enum

from app.db.base import Base


class MessageStatus(str, enum.Enum):
    """Message status enumeration."""
    NEW = "new"
    READ = "read"
    RESPONDED = "responded"
    ARCHIVED = "archived"


class ContactMessage(Base):
    """Contact message database model."""
    
    __tablename__ = "contact_messages"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Contact information
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(50), nullable=True)
    
    # Message content
    subject = Column(String(500), nullable=False)
    message = Column(Text, nullable=False)
    
    # Status
    status = Column(Enum(MessageStatus), default=MessageStatus.NEW, nullable=False, index=True)
    
    # Admin notes
    admin_notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    read_at = Column(DateTime, nullable=True)
    responded_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<ContactMessage from {self.email}>"
