"""
Shipment management API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from math import ceil

from app.db.session import get_db
from app.schemas.shipment import (
    ShipmentCreate,
    ShipmentUpdate,
    ShipmentResponse,
    ShipmentListResponse
)
from app.models.shipment import ShipmentStatus
from app.services.shipment_service import shipment_service
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=ShipmentResponse, status_code=status.HTTP_201_CREATED)
def create_shipment(
    shipment_in: ShipmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new shipment.
    """
    shipment = shipment_service.create(db, current_user.id, shipment_in)
    return shipment


@router.get("/", response_model=ShipmentListResponse)
def read_shipments(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[ShipmentStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get current user's shipments with pagination.
    """
    shipments, total = shipment_service.get_user_shipments(
        db,
        current_user.id,
        skip=skip,
        limit=limit,
        status=status
    )
    
    pages = ceil(total / limit) if limit > 0 else 0
    page = (skip // limit) + 1 if limit > 0 else 1
    
    return {
        "items": shipments,
        "total": total,
        "page": page,
        "page_size": limit,
        "pages": pages
    }


@router.get("/{shipment_id}", response_model=ShipmentResponse)
def read_shipment(
    shipment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get shipment by ID.
    """
    shipment = shipment_service.get_by_id(db, shipment_id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    
    # Check ownership
    if shipment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return shipment


@router.put("/{shipment_id}", response_model=ShipmentResponse)
def update_shipment(
    shipment_id: UUID,
    shipment_in: ShipmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update shipment.
    """
    shipment = shipment_service.get_by_id(db, shipment_id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    
    # Check ownership
    if shipment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    updated_shipment = shipment_service.update(db, shipment_id, shipment_in)
    return updated_shipment


@router.get("/track/{tracking_number}", response_model=ShipmentResponse)
def track_shipment(
    tracking_number: str,
    db: Session = Depends(get_db)
):
    """
    Public endpoint to track shipment by tracking number.
    """
    shipment = shipment_service.get_by_tracking_number(db, tracking_number)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    return shipment
