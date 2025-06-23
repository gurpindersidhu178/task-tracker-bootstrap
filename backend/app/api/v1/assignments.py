from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from ...core.database import get_db
from ...core.security import get_current_active_user, require_admin, require_reviewer_or_admin
from ...models.user import User
from ...models.assignment import Assignment
from ...models.project import Project
from ...schemas.assignment import AssignmentCreate, AssignmentUpdate, Assignment as AssignmentSchema, AssignmentWithProject, AssignmentWithStats

router = APIRouter()


@router.post("/", response_model=AssignmentSchema)
async def create_assignment(
    assignment_data: AssignmentCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Create a new assignment"""
    # Verify project exists
    project = db.query(Project).filter(Project.id == assignment_data.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db_assignment = Assignment(
        **assignment_data.dict(),
        created_by=current_user.id
    )
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment


@router.get("/", response_model=List[AssignmentWithProject])
async def get_assignments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    project_id: Optional[UUID] = Query(None),
    skillsets: Optional[List[str]] = Query(None),
    difficulty_level: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all assignments with optional filtering"""
    query = db.query(Assignment).join(Project)
    
    if project_id:
        query = query.filter(Assignment.project_id == project_id)
    if skillsets:
        # Filter by any of the required skillsets
        for skillset in skillsets:
            query = query.filter(Assignment.skillsets.contains([skillset]))
    if difficulty_level:
        query = query.filter(Assignment.difficulty_level == difficulty_level)
    if is_active is not None:
        query = query.filter(Assignment.is_active == is_active)
    
    assignments = query.offset(skip).limit(limit).all()
    
    # Add project information
    result = []
    for assignment in assignments:
        assignment_dict = AssignmentWithProject.from_orm(assignment)
        assignment_dict.project_name = assignment.project.name
        assignment_dict.project_domain = assignment.project.domain
        result.append(assignment_dict)
    
    return result


@router.get("/{assignment_id}", response_model=AssignmentWithProject)
async def get_assignment(
    assignment_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific assignment by ID"""
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    assignment_dict = AssignmentWithProject.from_orm(assignment)
    assignment_dict.project_name = assignment.project.name
    assignment_dict.project_domain = assignment.project.domain
    
    return assignment_dict


@router.put("/{assignment_id}", response_model=AssignmentSchema)
async def update_assignment(
    assignment_id: UUID,
    assignment_data: AssignmentUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update an assignment"""
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    update_data = assignment_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(assignment, field, value)
    
    db.commit()
    db.refresh(assignment)
    return assignment


@router.delete("/{assignment_id}")
async def delete_assignment(
    assignment_id: UUID,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Delete an assignment (soft delete)"""
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    assignment.is_active = False
    db.commit()
    
    return {"message": "Assignment deleted successfully"}


@router.get("/{assignment_id}/stats", response_model=AssignmentWithStats)
async def get_assignment_stats(
    assignment_id: UUID,
    current_user: User = Depends(require_reviewer_or_admin),
    db: Session = Depends(get_db)
):
    """Get assignment statistics"""
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    # Calculate stats
    candidate_assignments = assignment.candidate_assignments
    total_candidates = len(candidate_assignments)
    completed_count = len([ca for ca in candidate_assignments if ca.status == "completed"])
    in_progress_count = len([ca for ca in candidate_assignments if ca.status == "in_progress"])
    overdue_count = len([ca for ca in candidate_assignments if ca.is_overdue])
    
    assignment_dict = AssignmentWithStats.from_orm(assignment)
    assignment_dict.total_candidates = total_candidates
    assignment_dict.completed_count = completed_count
    assignment_dict.in_progress_count = in_progress_count
    assignment_dict.overdue_count = overdue_count
    
    return assignment_dict


@router.get("/skillsets/list")
async def get_assignment_skillsets(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get list of all assignment skillsets"""
    skillsets = db.query(Assignment.skillsets).filter(
        Assignment.is_active == True
    ).all()
    
    # Flatten and deduplicate skillsets
    all_skillsets = set()
    for skillset_list in skillsets:
        all_skillsets.update(skillset_list[0] or [])
    
    return list(all_skillsets) 