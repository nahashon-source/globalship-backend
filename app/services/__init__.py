"""
Services package - exports all service instances.
"""
from app.services.redis_service import redis_service
from app.services.user_service import user_service
from app.services.shipment_service import shipment_service
from app.services.shipment_event_service import shipment_event_service
from app.services.quote_service import quote_service
from app.services.contact_message_service import contact_message_service
from app.services.email_service import email_service

__all__ = [
    "redis_service",
    "user_service",
    "shipment_service",
    "shipment_event_service",
    "quote_service",
    "contact_message_service",
    "email_service",
]
