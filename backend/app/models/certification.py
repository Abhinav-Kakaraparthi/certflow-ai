from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class CaseStatus(str, Enum):
    NEW = "new"
    IN_REVIEW = "in_review"
    WAITING_FOR_HUMAN = "waiting_for_human"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_MORE_EVIDENCE = "needs_more_evidence"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class CertificationTrack(str, Enum):
    FAA_PART_23 = "faa_part_23"
    FAA_PART_25 = "faa_part_25"
    STC = "supplemental_type_certificate"


class CertificationDocument(BaseModel):
    document_name: str
    document_type: str
    is_available: bool
    notes: Optional[str] = None


class DesignChangeRequest(BaseModel):
    case_id: str
    title: str
    aircraft_area: str
    component: str
    change_summary: str
    reason_for_change: str
    certification_track: CertificationTrack
    submitted_by: str
    documents: List[CertificationDocument] = Field(default_factory=list)


class AgentFinding(BaseModel):
    agent_name: str
    summary: str
    risk_level: RiskLevel
    findings: List[str]
    recommended_next_step: str


class CertificationCaseResult(BaseModel):
    case_id: str
    status: CaseStatus
    overall_risk: RiskLevel
    findings: List[AgentFinding]
    missing_documents: List[str]
    human_review_required: bool
    final_summary: str
