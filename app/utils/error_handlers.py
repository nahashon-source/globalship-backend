"""
Global error handlers for FastAPI.
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
import logging

from app.utils.exceptions import (
    GlobalShipException,
    ResourceNotFoundException,
    UnauthorizedException,
    ValidationException,
    DuplicateResourceException
)

logger = logging.getLogger(__name__)


async def globalship_exception_handler(request: Request, exc: GlobalShipException):
    """Handle custom GlobalShip exceptions."""
    logger.error(f"GlobalShip exception: {exc.message}")
    
    status_code = status.HTTP_400_BAD_REQUEST
    
    if isinstance(exc, ResourceNotFoundException):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, UnauthorizedException):
        status_code = status.HTTP_401_UNAUTHORIZED
    elif isinstance(exc, DuplicateResourceException):
        status_code = status.HTTP_409_CONFLICT
    
    return JSONResponse(
        status_code=status_code,
        content={"detail": exc.message}
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.warning(f"Validation error: {errors}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation error", "errors": errors}
    )


async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors."""
    logger.error(f"Database integrity error: {exc}")
    
    error_msg = str(exc.orig)
    
    if "duplicate key" in error_msg.lower():
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Resource already exists"}
        )
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Database constraint violation"}
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """Handle uncaught exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )
