from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.session import get_db
from app.database.models import Team, Advisor, Call, Issue, Organization, Score
from app.core.config import settings
from typing import List

router = APIRouter()

@router.get("/structure")
def get_org_structure(db: Session = Depends(get_db)):
    teams = db.query(Team).all()
    results = []
    for t in teams:
        advisors = db.query(Advisor).filter(Advisor.team_id == t.id).all()
        results.append({
            "team_id": t.id,
            "team_name": t.name,
            "advisors": [{"id": a.id, "name": a.name, "email": a.email} for a in advisors]
        })
    return results

@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    avg_scores = db.query(
        func.avg(Score.needs_discovery).label("needs_discovery"),
        func.avg(Score.rapport).label("rapport"),
        func.avg(Score.product_knowledge).label("product_knowledge"),
        func.avg(Score.objection_handling).label("objection_handling"),
        func.avg(Score.compliance).label("compliance"),
        func.avg(Score.trial_booking).label("trial_booking"),
        func.avg(Score.closing).label("closing"),
        func.avg(Score.overall_score).label("overall")
    ).first()
    
    issues_by_type = db.query(
        Issue.issue_type,
        func.count(Issue.id).label("count")
    ).group_by(Issue.issue_type).all()
    
    team_rankings = db.query(
        Team.name,
        func.avg(Call.overall_score).label("avg_score")
    ).join(Call, Call.team_id == Team.id).filter(Call.status == "completed").group_by(Team.name).all()
    
    advisor_rankings = db.query(
        Advisor.name,
        func.avg(Call.overall_score).label("avg_score")
    ).join(Call, Call.advisor_id == Advisor.id).filter(Call.status == "completed").group_by(Advisor.name).all()
    
    severity_breakdown = db.query(
        Issue.severity,
        func.count(Issue.id).label("count")
    ).group_by(Issue.severity).all()

    return {
        "averages": {
            "needs_discovery": round(avg_scores.needs_discovery or 0.0, 2),
            "rapport": round(avg_scores.rapport or 0.0, 2),
            "product_knowledge": round(avg_scores.product_knowledge or 0.0, 2),
            "objection_handling": round(avg_scores.objection_handling or 0.0, 2),
            "compliance": round(avg_scores.compliance or 0.0, 2),
            "trial_booking": round(avg_scores.trial_booking or 0.0, 2),
            "closing": round(avg_scores.closing or 0.0, 2),
            "overall": round(avg_scores.overall or 0.0, 2)
        },
        "issues_by_type": [{"type": r[0], "count": r[1]} for r in issues_by_type],
        "team_rankings": [{"name": r[0], "score": round(r[1] or 0.0, 2)} for r in team_rankings],
        "advisor_rankings": [{"name": r[0], "score": round(r[1] or 0.0, 2)} for r in advisor_rankings],
        "severity_breakdown": [{"severity": r[0], "count": r[1]} for r in severity_breakdown]
    }

@router.get("/debug")
def debug_config():
    key = settings.GROQ_API_KEY
    if not key:
        return {
            "groq_api_key_configured": False,
            "groq_model": settings.GROQ_MODEL,
            "error": "No Groq API key found in settings"
        }
    
    masked_key = f"{key[:6]}...{key[-4:]}" if len(key) > 10 else "too short"
    
    try:
        from groq import Groq
        client = Groq(api_key=key)
        # Try a quick list models call to verify it works
        models = client.models.list()
        connection_status = "success"
        error_msg = None
    except Exception as e:
        connection_status = "failed"
        error_msg = str(e)

    return {
        "groq_api_key_configured": True,
        "groq_api_key_length": len(key),
        "groq_api_key_masked": masked_key,
        "groq_model": settings.GROQ_MODEL,
        "groq_client_connection": connection_status,
        "groq_client_error": error_msg
    }
