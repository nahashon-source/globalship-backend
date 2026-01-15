"""
Shipment event/timeline API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.shipment_event import (
    ShipmentEventCreate,
    ShipmentTimelineResponse
)
from app.services.shipment_service import shipment_service
from app.services.shipment_event_service import shipment_event_service
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_shipment_event(
    event_in: ShipmentEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new shipment event.
    """
    # Verify shipment exists and user owns it
    shipment = shipment_service.get_by_id(db, event_in.shipment_id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    
    if shipment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    event = shipment_event_service.create(db, event_in)
    return event


@router.get("/{shipment_id}/timeline", response_model=ShipmentTimelineResponse)
def get_shipment_timeline(
    shipment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get shipment timeline/events.
    """
    # Verify shipment exists and user owns it
    shipment = shipment_service.get_by_id(db, shipment_id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    
    if shipment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    events = shipment_event_service.get_shipment_timeline(db, shipment_id)
    
    return {
        "tracking_number": shipment.tracking_number,
        "events": events
    }


@router.get("/track/{tracking_number}/timeline", response_model=ShipmentTimelineResponse)
def track_shipment_timeline(
    tracking_number: str,
    db: Session = Depends(get_db)
):
    """
    Public endpoint to get shipment timeline by tracking number.
    """
    shipment = shipment_service.get_by_tracking_number(db, tracking_number)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    
    events = shipment_event_service.get_shipment_timeline(db, shipment.id)
    
    return {
        "tracking_number": shipment.tracking_number,
        "events": events
    }
