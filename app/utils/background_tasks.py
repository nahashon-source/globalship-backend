"""
Background tasks for async operations.
"""
from fastapi import BackgroundTasks
import logging

from app.services.email_service import email_service

logger = logging.getLogger(__name__)


def send_email_task(to_email: str, subject: str, body: str):
    """Background task to send email."""
    try:
        email_service.send_email(to_email, subject, body)
        logger.info(f"Email sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")


def process_shipment_update(shipment_id: str, status: str):
    """Background task to process shipment update."""
    logger.info(f"Processing shipment update: {shipment_id} -> {status}")
    # Add your business logic here
