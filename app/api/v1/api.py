"""
API v1 router - combines all endpoint routers.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    shipments,
    shipment_events,
    quotes,
    contact,
    dashboard,
    admin
)

api_router = APIRouter()

# Public endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(contact.router, prefix="/contact", tags=["Contact"])

# Authenticated user endpoints
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(shipments.router, prefix="/shipments", tags=["Shipments"])
api_router.include_router(shipment_events.router, prefix="/events", tags=["Shipment Events"])
api_router.include_router(quotes.router, prefix="/quotes", tags=["Quotes"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

# Admin endpoints
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
