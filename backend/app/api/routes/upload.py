import os
import shutil
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import Call, Advisor, Team, Customer, TranscriptSegment, Score, Issue, ProcessingLog
from app.services.transcription import TranscriptionService
from app.services.diarization import DiarizationService
from app.services.redaction import RedactionService
from app.agents.graph import CallAnalysisWorkflow
from app.core.config import settings

router = APIRouter()

transcription_service = TranscriptionService()
diarization_service = DiarizationService()
redaction_service = RedactionService()
analysis_workflow = CallAnalysisWorkflow()

def process_call_pipeline(call_id: str, db_session_factory):
    db = db_session_factory()
    try:
        call = db.query(Call).filter(Call.id == call_id).first()
        if not call:
            return
            
        def log_stage(stage, status, message=None):
            log = ProcessingLog(call_id=call_id, stage=stage, status=status, message=message)
            db.add(log)
            db.commit()
            
        log_stage("transcription", "running", "Starting audio transcription")
        raw_segments = transcription_service.transcribe(call.audio_path)
        log_stage("transcription", "completed", f"Transcribed {len(raw_segments)} segments")
        
        log_stage("diarization", "running", "Performing speaker diarization")
        diarized_segments = diarization_service.diarize(call.audio_path, raw_segments)
        log_stage("diarization", "completed", "Speakers identified as Advisor/Customer")
        
        log_stage("redaction", "running", "Redacting PII (Email, Phone, UPI, Cards)")
        full_transcript = []
        for seg in diarized_segments:
            redacted_text = redaction_service.redact(seg["text"])
            db_seg = TranscriptSegment(
                call_id=call_id,
                speaker=seg["speaker"],
                start_time=seg["start"],
                end_time=seg["end"],
                text=seg["text"],
                redacted_text=redacted_text
            )
            db.add(db_seg)
            full_transcript.append(f"{seg['speaker']}: {redacted_text}")
            
        db.commit()
        transcript_text = "\n".join(full_transcript)
        call.transcript_text = transcript_text
        log_stage("redaction", "completed", "PII redaction applied and transcript saved")
        
        log_stage("analysis", "running", "Running AI Analysis Engine (LangGraph)")
        analysis = analysis_workflow.run_analysis(transcript_text)
        
        s = analysis["scores"]
        db_score = Score(
            call_id=call_id,
            needs_discovery=s["needs_discovery"],
            rapport=s["rapport"],
            product_knowledge=s["product_knowledge"],
            objection_handling=s["objection_handling"],
            compliance=s["compliance"],
            trial_booking=s["trial_booking"],
            closing=s["closing"],
            overall_score=s["overall_score"],
            comments=s.get("comments", "")
        )
        db.add(db_score)
        
        for issue in analysis["issues"]:
            db_issue = Issue(
                call_id=call_id,
                issue_type=issue["issue_type"],
                severity=issue["severity"],
                timestamp=issue["timestamp"],
                quote=issue["quote"],
                reason=issue["reason"],
                status="active"
            )
            db.add(db_issue)
            
        call.summary = analysis["summary"]
        call.recommendations = analysis["recommendations"]
        call.overall_score = s["overall_score"]
        call.status = "completed"
        db.commit()
        
        log_stage("analysis", "completed", "Analysis, scoring and issue flagging complete")
        
    except Exception as e:
        db.rollback()
        log_stage("analysis", "failed", f"Failed with exception: {str(e)}")
        call = db.query(Call).filter(Call.id == call_id).first()
        if call:
            call.status = "failed"
            call.error_message = str(e)
            db.commit()
    finally:
        db.close()

@router.post("", response_model=dict)
def upload_call(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    advisor_id: str = None,
    db: Session = Depends(get_db)
):
    if not advisor_id:
        adv = db.query(Advisor).first()
        if not adv:
            raise HTTPException(status_code=400, detail="No advisors exist in DB. Run seed data first.")
        advisor_id = adv.id
    else:
        adv = db.query(Advisor).filter(Advisor.id == advisor_id).first()
        if not adv:
            raise HTTPException(status_code=404, detail="Advisor not found")
            
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_id = str(uuid.uuid4())
    filename = f"{file_id}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    new_call = Call(
        id=file_id,
        filename=file.filename,
        advisor_id=advisor_id,
        team_id=adv.team_id,
        organization_id=adv.organization_id,
        source="upload",
        audio_path=file_path,
        status="processing"
    )
    db.add(new_call)
    db.commit()
    db.refresh(new_call)
    
    from app.database.session import SessionLocal
    background_tasks.add_task(process_call_pipeline, new_call.id, SessionLocal)
    
    return {
        "call_id": new_call.id,
        "filename": new_call.filename,
        "status": "processing",
        "message": "Call queued for processing"
    }
