from sqlalchemy import Column, String, Text, DateTime, ARRAY, Boolean, Integer, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from ..core.database import Base


class Assignment(Base):
    __tablename__ = "assignments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    skillsets = Column(ARRAY(String), nullable=False)  # Array of required skillsets
    difficulty_level = Column(String(50), nullable=False)  # beginner, intermediate, advanced
    duration_days = Column(Integer, nullable=False)
    instructions = Column(Text)
    starter_code_url = Column(String(500))
    reference_materials = Column(JSON)  # JSON object with links and resources
    submission_criteria = Column(JSON)  # JSON object with evaluation criteria
    is_active = Column(Boolean, default=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="assignments")
    creator = relationship("User", back_populates="created_assignments")
    candidate_assignments = relationship("CandidateAssignment", back_populates="assignment")
    certificates = relationship("Certificate", back_populates="assignment")
    
    def __repr__(self):
        return f"<Assignment(id={self.id}, title={self.title}, project_id={self.project_id})>" 