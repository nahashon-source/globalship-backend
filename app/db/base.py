"""
SQLAlchemy base class for all database models.
Import all models here to ensure they're registered with Alembic.
"""
from sqlalchemy.ext.declarative import declarative_base

# Create base class for all models
Base = declarative_base()

# Models will be imported by Alembic and other modules as needed
# DO NOT import models here to avoid circular imports
