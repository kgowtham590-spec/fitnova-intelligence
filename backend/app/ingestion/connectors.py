import os
import shutil
from abc import ABC, abstractmethod
from app.database.models import Call

class AbstractConnector(ABC):
    @abstractmethod
    def ingest(self, source_path_or_payload: str, **kwargs) -> dict:
        pass

class FolderConnector(AbstractConnector):
    def __init__(self, upload_dir: str):
        self.upload_dir = upload_dir

    def ingest(self, source_path: str, **kwargs) -> dict:
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Source file not found: {source_path}")
        
        filename = os.path.basename(source_path)
        dest_path = os.path.join(self.upload_dir, filename)
        shutil.copy(source_path, dest_path)
        
        return {
            "filename": filename,
            "audio_path": dest_path,
            "source": "folder"
        }

class TwilioConnector(AbstractConnector):
    def ingest(self, payload: dict, **kwargs) -> dict:
        recording_url = payload.get("RecordingUrl")
        call_sid = payload.get("CallSid")
        filename = f"twilio_{call_sid}.mp3"
        dest_path = os.path.join(kwargs.get("upload_dir", "./data/uploads"), filename)
        
        with open(dest_path, "wb") as f:
            f.write(b"MOCK_TWILIO_AUDIO_DATA")
            
        return {
            "filename": filename,
            "audio_path": dest_path,
            "source": "twilio"
        }

class CRMConnector(AbstractConnector):
    def ingest(self, payload: dict, **kwargs) -> dict:
        filename = payload.get("filename", "crm_call.wav")
        audio_url = payload.get("audio_url")
        dest_path = os.path.join(kwargs.get("upload_dir", "./data/uploads"), filename)
        
        with open(dest_path, "wb") as f:
            f.write(b"MOCK_CRM_AUDIO_DATA")
            
        return {
            "filename": filename,
            "audio_path": dest_path,
            "source": "crm"
        }
