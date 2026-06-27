from typing import List
from pydantic import BaseModel, Field


class AIReasoningResult(BaseModel):
    ai_model: str = Field(description="Name of the AI model used for reasoning.")
    risk_explanation: str = Field(description="Plain-English explanation of the certification risk.")
    certification_concerns: List[str] = Field(description="Specific technical or certification concerns identified by AI.")
    missing_evidence_questions: List[str] = Field(description="Questions the certification engineer should ask before approval.")
    recommended_escalation: str = Field(description="Recommended escalation path such as auto approve, certification engineer review, or DER review.")
    confidence_score: float = Field(description="AI confidence score from 0.0 to 1.0.")
    audit_summary: str = Field(description="Short audit-friendly summary of the AI reasoning.")
