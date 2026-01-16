"""
File upload endpoints for shipping documents.
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from typing import List
import uuid
import os
from pathlib import Path

from app.core.config import settings
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter()

UPLOAD_DIR = Path("/tmp/globalship_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/document")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Upload shipping document."""
    # Validate file size
    contents = await file.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max size: {settings.MAX_UPLOAD_SIZE} bytes"
        )
    
    # Validate file extension
    file_ext = file.filename.split('.')[-1].lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed: {settings.ALLOWED_EXTENSIONS}"
        )
    
    # Save file
    file_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{file_id}.{file_ext}"
    
    with open(file_path, "wb") as f:
        f.write(contents)
    
    return {
        "file_id": file_id,
        "filename": file.filename,
        "size": len(contents),
        "path": str(file_path)
    }
