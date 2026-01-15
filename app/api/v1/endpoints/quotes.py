"""
Quote management API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from math import ceil

from app.db.session import get_db
from app.schemas.quote import (
    QuoteCreate,
    QuoteUpdate,
    QuoteResponse,
    QuoteListResponse
)
from app.models.quote import QuoteStatus
from app.services.quote_service import quote_service
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=QuoteResponse, status_code=status.HTTP_201_CREATED)
def create_quote(
    quote_in: QuoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new quote request.
    """
    quote = quote_service.create(db, current_user.id, quote_in)
    return quote


@router.get("/", response_model=QuoteListResponse)
def read_quotes(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[QuoteStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get current user's quotes with pagination.
    """
    quotes, total = quote_service.get_user_quotes(
        db,
        current_user.id,
        skip=skip,
        limit=limit,
        status=status
    )
    
    pages = ceil(total / limit) if limit > 0 else 0
    page = (skip // limit) + 1 if limit > 0 else 1
    
    return {
        "items": quotes,
        "total": total,
        "page": page,
        "page_size": limit,
        "pages": pages
    }


@router.get("/{quote_id}", response_model=QuoteResponse)
def read_quote(
    quote_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get quote by ID.
    """
    quote = quote_service.get_by_id(db, quote_id)
    if not quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quote not found"
        )
    
    # Check ownership
    if quote.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return quote


@router.put("/{quote_id}", response_model=QuoteResponse)
def update_quote(
    quote_id: UUID,
    quote_in: QuoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update quote (admin only in production).
    """
    quote = quote_service.get_by_id(db, quote_id)
    if not quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quote not found"
        )
    
    # In production, only admin should update quotes
    # For now, allowing user to update their own quotes
    if quote.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    updated_quote = quote_service.update(db, quote_id, quote_in)
    return updated_quote
