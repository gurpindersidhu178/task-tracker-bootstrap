from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from ..core.database import Base


class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_assignment_id = Column(UUID(as_uuid=True), ForeignKey("candidate_assignments.id"), nullable=False)
    submission_type = Column(String(50), nullable=False)  # github_pr, file_upload
    submission_url = Column(String(500))  # For GitHub PRs
    files = Column(JSON)  # For file uploads: [{"name": "file.zip", "url": "s3://..."}]
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), default="submitted")  # submitted, under_review, approved, rejected, resubmission_required
    notes = Column(Text)  # Candidate notes about the submission
    
    # Relationships
    candidate_assignment = relationship("CandidateAssignment", back_populates="submissions")
    reviews = relationship("Review", back_populates="submission")
    
    def __repr__(self):
        return f"<Submission(id={self.id}, type={self.submission_type}, status={self.status})>"
    
    @property
    def is_github_submission(self) -> bool:
        return self.submission_type == "github_pr"
    
    @property
    def is_file_submission(self) -> bool:
        return self.submission_type == "file_upload" 