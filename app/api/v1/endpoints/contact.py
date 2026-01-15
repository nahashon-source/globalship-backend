"""
Contact form API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.contact_message import ContactMessageCreate
from app.services.contact_message_service import contact_message_service

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def submit_contact_form(
    message_in: ContactMessageCreate,
    db: Session = Depends(get_db)
):
    """
    Submit contact form (public endpoint).
    """
    message = contact_message_service.create(db, message_in)
    
    # TODO: Send email notification to admin
    # You can implement email sending here
    
    return {
        "message": "Thank you for contacting us. We will get back to you soon.",
        "id": str(message.id)
    }
