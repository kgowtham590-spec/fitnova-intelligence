from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.routes import calls, org, appeals, upload
from app.database.session import engine, Base

setup_logging()
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix=f"{settings.API_V1_STR}/upload", tags=["Upload"])
app.include_router(calls.router, prefix=f"{settings.API_V1_STR}/calls", tags=["Calls"])
app.include_router(appeals.router, prefix=f"{settings.API_V1_STR}/appeals", tags=["Appeals"])
app.include_router(org.router, prefix=f"{settings.API_V1_STR}/org", tags=["Organization"])

@app.get("/health")
def health_check():
    return {"status": "healthy", "project": settings.PROJECT_NAME}
