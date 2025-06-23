from sqlalchemy import Column, String, Boolean, DateTime, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from ..core.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="candidate")  # admin, reviewer, candidate
    skillsets = Column(ARRAY(String), default=[])  # Array of skillsets
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    created_assignments = relationship("Assignment", back_populates="creator")
    assigned_assignments = relationship("CandidateAssignment", foreign_keys="CandidateAssignment.candidate_id", back_populates="candidate")
    reviews = relationship("Review", back_populates="reviewer")
    certificates = relationship("Certificate", back_populates="candidate")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
    
    @property
    def is_admin(self) -> bool:
        return self.role == "admin"
    
    @property
    def is_reviewer(self) -> bool:
        return self.role == "reviewer"
    
    @property
    def is_candidate(self) -> bool:
        return self.role == "candidate" 