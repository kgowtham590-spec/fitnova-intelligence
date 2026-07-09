from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import Call, Advisor, Team, TranscriptSegment, Score, Issue
from app.schemas.schemas import CallDetailResponse
from typing import List, Optional

router = APIRouter()

@router.get("", response_model=dict)
def get_calls(
    db: Session = Depends(get_db),
    team_id: Optional[str] = Query(None),
    advisor_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    min_score: Optional[float] = Query(None),
    max_score: Optional[float] = Query(None),
    limit: int = 20,
    offset: int = 0
):
    query = db.query(Call)
    if team_id:
        query = query.filter(Call.team_id == team_id)
    if advisor_id:
        query = query.filter(Call.advisor_id == advisor_id)
    if status:
        query = query.filter(Call.status == status)
    if min_score is not None:
        query = query.filter(Call.overall_score >= min_score)
    if max_score is not None:
        query = query.filter(Call.overall_score <= max_score)
        
    total = query.count()
    calls = query.order_by(Call.created_at.desc()).offset(offset).limit(limit).all()
    
    results = []
    for c in calls:
        results.append({
            "id": c.id,
            "filename": c.filename,
            "duration": c.duration,
            "status": c.status,
            "advisor_name": c.advisor.name if c.advisor else "Unknown",
            "team_name": c.team.name if c.team else "Unknown",
            "source": c.source,
            "overall_score": c.overall_score,
            "created_at": c.created_at
        })
        
    return {"total": total, "calls": results}

@router.get("/{call_id}", response_model=CallDetailResponse)
def get_call_detail(call_id: str, db: Session = Depends(get_db)):
    call = db.query(Call).filter(Call.id == call_id).first()
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
        
    return CallDetailResponse(
        id=call.id,
        filename=call.filename,
        duration=call.duration,
        status=call.status,
        advisor_name=call.advisor.name if call.advisor else "Unknown",
        advisor_id=call.advisor_id,
        team_name=call.team.name if call.team else "Unknown",
        team_id=call.team_id,
        customer_name=call.customer.name if call.customer else "Unknown Customer",
        source=call.source,
        created_at=call.created_at,
        summary=call.summary,
        recommendations=call.recommendations,
        overall_score=call.overall_score,
        segments=[s for s in call.segments],
        scores=[s for s in call.scores],
        issues=[i for i in call.issues]
    )
