"""
User CRUD service with SQL injection protection via SQLAlchemy ORM.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from uuid import UUID
import logging

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.services.redis_service import redis_service

logger = logging.getLogger(__name__)


class UserService:
    """User CRUD operations."""
    
    @staticmethod
    def get_by_id(db: Session, user_id: UUID) -> Optional[User]:
        """
        Get user by ID.
        SQLAlchemy ORM prevents SQL injection.
        """
        # Try cache first
        cache_key = f"user:{user_id}"
        cached = redis_service.get(cache_key)
        if cached:
            return User(**cached)
        
        # Query database
        user = db.query(User).filter(User.id == user_id).first()
        
        # Cache result
        if user:
            redis_service.set(cache_key, user.__dict__, expire=300)
        
        return user
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """
        Get user by email.
        SQLAlchemy ORM prevents SQL injection.
        """
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_multi(
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """
        Get multiple users with pagination.
        SQLAlchemy ORM prevents SQL injection.
        """
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, user_in: UserCreate) -> User:
        """
        Create new user.
        SQLAlchemy ORM prevents SQL injection.
        """
        # Hash password
        hashed_password = get_password_hash(user_in.password)
        
        # Create user object
        db_user = User(
            email=user_in.email,
            hashed_password=hashed_password,
            company_name=user_in.company_name,
            phone=user_in.phone,
            full_name=user_in.full_name,
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"User created: {db_user.email}")
        return db_user
    
    @staticmethod
    def update(
        db: Session,
        user_id: UUID,
        user_in: UserUpdate
    ) -> Optional[User]:
        """
        Update user.
        SQLAlchemy ORM prevents SQL injection.
        """
        user = UserService.get_by_id(db, user_id)
        if not user:
            return None
        
        # Update fields
        update_data = user_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        
        # Invalidate cache
        redis_service.delete(f"user:{user_id}")
        
        logger.info(f"User updated: {user.email}")
        return user
    
    @staticmethod
    def authenticate(
        db: Session,
        email: str,
        password: str
    ) -> Optional[User]:
        """
        Authenticate user with email and password.
        """
        user = UserService.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    @staticmethod
    def is_active(user: User) -> bool:
        """Check if user is active."""
        return user.is_active
    
    @staticmethod
    def is_superuser(user: User) -> bool:
        """Check if user is superuser."""
        return user.is_superuser


# Global user service instance
user_service = UserService()
