"""
Contact message CRUD service with SQL injection protection.
"""
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc
from uuid import UUID
from datetime import datetime
import logging

from app.models.contact_message import ContactMessage, MessageStatus
from app.schemas.contact_message import ContactMessageCreate, ContactMessageUpdate

logger = logging.getLogger(__name__)


class ContactMessageService:
    """Contact message CRUD operations."""
    
    @staticmethod
    def get_by_id(db: Session, message_id: UUID) -> Optional[ContactMessage]:
        """
        Get contact message by ID.
        SQLAlchemy ORM prevents SQL injection.
        """
        return db.query(ContactMessage).filter(
            ContactMessage.id == message_id
        ).first()
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[MessageStatus] = None
    ) -> Tuple[List[ContactMessage], int]:
        """
        Get all contact messages with pagination.
        SQLAlchemy ORM prevents SQL injection.
        """
        query = db.query(ContactMessage)
        
        if status:
            query = query.filter(ContactMessage.status == status)
        
        total = query.count()
        messages = query.order_by(desc(ContactMessage.created_at)).offset(skip).limit(limit).all()
        
        return messages, total
    
    @staticmethod
    def create(
        db: Session,
        message_in: ContactMessageCreate
    ) -> ContactMessage:
        """
        Create new contact message.
        SQLAlchemy ORM prevents SQL injection.
        """
        db_message = ContactMessage(**message_in.model_dump())
        
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        
        logger.info(f"Contact message created from: {message_in.email}")
        return db_message
    
    @staticmethod
    def update(
        db: Session,
        message_id: UUID,
        message_in: ContactMessageUpdate
    ) -> Optional[ContactMessage]:
        """
        Update contact message.
        SQLAlchemy ORM prevents SQL injection.
        """
        message = ContactMessageService.get_by_id(db, message_id)
        if not message:
            return None
        
        # Update fields
        update_data = message_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(message, field, value)
        
        # Mark as read if status is being updated
        if message_in.status and message.status == MessageStatus.NEW:
            message.read_at = datetime.utcnow()
        
        db.commit()
        db.refresh(message)
        
        logger.info(f"Contact message updated: {message_id}")
        return message


# Global contact message service instance
contact_message_service = ContactMessageService()
