from fastapi import APIRouter

from app.api.cases import router as cases_router
from app.api.uipath import router as uipath_router
from app.api.workflow import router as workflow_router

router = APIRouter()

router.include_router(cases_router)
router.include_router(workflow_router)
router.include_router(uipath_router)


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "certflow-ai-backend",
    }
