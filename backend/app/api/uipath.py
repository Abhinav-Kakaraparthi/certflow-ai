from fastapi import APIRouter, HTTPException

from app.models.certification import RiskLevel
from app.models.human_review import HumanReviewRequest
from app.services.ai_reasoning_service import AIReasoningService
from app.services.case_data_service import get_certification_case
from app.services.human_review_service import process_human_review
from app.services.uipath_payload_service import build_uipath_case_payload
from app.workflows.certification_case_workflow import CertificationCaseWorkflow

router = APIRouter(prefix="/uipath", tags=["UiPath Integration"])

ai_reasoning_service = AIReasoningService()


@router.post("/cases/{case_id}/start")
def start_uipath_certification_case(case_id: str):
    try:
        case = get_certification_case(case_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

    workflow = CertificationCaseWorkflow()
    result = workflow.run(case)

    payload = build_uipath_case_payload(result)

    should_run_ai = (
        result.overall_risk == RiskLevel.HIGH
        or result.human_review_required
        or len(result.missing_documents) > 0
    )

    if should_run_ai:
        ai_reasoning = ai_reasoning_service.analyze_case(case)
        payload["ai_reasoning"] = ai_reasoning.model_dump()
    else:
        payload["ai_reasoning"] = {
            "ai_model": "deterministic-low-risk-routing",
            "risk_explanation": "Live AI reasoning was not required because deterministic agents found complete evidence and low certification risk.",
            "certification_concerns": [
                "No missing certification evidence detected.",
                "No high-risk safety, software, structural, or control-logic escalation detected."
            ],
            "missing_evidence_questions": [
                "No evidence questions required for this low-risk case."
            ],
            "recommended_escalation": "Auto approval",
            "confidence_score": 1.0,
            "audit_summary": "Case routed through deterministic low-risk approval to conserve AI quota and preserve scalable orchestration.",
        }

    return payload


@router.post("/cases/{case_id}/human-review")
def submit_human_review(case_id: str, review: HumanReviewRequest):
    try:
        get_certification_case(case_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

    return process_human_review(case_id=case_id, review=review)
