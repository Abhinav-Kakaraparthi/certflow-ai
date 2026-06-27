from fastapi import APIRouter, HTTPException

from app.services.case_data_service import (
    get_certification_case,
    load_certification_cases,
)

router = APIRouter(prefix="/cases", tags=["Certification Cases"])


@router.get("")
def list_cases():
    return load_certification_cases()


@router.get("/{case_id}")
def get_case(case_id: str):
    try:
        return get_certification_case(case_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
