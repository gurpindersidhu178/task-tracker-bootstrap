from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timedelta

from ...core.database import get_db
from ...core.security import get_current_active_user, require_admin, require_reviewer_or_admin
from ...models.user import User
from ...models.candidate_assignment import CandidateAssignment
from ...models.assignment import Assignment
from ...models.submission import Submission
from ...schemas.user import User as UserSchema

router = APIRouter()


@router.post("/{candidate_id}/assign/{assignment_id}")
async def assign_assignment_to_candidate(
    candidate_id: UUID,
    assignment_id: UUID,
    deadline_days: int = Query(7, ge=1, le=30),
    notes: Optional[str] = None,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Assign an assignment to a candidate"""
    # Check if candidate exists
    candidate = db.query(User).filter(
        User.id == candidate_id,
        User.role == "candidate"
    ).first()
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    
    # Check if assignment exists
    assignment = db.query(Assignment).filter(
        Assignment.id == assignment_id,
        Assignment.is_active == True
    ).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    # Check if already assigned
    existing_assignment = db.query(CandidateAssignment).filter(
        CandidateAssignment.candidate_id == candidate_id,
        CandidateAssignment.assignment_id == assignment_id,
        CandidateAssignment.status.in_(["assigned", "in_progress"])
    ).first()
    if existing_assignment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assignment already assigned to this candidate"
        )
    
    # Create assignment
    deadline = datetime.utcnow() + timedelta(days=deadline_days)
    candidate_assignment = CandidateAssignment(
        candidate_id=candidate_id,
        assignment_id=assignment_id,
        assigned_by=current_user.id,
        deadline=deadline,
        notes=notes
    )
    
    db.add(candidate_assignment)
    db.commit()
    db.refresh(candidate_assignment)
    
    return {
        "message": "Assignment assigned successfully",
        "candidate_assignment_id": candidate_assignment.id,
        "deadline": deadline
    }


@router.get("/assignments", response_model=List[dict])
async def get_candidate_assignments(
    candidate_id: Optional[UUID] = Query(None),
    status: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get candidate assignments"""
    query = db.query(CandidateAssignment).join(Assignment).join(User, User.id == CandidateAssignment.candidate_id)
    
    # Filter by candidate if specified (or show current user's assignments if candidate)
    if candidate_id:
        if current_user.role == "candidate" and current_user.id != candidate_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Can only view own assignments"
            )
        query = query.filter(CandidateAssignment.candidate_id == candidate_id)
    elif current_user.role == "candidate":
        query = query.filter(CandidateAssignment.candidate_id == current_user.id)
    
    if status:
        query = query.filter(CandidateAssignment.status == status)
    
    assignments = query.offset(skip).limit(limit).all()
    
    result = []
    for ca in assignments:
        result.append({
            "id": ca.id,
            "assignment_title": ca.assignment.title,
            "project_name": ca.assignment.project.name,
            "candidate_name": ca.candidate.full_name,
            "candidate_email": ca.candidate.email,
            "status": ca.status,
            "progress_percentage": ca.progress_percentage,
            "assigned_at": ca.assigned_at,
            "deadline": ca.deadline,
            "is_overdue": ca.is_overdue,
            "days_remaining": ca.days_remaining,
            "notes": ca.notes
        })
    
    return result


@router.put("/assignments/{assignment_id}/status")
async def update_assignment_status(
    assignment_id: UUID,
    status: str,
    progress_percentage: Optional[int] = Query(None, ge=0, le=100),
    notes: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update assignment status (for candidates) or admin notes (for admins)"""
    candidate_assignment = db.query(CandidateAssignment).filter(
        CandidateAssignment.id == assignment_id
    ).first()
    
    if not candidate_assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    # Check permissions
    if current_user.role == "candidate":
        if candidate_assignment.candidate_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Can only update own assignments"
            )
        # Candidates can only update status and progress
        candidate_assignment.status = status
        if progress_percentage is not None:
            candidate_assignment.progress_percentage = progress_percentage
    else:
        # Admins/reviewers can update notes
        if notes is not None:
            candidate_assignment.notes = notes
        if status is not None:
            candidate_assignment.status = status
    
    db.commit()
    db.refresh(candidate_assignment)
    
    return {"message": "Assignment status updated successfully"}


@router.get("/candidates", response_model=List[UserSchema])
async def get_candidates(
    skillsets: Optional[List[str]] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(require_reviewer_or_admin),
    db: Session = Depends(get_db)
):
    """Get all candidates with optional filtering"""
    query = db.query(User).filter(User.role == "candidate")
    
    if skillsets:
        for skillset in skillsets:
            query = query.filter(User.skillsets.contains([skillset]))
    
    candidates = query.offset(skip).limit(limit).all()
    return candidates


@router.get("/candidates/{candidate_id}/assignments")
async def get_candidate_assignment_history(
    candidate_id: UUID,
    current_user: User = Depends(require_reviewer_or_admin),
    db: Session = Depends(get_db)
):
    """Get detailed assignment history for a candidate"""
    candidate = db.query(User).filter(
        User.id == candidate_id,
        User.role == "candidate"
    ).first()
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    
    assignments = db.query(CandidateAssignment).filter(
        CandidateAssignment.candidate_id == candidate_id
    ).join(Assignment).all()
    
    result = []
    for ca in assignments:
        assignment_data = {
            "assignment_id": ca.assignment.id,
            "assignment_title": ca.assignment.title,
            "project_name": ca.assignment.project.name,
            "status": ca.status,
            "progress_percentage": ca.progress_percentage,
            "assigned_at": ca.assigned_at,
            "deadline": ca.deadline,
            "is_overdue": ca.is_overdue,
            "notes": ca.notes,
            "submissions": []
        }
        
        # Add submission information
        for submission in ca.submissions:
            assignment_data["submissions"].append({
                "id": submission.id,
                "type": submission.submission_type,
                "status": submission.status,
                "submitted_at": submission.submitted_at,
                "notes": submission.notes
            })
        
        result.append(assignment_data)
    
    return {
        "candidate": {
            "id": candidate.id,
            "name": candidate.full_name,
            "email": candidate.email,
            "skillsets": candidate.skillsets
        },
        "assignments": result
    } 