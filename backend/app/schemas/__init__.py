from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class OrganizationType(str, Enum):
    SCHOOL = "school"
    KINDERGARTEN = "kindergarten"
    ADDITIONAL_EDU = "additional_education"


# Organization schemas
class OrganizationBase(BaseModel):
    inn: str = Field(..., min_length=10, max_length=12)
    name: Optional[str] = None
    type: OrganizationType = OrganizationType.SCHOOL
    region: Optional[str] = None


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[OrganizationType] = None
    region: Optional[str] = None


class OrganizationResponse(OrganizationBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


# Head schemas
class HeadBase(BaseModel):
    full_name: Optional[str] = None
    is_candidate: bool = False


class HeadCreate(HeadBase):
    organization_id: Optional[int] = None
    candidate_login: Optional[str] = None
    candidate_password: Optional[str] = None


class HeadUpdate(BaseModel):
    full_name: Optional[str] = None


class HeadResponse(HeadBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    organization_id: Optional[int] = None
    last_test_date: Optional[datetime] = None
    last_results: Optional[Dict[str, Any]] = None
    created_at: datetime
    organization: Optional[OrganizationResponse] = None


# Test session schemas
class TestSessionBase(BaseModel):
    answers: Dict[str, Any]
    scores: Optional[Dict[str, Any]] = None
    case_answers: Optional[Dict[str, Any]] = None


class TestSessionCreate(TestSessionBase):
    head_id: int
    organization_id: Optional[int] = None


class TestSessionResponse(TestSessionBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    head_id: int
    organization_id: Optional[int] = None
    test_date: datetime


# Login schemas
class HeadLoginRequest(BaseModel):
    inn: str = Field(..., min_length=10, max_length=12)


class HeadLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    head: HeadResponse


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
