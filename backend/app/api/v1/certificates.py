from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
import uuid

from ...core.database import get_db
from ...core.security import get_current_active_user, require_admin
from ...models.user import User
from ...models.certificate import Certificate
from ...models.candidate_assignment import CandidateAssignment
from ...models.review import Review
from ...services.certificate_service import generate_certificate_pdf

router = APIRouter()


@router.post("/generate/{candidate_assignment_id}")
async def generate_certificate(
    candidate_assignment_id: UUID,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Generate a certificate for a completed assignment"""
    # Check if candidate assignment exists and is completed
    candidate_assignment = db.query(CandidateAssignment).filter(
        CandidateAssignment.id == candidate_assignment_id,
        CandidateAssignment.status == "completed"
    ).first()
    
    if not candidate_assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Completed assignment not found"
        )
    
    # Check if certificate already exists
    existing_certificate = db.query(Certificate).filter(
        Certificate.candidate_id == candidate_assignment.candidate_id,
        Certificate.assignment_id == candidate_assignment.assignment_id
    ).first()
    
    if existing_certificate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Certificate already exists for this assignment"
        )
    
    # Get the best review score
    reviews = db.query(Review).join(Submission).filter(
        Submission.candidate_assignment_id == candidate_assignment_id
    ).all()
    
    if not reviews:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No reviews found for this assignment"
        )
    
    # Get the highest score
    best_score = max(review.score for review in reviews if review.score is not None)
    
    # Generate certificate number
    certificate_number = f"CERT-{uuid.uuid4().hex[:8].upper()}"
    
    # Generate PDF
    try:
        pdf_url = await generate_certificate_pdf(
            candidate=candidate_assignment.candidate,
            assignment=candidate_assignment.assignment,
            score=best_score,
            certificate_number=certificate_number
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate certificate PDF: {str(e)}"
        )
    
    # Create certificate record
    certificate = Certificate(
        candidate_id=candidate_assignment.candidate_id,
        assignment_id=candidate_assignment.assignment_id,
        certificate_number=certificate_number,
        score=best_score,
        skills_demonstrated=candidate_assignment.assignment.skillsets,
        pdf_url=pdf_url
    )
    
    db.add(certificate)
    db.commit()
    db.refresh(certificate)
    
    return {
        "message": "Certificate generated successfully",
        "certificate_id": certificate.id,
        "certificate_number": certificate_number,
        "pdf_url": pdf_url
    }


@router.get("/", response_model=List[dict])
async def get_certificates(
    candidate_id: Optional[UUID] = Query(None),
    assignment_id: Optional[UUID] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get certificates with optional filtering"""
    query = db.query(Certificate).join(User).join(Assignment)
    
    # Filter by candidate if specified
    if candidate_id:
        if current_user.role == "candidate" and current_user.id != candidate_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Can only view own certificates"
            )
        query = query.filter(Certificate.candidate_id == candidate_id)
    elif current_user.role == "candidate":
        query = query.filter(Certificate.candidate_id == current_user.id)
    
    if assignment_id:
        query = query.filter(Certificate.assignment_id == assignment_id)
    
    certificates = query.offset(skip).limit(limit).all()
    
    result = []
    for cert in certificates:
        result.append({
            "id": cert.id,
            "certificate_number": cert.certificate_number,
            "candidate_name": cert.candidate.full_name,
            "candidate_email": cert.candidate.email,
            "assignment_title": cert.assignment.title,
            "project_name": cert.assignment.project.name,
            "score": cert.score,
            "skills_demonstrated": cert.skills_demonstrated,
            "issued_at": cert.issued_at,
            "pdf_url": cert.pdf_url,
            "is_passing": cert.is_passing_score
        })
    
    return result


@router.get("/{certificate_id}")
async def get_certificate(
    certificate_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific certificate"""
    certificate = db.query(Certificate).filter(Certificate.id == certificate_id).first()
    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found"
        )
    
    # Check permissions
    if current_user.role == "candidate" and certificate.candidate_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only view own certificates"
        )
    
    return {
        "id": certificate.id,
        "certificate_number": certificate.certificate_number,
        "candidate_name": certificate.candidate.full_name,
        "candidate_email": certificate.candidate.email,
        "assignment_title": certificate.assignment.title,
        "project_name": certificate.assignment.project.name,
        "score": certificate.score,
        "skills_demonstrated": certificate.skills_demonstrated,
        "issued_at": certificate.issued_at,
        "pdf_url": certificate.pdf_url,
        "is_passing": certificate.is_passing_score
    }


@router.delete("/{certificate_id}")
async def delete_certificate(
    certificate_id: UUID,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Delete a certificate (soft delete)"""
    certificate = db.query(Certificate).filter(Certificate.id == certificate_id).first()
    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found"
        )
    
    certificate.is_active = False
    db.commit()
    
    return {"message": "Certificate deleted successfully"}


@router.get("/verify/{certificate_number}")
async def verify_certificate(
    certificate_number: str,
    db: Session = Depends(get_db)
):
    """Verify a certificate by number (public endpoint)"""
    certificate = db.query(Certificate).filter(
        Certificate.certificate_number == certificate_number,
        Certificate.is_active == True
    ).first()
    
    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found or invalid"
        )
    
    return {
        "valid": True,
        "certificate_number": certificate.certificate_number,
        "candidate_name": certificate.candidate.full_name,
        "assignment_title": certificate.assignment.title,
        "project_name": certificate.assignment.project.name,
        "score": certificate.score,
        "issued_at": certificate.issued_at,
        "is_passing": certificate.is_passing_score
    } 