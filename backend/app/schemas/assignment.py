from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


class AssignmentBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    skillsets: List[str] = Field(..., min_items=1)
    difficulty_level: str = Field(..., regex="^(beginner|intermediate|advanced)$")
    duration_days: int = Field(..., gt=0, le=30)
    instructions: Optional[str] = None
    starter_code_url: Optional[HttpUrl] = None
    reference_materials: Optional[Dict[str, Any]] = None
    submission_criteria: Optional[Dict[str, Any]] = None


class AssignmentCreate(AssignmentBase):
    project_id: UUID


class AssignmentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    skillsets: Optional[List[str]] = Field(None, min_items=1)
    difficulty_level: Optional[str] = Field(None, regex="^(beginner|intermediate|advanced)$")
    duration_days: Optional[int] = Field(None, gt=0, le=30)
    instructions: Optional[str] = None
    starter_code_url: Optional[HttpUrl] = None
    reference_materials: Optional[Dict[str, Any]] = None
    submission_criteria: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class AssignmentInDB(AssignmentBase):
    id: UUID
    project_id: UUID
    is_active: bool
    created_by: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Assignment(AssignmentInDB):
    pass


class AssignmentWithProject(Assignment):
    project_name: str
    project_domain: Optional[str] = None


class AssignmentWithStats(Assignment):
    total_candidates: int = 0
    completed_count: int = 0
    in_progress_count: int = 0
    overdue_count: int = 0 