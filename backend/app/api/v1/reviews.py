from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from ...core.database import get_db
from ...core.security import get_current_active_user, require_reviewer_or_admin
from ...models.user import User
from ...models.review import Review
from ...models.submission import Submission
from ...models.candidate_assignment import CandidateAssignment

router = APIRouter()


@router.post("/submissions/{submission_id}/review")
async def create_review(
    submission_id: UUID,
    score: int,
    feedback: str,
    criteria_scores: Optional[dict] = None,
    current_user: User = Depends(require_reviewer_or_admin),
    db: Session = Depends(get_db)
):
    """Create a review for a submission"""
    # Check if submission exists
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )
    
    # Check if already reviewed by this reviewer
    existing_review = db.query(Review).filter(
        Review.submission_id == submission_id,
        Review.reviewer_id == current_user.id
    ).first()
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already reviewed this submission"
        )
    
    # Validate score
    if not 0 <= score <= 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Score must be between 0 and 100"
        )
    
    # Create review
    review = Review(
        submission_id=submission_id,
        reviewer_id=current_user.id,
        score=score,
        feedback=feedback,
        criteria_scores=criteria_scores or {},
        status="completed"
    )
    
    db.add(review)
    
    # Update submission status
    submission.status = "reviewed"
    
    # Update candidate assignment status if score is passing
    if score >= 70:
        candidate_assignment = submission.candidate_assignment
        candidate_assignment.status = "completed"
    
    db.commit()
    db.refresh(review)
    
    return {
        "message": "Review submitted successfully",
        "review_id": review.id,
        "score": score
    }


@router.get("/submissions/{submission_id}/reviews")
async def get_submission_reviews(
    submission_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all reviews for a submission"""
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )
    
    # Check permissions
    if current_user.role == "candidate":
        candidate_assignment = submission.candidate_assignment
        if candidate_assignment.candidate_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Can only view reviews for own submissions"
            )
    
    reviews = db.query(Review).filter(Review.submission_id == submission_id).all()
    
    result = []
    for review in reviews:
        result.append({
            "id": review.id,
            "reviewer_name": review.reviewer.full_name,
            "score": review.score,
            "feedback": review.feedback,
            "criteria_scores": review.criteria_scores,
            "reviewed_at": review.reviewed_at,
            "status": review.status
        })
    
    return result


@router.get("/pending")
async def get_pending_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(require_reviewer_or_admin),
    db: Session = Depends(get_db)
):
    """Get pending reviews for the current reviewer"""
    # Get submissions that need review
    pending_submissions = db.query(Submission).filter(
        Submission.status == "submitted"
    ).join(CandidateAssignment).join(User).all()
    
    result = []
    for submission in pending_submissions:
        # Check if current user already reviewed this submission
        existing_review = db.query(Review).filter(
            Review.submission_id == submission.id,
            Review.reviewer_id == current_user.id
        ).first()
        
        if not existing_review:
            result.append({
                "submission_id": submission.id,
                "candidate_name": submission.candidate_assignment.candidate.full_name,
                "candidate_email": submission.candidate_assignment.candidate.email,
                "assignment_title": submission.candidate_assignment.assignment.title,
                "project_name": submission.candidate_assignment.assignment.project.name,
                "submission_type": submission.submission_type,
                "submitted_at": submission.submitted_at,
                "notes": submission.notes
            })
    
    return result[skip:skip + limit]


@router.put("/{review_id}")
async def update_review(
    review_id: UUID,
    score: Optional[int] = None,
    feedback: Optional[str] = None,
    criteria_scores: Optional[dict] = None,
    current_user: User = Depends(require_reviewer_or_admin),
    db: Session = Depends(get_db)
):
    """Update a review (only by the original reviewer)"""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    # Check if current user is the reviewer
    if review.reviewer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only update own reviews"
        )
    
    # Update fields
    if score is not None:
        if not 0 <= score <= 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Score must be between 0 and 100"
            )
        review.score = score
    
    if feedback is not None:
        review.feedback = feedback
    
    if criteria_scores is not None:
        review.criteria_scores = criteria_scores
    
    db.commit()
    db.refresh(review)
    
    return {"message": "Review updated successfully"}


@router.get("/stats")
async def get_review_stats(
    current_user: User = Depends(require_reviewer_or_admin),
    db: Session = Depends(get_db)
):
    """Get review statistics for the current user"""
    total_reviews = db.query(Review).filter(Review.reviewer_id == current_user.id).count()
    completed_reviews = db.query(Review).filter(
        Review.reviewer_id == current_user.id,
        Review.status == "completed"
    ).count()
    
    # Average score
    avg_score = db.query(Review.score).filter(
        Review.reviewer_id == current_user.id,
        Review.status == "completed"
    ).all()
    avg_score = sum([r[0] for r in avg_score]) / len(avg_score) if avg_score else 0
    
    return {
        "total_reviews": total_reviews,
        "completed_reviews": completed_reviews,
        "pending_reviews": total_reviews - completed_reviews,
        "average_score": round(avg_score, 2)
    } 