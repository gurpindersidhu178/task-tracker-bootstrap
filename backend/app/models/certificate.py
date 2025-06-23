from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, ARRAY, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from ..core.database import Base


class Certificate(Base):
    __tablename__ = "certificates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    assignment_id = Column(UUID(as_uuid=True), ForeignKey("assignments.id"), nullable=False)
    certificate_number = Column(String(50), unique=True, nullable=False, index=True)
    score = Column(Integer)  # Final score from review
    skills_demonstrated = Column(ARRAY(String), default=[])
    issued_at = Column(DateTime(timezone=True), server_default=func.now())
    pdf_url = Column(String(500))  # URL to generated PDF
    is_active = Column(Boolean, default=True)
    
    # Relationships
    candidate = relationship("User", back_populates="certificates")
    assignment = relationship("Assignment", back_populates="certificates")
    
    def __repr__(self):
        return f"<Certificate(id={self.id}, number={self.certificate_number}, candidate_id={self.candidate_id})>"
    
    @property
    def is_passing_score(self) -> bool:
        return (self.score or 0) >= 70  # 70% passing threshold 