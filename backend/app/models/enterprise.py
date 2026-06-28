from typing import Optional
from pydantic import BaseModel


class EnterpriseUser(BaseModel):
    user_id: str
    name: str
    role: str
    team: str
    email: str
    access_level: str


class EvidenceRecord(BaseModel):
    evidence_id: str
    case_id: str
    file_name: str
    evidence_type: str
    submitted_by: Optional[str]
    assigned_reviewer: str
    status: str
    submitted_at: Optional[str]
    last_action_by: str


class AuditEvent(BaseModel):
    event_id: str
    case_id: str
    actor_id: str
    actor_role: str
    action: str
    target: str
    timestamp: str
    summary: str


class EnterpriseCaseSnapshot(BaseModel):
    case_id: str
    owner: Optional[EnterpriseUser]
    evidence_records: list[EvidenceRecord]
    audit_events: list[AuditEvent]
    missing_evidence_count: int
    blocked_evidence_count: int
    latest_action: Optional[AuditEvent]
