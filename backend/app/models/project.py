from sqlalchemy import Column, String, Text, DateTime, ARRAY, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from ..core.database import Base


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    domain = Column(String(100))  # e.g., 'sports', 'e-commerce', 'finance'
    tech_stack = Column(ARRAY(String), default=[])
    difficulty_level = Column(String(50), nullable=False)  # beginner, intermediate, advanced
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    assignments = relationship("Assignment", back_populates="project")
    certificates = relationship("Certificate", back_populates="assignment")
    
    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name}, domain={self.domain})>" 