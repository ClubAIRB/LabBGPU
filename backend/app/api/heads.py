from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import timedelta

from app.core.database import get_db
from app.models import Head, TestSession, Organization
from app.schemas import HeadResponse, HeadUpdate, TestSessionCreate, TestSessionResponse
from app.core.security import create_access_token

router = APIRouter(prefix="/heads", tags=["heads"])


@router.get("/me", response_model=HeadResponse)
async def get_current_head_profile(
    db: Session = Depends(get_db),
    head_id: int = Depends(lambda: 1)  # TODO: Extract from JWT token
):
    """Get current head profile with organization info."""
    head = db.query(Head).filter(Head.id == head_id).first()
    
    if not head:
        raise HTTPException(status_code=404, detail="Руководитель не найден")
    
    return head


@router.put("/me", response_model=HeadResponse)
async def update_current_head_profile(
    update_data: HeadUpdate,
    db: Session = Depends(get_db),
    head_id: int = Depends(lambda: 1)  # TODO: Extract from JWT token
):
    """Update current head profile (e.g., full name)."""
    head = db.query(Head).filter(Head.id == head_id).first()
    
    if not head:
        raise HTTPException(status_code=404, detail="Руководитель не найден")
    
    # Update fields
    if update_data.full_name is not None:
        head.full_name = update_data.full_name
    
    db.commit()
    db.refresh(head)
    
    return head


@router.post("/sessions", response_model=TestSessionResponse)
async def create_test_session(
    session_data: TestSessionCreate,
    db: Session = Depends(get_db),
    head_id: int = Depends(lambda: 1)  # TODO: Extract from JWT token
):
    """Create a new test session for the current head."""
    head = db.query(Head).filter(Head.id == head_id).first()
    
    if not head:
        raise HTTPException(status_code=404, detail="Руководитель не найден")
    
    # Create test session
    test_session = TestSession(
        head_id=head_id,
        organization_id=head.organization_id,
        answers=session_data.answers,
        scores=session_data.scores,
        case_answers=session_data.case_answers
    )
    
    db.add(test_session)
    
    # Update head's last test date and results
    head.last_test_date = test_session.test_date
    head.last_results = session_data.scores
    
    db.commit()
    db.refresh(test_session)
    
    return test_session


@router.get("/sessions", response_model=List[TestSessionResponse])
async def get_head_test_sessions(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    head_id: int = Depends(lambda: 1)  # TODO: Extract from JWT token
):
    """Get test sessions for current head."""
    sessions = db.query(TestSession).filter(
        TestSession.head_id == head_id
    ).order_by(TestSession.test_date.desc()).offset(skip).limit(limit).all()
    
    return sessions
