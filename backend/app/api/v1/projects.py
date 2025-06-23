from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from ...core.database import get_db
from ...core.security import get_current_active_user, require_admin
from ...models.user import User
from ...models.project import Project
from ...schemas.project import ProjectCreate, ProjectUpdate, Project as ProjectSchema, ProjectWithAssignments

router = APIRouter()


@router.post("/", response_model=ProjectSchema)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Create a new project"""
    db_project = Project(**project_data.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@router.get("/", response_model=List[ProjectWithAssignments])
async def get_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    domain: Optional[str] = Query(None),
    difficulty_level: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all projects with optional filtering"""
    query = db.query(Project)
    
    if domain:
        query = query.filter(Project.domain == domain)
    if difficulty_level:
        query = query.filter(Project.difficulty_level == difficulty_level)
    if is_active is not None:
        query = query.filter(Project.is_active == is_active)
    
    projects = query.offset(skip).limit(limit).all()
    
    # Add assignment counts
    result = []
    for project in projects:
        project_dict = ProjectWithAssignments.from_orm(project)
        project_dict.assignments_count = len(project.assignments)
        result.append(project_dict)
    
    return result


@router.get("/{project_id}", response_model=ProjectSchema)
async def get_project(
    project_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific project by ID"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return project


@router.put("/{project_id}", response_model=ProjectSchema)
async def update_project(
    project_id: UUID,
    project_data: ProjectUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update a project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    update_data = project_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}")
async def delete_project(
    project_id: UUID,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Delete a project (soft delete by setting is_active=False)"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    project.is_active = False
    db.commit()
    
    return {"message": "Project deleted successfully"}


@router.get("/domains/list")
async def get_project_domains(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get list of all project domains"""
    domains = db.query(Project.domain).filter(
        Project.domain.isnot(None),
        Project.is_active == True
    ).distinct().all()
    return [domain[0] for domain in domains if domain[0]] 