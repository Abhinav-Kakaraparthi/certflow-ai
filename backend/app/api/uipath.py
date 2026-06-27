from fastapi import APIRouter, HTTPException

from app.models.human_review import HumanReviewRequest
from app.services.case_data_service import get_certification_case
from app.services.human_review_service import process_human_review
from app.services.uipath_payload_service import build_uipath_case_payload
from app.workflows.certification_case_workflow import CertificationCaseWorkflow

router = APIRouter(prefix="/uipath", tags=["UiPath Integration"])


@router.post("/cases/{case_id}/start")
def start_uipath_certification_case(case_id: str):
    try:
        case = get_certification_case(case_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

    workflow = CertificationCaseWorkflow()
    result = workflow.run(case)

    return build_uipath_case_payload(result)


@router.post("/cases/{case_id}/human-review")
def submit_human_review(case_id: str, review: HumanReviewRequest):
    try:
        get_certification_case(case_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

    return process_human_review(case_id=case_id, review=review)
