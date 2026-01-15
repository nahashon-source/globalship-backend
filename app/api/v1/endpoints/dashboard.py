"""
Dashboard API endpoints.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.dashboard import DashboardResponse, DashboardStats
from app.services.shipment_service import shipment_service
from app.services.quote_service import quote_service
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/stats", response_model=DashboardResponse)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get dashboard statistics and recent shipments for current user.
    """
    # Get statistics
    stats = shipment_service.get_dashboard_stats(db, current_user.id)
    
    # Get pending quotes count
    pending_quotes = quote_service.get_pending_count(db, current_user.id)
    stats["pending_quotes"] = pending_quotes
    
    # Get recent shipments (last 10)
    recent_shipments, _ = shipment_service.get_user_shipments(
        db,
        current_user.id,
        skip=0,
        limit=10
    )
    
    return {
        "stats": DashboardStats(**stats),
        "recent_shipments": recent_shipments
    }
