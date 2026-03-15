from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON, Float, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class ClusterResult(Base):
    """Clustering results for heads analysis."""
    __tablename__ = "cluster_results"
    
    id = Column(Integer, primary_key=True, index=True)
    cluster_name = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    heads_data = Column(JSON, nullable=True)  # List of head IDs and their data
    avg_scores = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TestingSchedule(Base):
    """Scheduled testing sessions."""
    __tablename__ = "testing_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_inn = Column(String(12), nullable=True)
    candidate_name = Column(String(300), nullable=True)
    test_date = Column(Date, nullable=False)
    test_time = Column(Time, nullable=True)
    status = Column(String(50), default="scheduled")  # scheduled, completed, cancelled
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
