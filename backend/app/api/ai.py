from fastapi import APIRouter, HTTPException

from app.models.ai_reasoning import AIReasoningResult
from app.services.ai_reasoning_service import AIReasoningService
from app.services.case_data_service import get_certification_case


router = APIRouter(prefix="/ai", tags=["AI Reasoning"])

ai_reasoning_service = AIReasoningService()


@router.post("/cases/{case_id}/analyze", response_model=AIReasoningResult)
def analyze_case_with_ai(case_id: str) -> AIReasoningResult:
    try:
        certification_case = get_certification_case(case_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error

    try:
        return ai_reasoning_service.analyze_case(certification_case)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"AI reasoning failed: {str(error)}",
        ) from error
