import uuid
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class Organization(Base):
    __tablename__ = "organizations"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    teams = relationship("Team", back_populates="organization", cascade="all, delete-orphan")
    advisors = relationship("Advisor", back_populates="organization", cascade="all, delete-orphan")
    calls = relationship("Call", back_populates="organization", cascade="all, delete-orphan")

class Team(Base):
    __tablename__ = "teams"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    team_leader_id = Column(String(36), nullable=True) # ID of Advisor who is the TL
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    organization = relationship("Organization", back_populates="teams")
    advisors = relationship("Advisor", back_populates="team", foreign_keys="[Advisor.team_id]", cascade="all, delete-orphan")
    calls = relationship("Call", back_populates="team", cascade="all, delete-orphan")

class Advisor(Base):
    __tablename__ = "advisors"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    team_id = Column(String(36), ForeignKey("teams.id", ondelete="SET NULL"), nullable=True)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    organization = relationship("Organization", back_populates="advisors")
    team = relationship("Team", back_populates="advisors", foreign_keys=[team_id])
    calls = relationship("Call", back_populates="advisor", cascade="all, delete-orphan")

class Customer(Base):
    __tablename__ = "customers"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    calls = relationship("Call", back_populates="customer")

class Call(Base):
    __tablename__ = "calls"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    filename = Column(String(255), nullable=False)
    duration = Column(Float, nullable=True) # in seconds
    status = Column(String(50), default="processing") # processing, completed, failed
    error_message = Column(Text, nullable=True)
    
    advisor_id = Column(String(36), ForeignKey("advisors.id", ondelete="CASCADE"), nullable=False)
    customer_id = Column(String(36), ForeignKey("customers.id", ondelete="SET NULL"), nullable=True)
    team_id = Column(String(36), ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    
    source = Column(String(50), default="upload") # upload, folder, twilio, crm
    audio_path = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Aggregated analysis results
    transcript_text = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    recommendations = Column(Text, nullable=True)
    overall_score = Column(Float, nullable=True)
    
    organization = relationship("Organization", back_populates="calls")
    team = relationship("Team", back_populates="calls")
    advisor = relationship("Advisor", back_populates="calls")
    customer = relationship("Customer", back_populates="calls")
    
    segments = relationship("TranscriptSegment", back_populates="call", cascade="all, delete-orphan")
    scores = relationship("Score", back_populates="call", cascade="all, delete-orphan")
    issues = relationship("Issue", back_populates="call", cascade="all, delete-orphan")
    logs = relationship("ProcessingLog", back_populates="call", cascade="all, delete-orphan")

class TranscriptSegment(Base):
    __tablename__ = "transcript_segments"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    call_id = Column(String(36), ForeignKey("calls.id", ondelete="CASCADE"), nullable=False)
    speaker = Column(String(50), nullable=False) # Advisor, Customer
    start_time = Column(Float, nullable=False) # seconds
    end_time = Column(Float, nullable=False) # seconds
    text = Column(Text, nullable=False)
    redacted_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    call = relationship("Call", back_populates="segments")

class Score(Base):
    __tablename__ = "scores"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    call_id = Column(String(36), ForeignKey("calls.id", ondelete="CASCADE"), nullable=False)
    needs_discovery = Column(Float, nullable=False)
    rapport = Column(Float, nullable=False)
    product_knowledge = Column(Float, nullable=False)
    objection_handling = Column(Float, nullable=False)
    compliance = Column(Float, nullable=False)
    trial_booking = Column(Float, nullable=False)
    closing = Column(Float, nullable=False)
    overall_score = Column(Float, nullable=False)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    call = relationship("Call", back_populates="scores")

class Issue(Base):
    __tablename__ = "issues"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    call_id = Column(String(36), ForeignKey("calls.id", ondelete="CASCADE"), nullable=False)
    issue_type = Column(String(100), nullable=False) # no_needs_discovery, pressure_selling, etc.
    severity = Column(String(20), nullable=False) # low, medium, high
    timestamp = Column(Float, nullable=False) # start timestamp in call
    quote = Column(Text, nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(String(50), default="active") # active, appealed, resolved_approved, resolved_rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    call = relationship("Call", back_populates="issues")
    appeal = relationship("Appeal", uselist=False, back_populates="issue", cascade="all, delete-orphan")

class Appeal(Base):
    __tablename__ = "appeals"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    issue_id = Column(String(36), ForeignKey("issues.id", ondelete="CASCADE"), unique=True, nullable=False)
    advisor_id = Column(String(36), ForeignKey("advisors.id", ondelete="CASCADE"), nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(String(50), default="pending") # pending, approved, rejected
    reviewer_id = Column(String(36), nullable=True) # ID of Advisor/TL reviewing
    reviewer_notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    issue = relationship("Issue", back_populates="appeal")

class ProcessingLog(Base):
    __tablename__ = "processing_logs"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    call_id = Column(String(36), ForeignKey("calls.id", ondelete="CASCADE"), nullable=False)
    stage = Column(String(100), nullable=False) # ingestion, transcription, diarization, redaction, analysis, completed
    status = Column(String(50), nullable=False) # running, completed, failed
    message = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    call = relationship("Call", back_populates="logs")
