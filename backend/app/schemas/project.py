from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    domain: Optional[str] = Field(None, max_length=100)
    tech_stack: List[str] = Field(default_factory=list)
    difficulty_level: str = Field(..., regex="^(beginner|intermediate|advanced)$")


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    domain: Optional[str] = Field(None, max_length=100)
    tech_stack: Optional[List[str]] = None
    difficulty_level: Optional[str] = Field(None, regex="^(beginner|intermediate|advanced)$")
    is_active: Optional[bool] = None


class ProjectInDB(ProjectBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Project(ProjectInDB):
    pass


class ProjectWithAssignments(Project):
    assignments_count: int = 0 