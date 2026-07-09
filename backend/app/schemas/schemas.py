from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# Auth / User Schemas
class AdvisorBase(BaseModel):
    name: str
    email: EmailStr
    team_id: Optional[str] = None
    organization_id: str

class AdvisorCreate(AdvisorBase):
    pass

class AdvisorResponse(AdvisorBase):
    id: str
    created_at: datetime
    class Config:
        from_attributes = True

# Org / Team Schemas
class TeamResponse(BaseModel):
    id: str
    name: str
    organization_id: str
    team_leader_id: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True

# Ingestion Schemas
class CallUploadResponse(BaseModel):
    call_id: str
    filename: str
    status: str
    message: str

class TranscriptSegmentResponse(BaseModel):
    id: str
    speaker: str
    start_time: float
    end_time: float
    text: str
    redacted_text: str
    class Config:
        from_attributes = True

class ScoreResponse(BaseModel):
    needs_discovery: float
    rapport: float
    product_knowledge: float
    objection_handling: float
    compliance: float
    trial_booking: float
    closing: float
    overall_score: float
    comments: Optional[str] = None
    class Config:
        from_attributes = True

class IssueResponse(BaseModel):
    id: str
    issue_type: str
    severity: str
    timestamp: float
    quote: str
    reason: str
    status: str
    class Config:
        from_attributes = True

# Appeal Schemas
class AppealCreate(BaseModel):
    issue_id: str
    reason: str

class AppealReview(BaseModel):
    status: str # approved, rejected
    reviewer_notes: str

class AppealResponse(BaseModel):
    id: str
    issue_id: str
    advisor_id: str
    reason: str
    status: str
    reviewer_notes: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True

class CallDetailResponse(BaseModel):
    id: str
    filename: str
    duration: Optional[float] = None
    status: str
    advisor_name: str
    advisor_id: str
    team_name: str
    team_id: str
    customer_name: Optional[str] = None
    source: str
    created_at: datetime
    summary: Optional[str] = None
    recommendations: Optional[str] = None
    overall_score: Optional[float] = None
    segments: List[TranscriptSegmentResponse] = []
    scores: List[ScoreResponse] = []
    issues: List[IssueResponse] = []
    class Config:
        from_attributes = True
