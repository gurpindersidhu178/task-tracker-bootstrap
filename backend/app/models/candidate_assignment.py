from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from ..core.database import Base


class CandidateAssignment(Base):
    __tablename__ = "candidate_assignments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    assignment_id = Column(UUID(as_uuid=True), ForeignKey("assignments.id"), nullable=False)
    assigned_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())
    deadline = Column(DateTime(timezone=True))
    status = Column(String(50), default="assigned")  # assigned, in_progress, submitted, reviewed, completed, failed
    progress_percentage = Column(Integer, default=0)
    notes = Column(String(1000))  # Admin notes about the assignment
    
    # Relationships
    candidate = relationship("User", foreign_keys=[candidate_id], back_populates="assigned_assignments")
    assignment = relationship("Assignment", back_populates="candidate_assignments")
    assigner = relationship("User", foreign_keys=[assigned_by])
    submissions = relationship("Submission", back_populates="candidate_assignment")
    
    def __repr__(self):
        return f"<CandidateAssignment(id={self.id}, candidate_id={self.candidate_id}, assignment_id={self.assignment_id})>"
    
    @property
    def is_overdue(self) -> bool:
        if not self.deadline:
            return False
        return func.now() > self.deadline and self.status not in ["completed", "failed"]
    
    @property
    def days_remaining(self) -> int:
        if not self.deadline:
            return 0
        from datetime import datetime
        remaining = self.deadline - datetime.utcnow()
        return max(0, remaining.days) 