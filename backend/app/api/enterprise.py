from fastapi import APIRouter

from app.models.enterprise import EnterpriseCaseSnapshot
from app.services.enterprise_service import (
    get_case_enterprise_snapshot,
    get_enterprise_summary,
    load_audit_events,
    load_evidence_records,
    load_users,
)


router = APIRouter(prefix="/enterprise", tags=["Enterprise Command Center"])


@router.get("/users")
def get_users():
    return load_users()


@router.get("/evidence")
def get_evidence_records():
    return load_evidence_records()


@router.get("/audit-events")
def get_audit_events():
    return load_audit_events()


@router.get("/summary")
def get_summary():
    return get_enterprise_summary()


@router.get("/cases/{case_id}/snapshot", response_model=EnterpriseCaseSnapshot)
def get_case_snapshot(case_id: str) -> EnterpriseCaseSnapshot:
    return get_case_enterprise_snapshot(case_id)
