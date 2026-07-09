import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import Optional

# Resolve the backend directory
_HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load backend/.env
load_dotenv(os.path.join(_HERE, ".env"))

_DEFAULT_DB = f"sqlite:///{_HERE}/fitnova.db"

class Settings(BaseSettings):
    PROJECT_NAME: str = "FitNova AI Sales Call Intelligence System"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = os.getenv("DATABASE_URL", _DEFAULT_DB)
    
    # LLM API Config
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY", None)
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    
    # Transcription/Diarization Config
    HF_TOKEN: Optional[str] = os.getenv("HF_TOKEN", None)
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./data/uploads")
    
    class Config:
        case_sensitive = True

settings = Settings()
