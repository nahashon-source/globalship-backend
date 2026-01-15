"""
Quote CRUD service with SQL injection protection.
"""
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from uuid import UUID
from datetime import datetime, timedelta
import logging

from app.models.quote import Quote, QuoteStatus
from app.schemas.quote import QuoteCreate, QuoteUpdate

logger = logging.getLogger(__name__)


class QuoteService:
    """Quote CRUD operations."""
    
    @staticmethod
    def get_by_id(db: Session, quote_id: UUID) -> Optional[Quote]:
        """
        Get quote by ID.
        SQLAlchemy ORM prevents SQL injection.
        """
        return db.query(Quote).filter(Quote.id == quote_id).first()
    
    @staticmethod
    def get_user_quotes(
        db: Session,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        status: Optional[QuoteStatus] = None
    ) -> Tuple[List[Quote], int]:
        """
        Get user's quotes with pagination.
        SQLAlchemy ORM prevents SQL injection.
        """
        query = db.query(Quote).filter(Quote.user_id == user_id)
        
        if status:
            query = query.filter(Quote.status == status)
        
        total = query.count()
        quotes = query.order_by(desc(Quote.created_at)).offset(skip).limit(limit).all()
        
        return quotes, total
    
    @staticmethod
    def create(
        db: Session,
        user_id: UUID,
        quote_in: QuoteCreate
    ) -> Quote:
        """
        Create new quote.
        SQLAlchemy ORM prevents SQL injection.
        """
        # Set expiration date (7 days from now)
        expires_at = datetime.utcnow() + timedelta(days=7)
        
        db_quote = Quote(
            user_id=user_id,
            expires_at=expires_at,
            **quote_in.model_dump()
        )
        
        db.add(db_quote)
        db.commit()
        db.refresh(db_quote)
        
        logger.info(f"Quote created for user: {user_id}")
        return db_quote
    
    @staticmethod
    def update(
        db: Session,
        quote_id: UUID,
        quote_in: QuoteUpdate
    ) -> Optional[Quote]:
        """
        Update quote.
        SQLAlchemy ORM prevents SQL injection.
        """
        quote = QuoteService.get_by_id(db, quote_id)
        if not quote:
            return None
        
        # Update fields
        update_data = quote_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(quote, field, value)
        
        db.commit()
        db.refresh(quote)
        
        logger.info(f"Quote updated: {quote_id}")
        return quote
    
    @staticmethod
    def get_pending_count(db: Session, user_id: UUID) -> int:
        """
        Get count of pending quotes for user.
        SQLAlchemy ORM prevents SQL injection.
        """
        return db.query(func.count(Quote.id)).filter(
            Quote.user_id == user_id,
            Quote.status == QuoteStatus.PENDING
        ).scalar() or 0


# Global quote service instance
quote_service = QuoteService()
