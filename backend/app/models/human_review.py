from enum import Enum
from typing import Optional
from pydantic import BaseModel


class HumanDecision(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    REQUEST_MORE_EVIDENCE = "request_more_evidence"


class HumanReviewRequest(BaseModel):
    reviewer_name: str
    reviewer_role: str
    decision: HumanDecision
    comments: Optional[str] = None


class HumanReviewResult(BaseModel):
    case_id: str
    reviewer_name: str
    reviewer_role: str
    decision: HumanDecision
    final_case_status: str
    comments: Optional[str]
    audit_message: str
