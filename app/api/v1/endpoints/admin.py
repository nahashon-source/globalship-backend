"""
Admin-only endpoints for system management.
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List
from datetime import datetime, timedelta

from app.db.session import get_db
from app.api.dependencies import get_current_superuser
from app.models.user import User
from app.models.shipment import Shipment, ShipmentStatus
from app.models.quote import Quote, QuoteStatus
from app.models.contact_message import ContactMessage
from app.schemas.user import UserResponse
from app.schemas.shipment import ShipmentResponse, ShipmentUpdate
from app.schemas.quote import QuoteResponse, QuoteUpdate
from app.schemas.contact_message import ContactMessageResponse, ContactMessageUpdate
from app.services.user_service import user_service
from app.services.shipment_service import shipment_service
from app.services.quote_service import quote_service
from app.services.contact_message_service import contact_message_service

router = APIRouter()


@router.get("/stats")
def get_system_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Get system statistics (admin only)."""
    
    # User stats
    total_users = db.query(func.count(User.id)).scalar()
    active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar()
    new_users_30d = db.query(func.count(User.id)).filter(
        User.created_at >= datetime.utcnow() - timedelta(days=30)
    ).scalar()
    
    # Shipment stats
    total_shipments = db.query(func.count(Shipment.id)).scalar()
    active_shipments = db.query(func.count(Shipment.id)).filter(
        Shipment.status.in_([
            ShipmentStatus.PENDING,
            ShipmentStatus.PROCESSING,
            ShipmentStatus.IN_TRANSIT,
            ShipmentStatus.CUSTOMS,
            ShipmentStatus.OUT_FOR_DELIVERY
        ])
    ).scalar()
    delivered_shipments = db.query(func.count(Shipment.id)).filter(
        Shipment.status == ShipmentStatus.DELIVERED
    ).scalar()
    
    # Quote stats
    total_quotes = db.query(func.count(Quote.id)).scalar()
    pending_quotes = db.query(func.count(Quote.id)).filter(
        Quote.status == QuoteStatus.PENDING
    ).scalar()
    
    # Contact message stats
    unread_messages = db.query(func.count(ContactMessage.id)).filter(
        ContactMessage.status == "new"
    ).scalar()
    
    # Revenue (sum of actual costs)
    total_revenue = db.query(func.sum(Shipment.actual_cost)).filter(
        Shipment.actual_cost.isnot(None)
    ).scalar() or 0
    
    return {
        "users": {
            "total": total_users,
            "active": active_users,
            "new_last_30_days": new_users_30d
        },
        "shipments": {
            "total": total_shipments,
            "active": active_shipments,
            "delivered": delivered_shipments
        },
        "quotes": {
            "total": total_quotes,
            "pending": pending_quotes
        },
        "messages": {
            "unread": unread_messages
        },
        "revenue": {
            "total": float(total_revenue),
            "currency": "USD"
        }
    }


@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Get all users (admin only)."""
    users = user_service.get_multi(db, skip=skip, limit=limit)
    return users


@router.get("/shipments", response_model=List[ShipmentResponse])
def get_all_shipments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: ShipmentStatus = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Get all shipments (admin only)."""
    query = db.query(Shipment)
    
    if status:
        query = query.filter(Shipment.status == status)
    
    shipments = query.order_by(desc(Shipment.created_at)).offset(skip).limit(limit).all()
    return shipments


@router.put("/shipments/{shipment_id}/status", response_model=ShipmentResponse)
def update_shipment_status_admin(
    shipment_id: str,
    shipment_update: ShipmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Update shipment status (admin only)."""
    from uuid import UUID
    
    shipment = shipment_service.update(db, UUID(shipment_id), shipment_update)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    
    return shipment


@router.get("/quotes", response_model=List[QuoteResponse])
def get_all_quotes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: QuoteStatus = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Get all quotes (admin only)."""
    query = db.query(Quote)
    
    if status:
        query = query.filter(Quote.status == status)
    
    quotes = query.order_by(desc(Quote.created_at)).offset(skip).limit(limit).all()
    return quotes


@router.put("/quotes/{quote_id}", response_model=QuoteResponse)
def update_quote_admin(
    quote_id: str,
    quote_update: QuoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Update quote (admin only)."""
    from uuid import UUID
    
    quote = quote_service.update(db, UUID(quote_id), quote_update)
    if not quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quote not found"
        )
    
    return quote


@router.get("/messages", response_model=List[ContactMessageResponse])
def get_all_messages(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """Get all contact messages (admin only)."""
    messages, _ = contact_message_service.get_all(db, skip=skip, limit=limit)
    return messages
