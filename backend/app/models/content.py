from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, JSON, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


# Association table for case templates and documents
case_template_documents = Table(
    'case_template_documents',
    Base.metadata,
    Column('case_template_id', Integer, ForeignKey('case_templates.id')),
    Column('document_id', Integer, ForeignKey('normative_documents.id'))
)


class NormativeDocument(Base):
    """Normative documents for RAG context."""
    __tablename__ = "normative_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    organization_type = Column(String(50), nullable=True)
    category = Column(String(100), nullable=True)  # кадры, процессы, результаты, информация, ресурсы
    file_path = Column(String(300), nullable=True)
    content = Column(Text, nullable=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    case_templates = relationship(
        "CaseTemplate",
        secondary=case_template_documents,
        back_populates="normative_documents"
    )


class GeneratedQuestion(Base):
    """Generated test questions."""
    __tablename__ = "generated_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), nullable=False)
    question_text = Column(Text, nullable=False)
    answer_variants = Column(JSON, nullable=True)  # List of answer options
    correct_answer = Column(String(500), nullable=True)
    status = Column(String(20), default="draft")  # draft, published
    organization_type = Column(String(50), nullable=True)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())


class CaseTemplate(Base):
    """Templates for case generation."""
    __tablename__ = "case_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_type = Column(String(50), nullable=False)
    title = Column(String(300), nullable=True)
    template_text = Column(Text, nullable=False)
    
    normative_documents = relationship(
        "NormativeDocument",
        secondary=case_template_documents,
        back_populates="case_templates"
    )


class GeneratedCase(Base):
    """Generated cases with AI answers."""
    __tablename__ = "generated_cases"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_type = Column(String(50), nullable=False)
    case_text = Column(Text, nullable=False)
    ai_answer = Column(Text, nullable=True)
    status = Column(String(20), default="draft")  # draft, published
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
