"""
SQLAlchemy base class for all database models.
Import all models here to ensure they're registered with Alembic.
"""
from sqlalchemy.ext.declarative import declarative_base

# Create base class for all models
Base = declarative_base()

# Import all models here for Alembic to detect them
from app.models.user import User
from app.models.shipment import Shipment
from app.models.shipment_event import ShipmentEvent
from app.models.quote import Quote
from app.models.contact_message import ContactMessage
