"""
Shipment CRUD service with SQL injection protection via SQLAlchemy ORM.
"""
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, func
from uuid import UUID
from datetime import datetime
import secrets
import logging

from app.models.shipment import Shipment, ShipmentStatus
from app.schemas.shipment import ShipmentCreate, ShipmentUpdate
from app.services.redis_service import redis_service

logger = logging.getLogger(__name__)


class ShipmentService:
    """Shipment CRUD operations."""
    
    @staticmethod
    def generate_tracking_number() -> str:
        """Generate unique tracking number."""
        prefix = "GS"
        random_part = secrets.token_hex(6).upper()
        return f"{prefix}{random_part}"
    
    @staticmethod
    def get_by_id(db: Session, shipment_id: UUID) -> Optional[Shipment]:
        """
        Get shipment by ID.
        SQLAlchemy ORM prevents SQL injection.
        """
        cache_key = f"shipment:{shipment_id}"
        cached = redis_service.get(cache_key)
        if cached:
            return Shipment(**cached)
        
        shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
        
        if shipment:
            redis_service.set(cache_key, shipment.__dict__, expire=300)
        
        return shipment
    
    @staticmethod
    def get_by_tracking_number(
        db: Session,
        tracking_number: str
    ) -> Optional[Shipment]:
        """
        Get shipment by tracking number.
        SQLAlchemy ORM prevents SQL injection.
        """
        return db.query(Shipment).filter(
            Shipment.tracking_number == tracking_number
        ).first()
    
    @staticmethod
    def get_user_shipments(
        db: Session,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        status: Optional[ShipmentStatus] = None
    ) -> Tuple[List[Shipment], int]:
        """
        Get user's shipments with pagination.
        SQLAlchemy ORM prevents SQL injection.
        """
        query = db.query(Shipment).filter(Shipment.user_id == user_id)
        
        if status:
            query = query.filter(Shipment.status == status)
        
        total = query.count()
        shipments = query.order_by(desc(Shipment.created_at)).offset(skip).limit(limit).all()
        
        return shipments, total
    
    @staticmethod
    def create(
        db: Session,
        user_id: UUID,
        shipment_in: ShipmentCreate
    ) -> Shipment:
        """
        Create new shipment.
        SQLAlchemy ORM prevents SQL injection.
        """
        # Generate unique tracking number
        tracking_number = ShipmentService.generate_tracking_number()
        while ShipmentService.get_by_tracking_number(db, tracking_number):
            tracking_number = ShipmentService.generate_tracking_number()
        
        # Create shipment object
        db_shipment = Shipment(
            tracking_number=tracking_number,
            user_id=user_id,
            **shipment_in.model_dump()
        )
        
        db.add(db_shipment)
        db.commit()
        db.refresh(db_shipment)
        
        logger.info(f"Shipment created: {tracking_number}")
        return db_shipment
    
    @staticmethod
    def update(
        db: Session,
        shipment_id: UUID,
        shipment_in: ShipmentUpdate
    ) -> Optional[Shipment]:
        """
        Update shipment.
        SQLAlchemy ORM prevents SQL injection.
        """
        shipment = ShipmentService.get_by_id(db, shipment_id)
        if not shipment:
            return None
        
        # Update fields
        update_data = shipment_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(shipment, field, value)
        
        db.commit()
        db.refresh(shipment)
        
        # Invalidate cache
        redis_service.delete(f"shipment:{shipment_id}")
        
        logger.info(f"Shipment updated: {shipment.tracking_number}")
        return shipment
    
    @staticmethod
    def get_dashboard_stats(db: Session, user_id: UUID) -> dict:
        """
        Get dashboard statistics for user.
        SQLAlchemy ORM prevents SQL injection.
        """
        # Active shipments
        active_count = db.query(func.count(Shipment.id)).filter(
            Shipment.user_id == user_id,
            Shipment.status.in_([
                ShipmentStatus.PENDING,
                ShipmentStatus.PROCESSING,
                ShipmentStatus.PICKED_UP,
                ShipmentStatus.IN_TRANSIT,
                ShipmentStatus.CUSTOMS,
                ShipmentStatus.OUT_FOR_DELIVERY
            ])
        ).scalar()
        
        # Delivered shipments
        delivered_count = db.query(func.count(Shipment.id)).filter(
            Shipment.user_id == user_id,
            Shipment.status == ShipmentStatus.DELIVERED
        ).scalar()
        
        # Total spent
        total_spent = db.query(func.sum(Shipment.actual_cost)).filter(
            Shipment.user_id == user_id,
            Shipment.actual_cost.isnot(None)
        ).scalar() or 0
        
        return {
            "active_shipments": active_count or 0,
            "delivered_shipments": delivered_count or 0,
            "total_spent": float(total_spent)
        }


# Global shipment service instance
shipment_service = ShipmentService()
