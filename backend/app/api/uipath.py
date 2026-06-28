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


@router.post("/documents/{document_id}/route")
def route_document_after_workspace_update(document_id: str):
    from fastapi import HTTPException

    from app.services.document_workspace_service import get_workspace_document

    try:
        document = get_workspace_document(document_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error

    if document.status == "blocked":
        next_action = "request_supplier_input"
        assigned_role = "Supplier Evidence Owner"
        maestro_stage = "Evidence Collection"
        task_title = "Request missing supplier evidence"
    elif document.ai_review_status in ["needs_revision", "reviewed_with_concerns"]:
        next_action = "create_ai_review_task"
        assigned_role = document.required_review_role
        maestro_stage = "AI Evidence Review"
        task_title = "Review updated certification evidence"
    elif document.status in ["draft", "in_progress"]:
        next_action = "continue_authoring"
        assigned_role = "Certification Engineer"
        maestro_stage = "Evidence Authoring"
        task_title = "Complete certification artifact"
    else:
        next_action = "advance_to_human_approval"
        assigned_role = document.required_review_role
        maestro_stage = "Human Approval"
        task_title = "Approve certification evidence"

    return {
        "document_id": document.document_id,
        "case_id": document.case_id,
        "artifact_type": document.artifact_type,
        "document_status": document.status,
        "ai_review_status": document.ai_review_status,
        "maestro_stage": maestro_stage,
        "next_uipath_action": next_action,
        "task_title": task_title,
        "assigned_role": assigned_role,
        "routing_reason": (
            f"{document.title} is {document.status} with AI review status "
            f"{document.ai_review_status}. UiPath should route this artifact to "
            f"{assigned_role} for the next certification action."
        ),
        "human_review_required": assigned_role in [
            "DER Reviewer",
            "Certification Manager",
            "Senior Certification Engineer",
        ],
    }
