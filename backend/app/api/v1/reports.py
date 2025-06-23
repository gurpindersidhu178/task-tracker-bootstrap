from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
from datetime import datetime, timedelta
from uuid import UUID

from ...core.database import get_db
from ...core.security import get_current_active_user, require_admin
from ...models.user import User
from ...models.assignment import Assignment
from ...models.candidate_assignment import CandidateAssignment
from ...models.review import Review
from ...models.certificate import Certificate
from ...models.project import Project

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard_stats(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics"""
    # Total counts
    total_projects = db.query(Project).filter(Project.is_active == True).count()
    total_assignments = db.query(Assignment).filter(Assignment.is_active == True).count()
    total_candidates = db.query(User).filter(User.role == "candidate").count()
    total_reviewers = db.query(User).filter(User.role == "reviewer").count()
    
    # Assignment statistics
    total_assigned = db.query(CandidateAssignment).count()
    completed_assignments = db.query(CandidateAssignment).filter(
        CandidateAssignment.status == "completed"
    ).count()
    in_progress_assignments = db.query(CandidateAssignment).filter(
        CandidateAssignment.status == "in_progress"
    ).count()
    overdue_assignments = db.query(CandidateAssignment).filter(
        and_(
            CandidateAssignment.deadline < datetime.utcnow(),
            CandidateAssignment.status.in_(["assigned", "in_progress"])
        )
    ).count()
    
    # Certificate statistics
    total_certificates = db.query(Certificate).filter(Certificate.is_active == True).count()
    passing_certificates = db.query(Certificate).filter(
        and_(
            Certificate.is_active == True,
            Certificate.score >= 70
        )
    ).count()
    
    # Recent activity (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_assignments = db.query(CandidateAssignment).filter(
        CandidateAssignment.assigned_at >= thirty_days_ago
    ).count()
    recent_completions = db.query(CandidateAssignment).filter(
        and_(
            CandidateAssignment.status == "completed",
            CandidateAssignment.assigned_at >= thirty_days_ago
        )
    ).count()
    
    return {
        "overview": {
            "total_projects": total_projects,
            "total_assignments": total_assignments,
            "total_candidates": total_candidates,
            "total_reviewers": total_reviewers
        },
        "assignments": {
            "total_assigned": total_assigned,
            "completed": completed_assignments,
            "in_progress": in_progress_assignments,
            "overdue": overdue_assignments,
            "completion_rate": round((completed_assignments / total_assigned * 100) if total_assigned > 0 else 0, 2)
        },
        "certificates": {
            "total_issued": total_certificates,
            "passing": passing_certificates,
            "pass_rate": round((passing_certificates / total_certificates * 100) if total_certificates > 0 else 0, 2)
        },
        "recent_activity": {
            "new_assignments_30d": recent_assignments,
            "completions_30d": recent_completions
        }
    }


@router.get("/assignments/analytics")
async def get_assignment_analytics(
    project_id: Optional[UUID] = Query(None),
    skillset: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get assignment analytics"""
    query = db.query(CandidateAssignment).join(Assignment)
    
    if project_id:
        query = query.filter(Assignment.project_id == project_id)
    if skillset:
        query = query.filter(Assignment.skillsets.contains([skillset]))
    if start_date:
        query = query.filter(CandidateAssignment.assigned_at >= start_date)
    if end_date:
        query = query.filter(CandidateAssignment.assigned_at <= end_date)
    
    assignments = query.all()
    
    # Calculate statistics
    total = len(assignments)
    status_counts = {}
    difficulty_counts = {}
    avg_completion_time = 0
    completion_times = []
    
    for assignment in assignments:
        # Status counts
        status = assignment.status
        status_counts[status] = status_counts.get(status, 0) + 1
        
        # Difficulty counts
        difficulty = assignment.assignment.difficulty_level
        difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1
        
        # Completion time for completed assignments
        if assignment.status == "completed":
            completion_time = (assignment.assigned_at - assignment.assigned_at).days
            completion_times.append(completion_time)
    
    if completion_times:
        avg_completion_time = sum(completion_times) / len(completion_times)
    
    return {
        "total_assignments": total,
        "status_distribution": status_counts,
        "difficulty_distribution": difficulty_counts,
        "average_completion_time_days": round(avg_completion_time, 2),
        "completion_rate": round((status_counts.get("completed", 0) / total * 100) if total > 0 else 0, 2)
    }


@router.get("/candidates/performance")
async def get_candidate_performance(
    skillset: Optional[str] = Query(None),
    min_assignments: int = Query(1, ge=1),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get candidate performance analytics"""
    # Get candidates with their assignment history
    query = db.query(User).filter(User.role == "candidate")
    
    if skillset:
        query = query.filter(User.skillsets.contains([skillset]))
    
    candidates = query.all()
    
    performance_data = []
    for candidate in candidates:
        assignments = candidate.assigned_assignments
        
        if len(assignments) < min_assignments:
            continue
        
        completed = [ca for ca in assignments if ca.status == "completed"]
        total_score = 0
        certificates_count = 0
        
        # Calculate average score from certificates
        certificates = db.query(Certificate).filter(
            Certificate.candidate_id == candidate.id
        ).all()
        
        for cert in certificates:
            total_score += cert.score or 0
            certificates_count += 1
        
        avg_score = total_score / certificates_count if certificates_count > 0 else 0
        
        performance_data.append({
            "candidate_id": candidate.id,
            "candidate_name": candidate.full_name,
            "candidate_email": candidate.email,
            "total_assignments": len(assignments),
            "completed_assignments": len(completed),
            "completion_rate": round((len(completed) / len(assignments) * 100) if assignments else 0, 2),
            "average_score": round(avg_score, 2),
            "certificates_earned": certificates_count,
            "skillsets": candidate.skillsets
        })
    
    # Sort by average score
    performance_data.sort(key=lambda x: x["average_score"], reverse=True)
    
    return {
        "total_candidates": len(performance_data),
        "top_performers": performance_data[:10],
        "performance_data": performance_data
    }


@router.get("/projects/summary")
async def get_projects_summary(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get projects summary with assignment statistics"""
    projects = db.query(Project).filter(Project.is_active == True).all()
    
    project_summary = []
    for project in projects:
        assignments = project.assignments
        total_assignments = len(assignments)
        
        # Count assignments by status
        assigned_count = 0
        completed_count = 0
        in_progress_count = 0
        
        for assignment in assignments:
            candidate_assignments = assignment.candidate_assignments
            assigned_count += len(candidate_assignments)
            completed_count += len([ca for ca in candidate_assignments if ca.status == "completed"])
            in_progress_count += len([ca for ca in candidate_assignments if ca.status == "in_progress"])
        
        project_summary.append({
            "project_id": project.id,
            "project_name": project.name,
            "domain": project.domain,
            "difficulty_level": project.difficulty_level,
            "total_assignments": total_assignments,
            "assigned_count": assigned_count,
            "completed_count": completed_count,
            "in_progress_count": in_progress_count,
            "completion_rate": round((completed_count / assigned_count * 100) if assigned_count > 0 else 0, 2)
        })
    
    return {
        "total_projects": len(project_summary),
        "projects": project_summary
    }


@router.get("/export/candidates")
async def export_candidates_report(
    format: str = Query("csv", regex="^(csv|json)$"),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Export candidates report"""
    candidates = db.query(User).filter(User.role == "candidate").all()
    
    report_data = []
    for candidate in candidates:
        assignments = candidate.assigned_assignments
        completed = [ca for ca in assignments if ca.status == "completed"]
        certificates = db.query(Certificate).filter(Certificate.candidate_id == candidate.id).count()
        
        report_data.append({
            "id": str(candidate.id),
            "name": candidate.full_name,
            "email": candidate.email,
            "skillsets": ", ".join(candidate.skillsets),
            "total_assignments": len(assignments),
            "completed_assignments": len(completed),
            "certificates_earned": certificates,
            "completion_rate": round((len(completed) / len(assignments) * 100) if assignments else 0, 2),
            "created_at": candidate.created_at.isoformat() if candidate.created_at else None
        })
    
    if format == "csv":
        # Return CSV format
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=report_data[0].keys())
        writer.writeheader()
        writer.writerows(report_data)
        
        return {
            "format": "csv",
            "data": output.getvalue(),
            "filename": f"candidates_report_{datetime.utcnow().strftime('%Y%m%d')}.csv"
        }
    else:
        return {
            "format": "json",
            "data": report_data,
            "total_candidates": len(report_data)
        } 