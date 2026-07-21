from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import Appeal, Issue
from app.schemas.schemas import AppealCreate, AppealReview, AppealResponse

router = APIRouter()

@router.post("", response_model=AppealResponse)
def create_appeal(appeal_in: AppealCreate, db: Session = Depends(get_db)):
    issue = db.query(Issue).filter(Issue.id == appeal_in.issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
        
    existing = db.query(Appeal).filter(Appeal.issue_id == appeal_in.issue_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Appeal already exists for this issue")
        
    call = issue.call
    appeal = Appeal(
        issue_id=appeal_in.issue_id,
        advisor_id=call.advisor_id,
        reason=appeal_in.reason,
        status="pending"
    )
    issue.status = "appealed"
    db.add(appeal)
    db.commit()
    db.refresh(appeal)
    return appeal

@router.get("", response_model=list[AppealResponse])
def get_appeals(db: Session = Depends(get_db)):
    return db.query(Appeal).all()

@router.put("/{appeal_id}", response_model=AppealResponse)
def review_appeal(appeal_id: str, review_in: AppealReview, db: Session = Depends(get_db)):
    appeal = db.query(Appeal).filter(Appeal.id == appeal_id).first()
    if not appeal:
        raise HTTPException(status_code=404, detail="Appeal not found")
        
    appeal.status = review_in.status
    appeal.reviewer_notes = review_in.reviewer_notes
    
    issue = db.query(Issue).filter(Issue.id == appeal.issue_id).first()
    if issue:
        if review_in.status == "approved":
            issue.status = "resolved_approved"
        else:
            issue.status = "resolved_rejected"
            
    db.commit()
    db.refresh(appeal)
    return appeal
