from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Boolean, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class OrganizationType(str, enum.Enum):
    SCHOOL = "school"
    KINDERGARTEN = "kindergarten"
    ADDITIONAL_EDU = "additional_education"


class Organization(Base):
    """Organization model (schools, kindergartens, etc.)."""
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    inn = Column(String(12), unique=True, index=True, nullable=False)
    name = Column(String(500), nullable=True)
    type = Column(SQLEnum(OrganizationType), nullable=False, default=OrganizationType.SCHOOL)
    region = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    heads = relationship("Head", back_populates="organization", cascade="all, delete-orphan")
    test_sessions = relationship("TestSession", back_populates="organization", cascade="all, delete-orphan")


class Head(Base):
    """Head/Manager of organization."""
    __tablename__ = "heads"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(300), nullable=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    last_test_date = Column(DateTime(timezone=True), nullable=True)
    last_results = Column(JSON, nullable=True)
    is_candidate = Column(Boolean, default=False)
    candidate_login = Column(String(100), nullable=True)
    candidate_password = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    organization = relationship("Organization", back_populates="heads")
    test_sessions = relationship("TestSession", back_populates="head", cascade="all, delete-orphan")


class TestSession(Base):
    """Test session for head assessment."""
    __tablename__ = "test_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    head_id = Column(Integer, ForeignKey("heads.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    test_date = Column(DateTime(timezone=True), server_default=func.now())
    answers = Column(JSON, nullable=False)
    scores = Column(JSON, nullable=True)
    case_answers = Column(JSON, nullable=True)
    
    head = relationship("Head", back_populates="test_sessions")
    organization = relationship("Organization", back_populates="test_sessions")
