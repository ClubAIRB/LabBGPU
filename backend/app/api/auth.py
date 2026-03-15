from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from app.core.database import get_db
from app.models import Organization, Head, TestSession, OrganizationType
from app.schemas import (
    OrganizationCreate, OrganizationResponse, OrganizationUpdate,
    HeadResponse, HeadLoginRequest, HeadLoginResponse,
    TestSessionCreate, TestSessionResponse
)
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/head/login", response_model=HeadLoginResponse)
async def head_login(request: HeadLoginRequest, db: Session = Depends(get_db)):
    """
    Login for organization head using INN.
    Creates a session if INN exists in database.
    """
    # Find organization by INN
    organization = db.query(Organization).filter(Organization.inn == request.inn).first()
    
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Организация с данным ИНН не найдена"
        )
    
    # Find or create head for this organization
    head = db.query(Head).filter(Head.organization_id == organization.id).first()
    
    if not head:
        # Create new head record
        head = Head(
            organization_id=organization.id,
            full_name=None
        )
        db.add(head)
        db.commit()
        db.refresh(head)
    
    # Create JWT token
    access_token = create_access_token(
        data={"sub": str(head.id), "type": "head", "inn": organization.inn}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "head": head
    }


@router.get("/me", response_model=HeadResponse)
async def get_current_head(
    db: Session = Depends(get_db),
    current_head_id: int = Depends(lambda: 1)  # TODO: Add proper JWT dependency
):
    """Get current authenticated head profile."""
    head = db.query(Head).filter(Head.id == current_head_id).first()
    
    if not head:
        raise HTTPException(status_code=404, detail="Руководитель не найден")
    
    return head
