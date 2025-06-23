from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from ..core.database import Base


class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    submission_id = Column(UUID(as_uuid=True), ForeignKey("submissions.id"), nullable=False)
    reviewer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    score = Column(Integer)  # Overall score (0-100)
    feedback = Column(Text)  # General feedback
    criteria_scores = Column(JSON)  # Detailed scoring by criteria
    reviewed_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), default="pending")  # pending, in_progress, completed
    
    # Relationships
    submission = relationship("Submission", back_populates="reviews")
    reviewer = relationship("User", back_populates="reviews")
    
    def __repr__(self):
        return f"<Review(id={self.id}, submission_id={self.submission_id}, reviewer_id={self.reviewer_id})>"
    
    @property
    def is_completed(self) -> bool:
        return self.status == "completed"
    
    @property
    def score_percentage(self) -> float:
        return (self.score or 0) / 100.0 