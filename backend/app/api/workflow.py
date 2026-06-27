from fastapi import APIRouter, HTTPException

from app.services.case_data_service import (
    get_certification_case,
    load_certification_cases,
)
from app.workflows.certification_case_workflow import CertificationCaseWorkflow

router = APIRouter(prefix="/workflow", tags=["Agentic Certification Workflow"])


@router.post("/cases/{case_id}/run")
def run_certification_case(case_id: str):
    try:
        case = get_certification_case(case_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

    workflow = CertificationCaseWorkflow()
    return workflow.run(case)


@router.post("/cases/run-all")
def run_all_certification_cases():
    workflow = CertificationCaseWorkflow()
    cases = load_certification_cases()

    return [workflow.run(case) for case in cases]
