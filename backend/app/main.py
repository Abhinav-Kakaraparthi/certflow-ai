from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

app = FastAPI(
    title="CertFlow AI",
    description="Agentic aerospace certification case management system built for UiPath AgentHack.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.get("/")
def root():
    return {
        "name": "CertFlow AI",
        "status": "running",
        "track": "UiPath Maestro Case",
    }

@app.get("/health")
def root_health_check():
    return {
        "status": "healthy",
        "service": "CertFlow AI API",
        "platform": "Render"
    }


@app.get("/api/health")
def api_health_check():
    return {
        "status": "healthy",
        "service": "CertFlow AI API",
        "platform": "Render"
    }
