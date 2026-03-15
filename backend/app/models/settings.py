from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class PromptTemplate(Base):
    """Prompt templates for AI generation."""
    __tablename__ = "prompt_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), nullable=False)  # test_questions, cases, case_answers, report, edu_program
    organization_type = Column(String(50), nullable=True)  # school, kindergarten, additional_education
    template_text = Column(Text, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ModelSettings(Base):
    """AI model settings."""
    __tablename__ = "model_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100), nullable=False)
    parameters = Column(JSON, nullable=True)  # temperature, penalties, max_tokens, etc.
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class EmbeddingModel(Base):
    """Embedding model configuration."""
    __tablename__ = "embedding_models"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(200), nullable=False)
    model_type = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)


class SimilarityThreshold(Base):
    """Semantic similarity threshold for question variation."""
    __tablename__ = "similarity_thresholds"
    
    id = Column(Integer, primary_key=True, index=True)
    threshold = Column(Float, default=0.8)
    description = Column(String(300), nullable=True)
