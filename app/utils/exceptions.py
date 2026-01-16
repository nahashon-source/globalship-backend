"""
Custom exceptions and error handlers.
"""
from fastapi import HTTPException, status


class GlobalShipException(Exception):
    """Base exception for GlobalShip application."""
    pass


class ResourceNotFoundException(GlobalShipException):
    """Resource not found exception."""
    def __init__(self, resource: str, id: str):
        self.message = f"{resource} with id {id} not found"
        super().__init__(self.message)


class UnauthorizedException(GlobalShipException):
    """Unauthorized access exception."""
    def __init__(self, message: str = "Unauthorized access"):
        self.message = message
        super().__init__(self.message)


class ValidationException(GlobalShipException):
    """Validation error exception."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class DuplicateResourceException(GlobalShipException):
    """Duplicate resource exception."""
    def __init__(self, resource: str, field: str, value: str):
        self.message = f"{resource} with {field}='{value}' already exists"
        super().__init__(self.message)
