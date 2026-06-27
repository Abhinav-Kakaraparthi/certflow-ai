import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.models.ai_reasoning import AIReasoningResult
from app.models.certification import DesignChangeRequest


BACKEND_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(BACKEND_ROOT / ".env")


class AIReasoningService:
    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None
        self.cache: dict[str, AIReasoningResult] = {}

    def analyze_case(self, certification_case: DesignChangeRequest) -> AIReasoningResult:
        if certification_case.case_id in self.cache:
            return self.cache[certification_case.case_id]

        if not self.client:
            return self._safe_fallback(
                certification_case,
                "Gemini API key is not configured. Deterministic routing remains active.",
            )

        try:
            prompt = self._build_prompt(certification_case)

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    response_mime_type="application/json",
                    response_schema=AIReasoningResult,
                ),
            )

            result = response.parsed if response.parsed else AIReasoningResult.model_validate_json(response.text)

            result.ai_model = self.model_name
            result.certification_concerns = [
                concern.replace("FAA Part 25", "applicable certification requirements")
                for concern in result.certification_concerns
            ]
            result.missing_evidence_questions = [
                question.replace("FAA Part 25", "applicable certification requirements")
                for question in result.missing_evidence_questions
            ]
            result.audit_summary = result.audit_summary.replace(
                "FAA Part 25",
                "applicable certification requirements",
            )

            self.cache[certification_case.case_id] = result
            return result

        except Exception:
            return self._safe_fallback(
                certification_case,
                "Live AI reasoning is temporarily unavailable or rate-limited. Deterministic routing completed safely.",
            )

    def _safe_fallback(self, certification_case: DesignChangeRequest, reason: str) -> AIReasoningResult:
        return AIReasoningResult(
            ai_model="deterministic-safety-fallback",
            risk_explanation=reason,
            certification_concerns=[
                f"Fallback routing used for {certification_case.case_id}.",
                "Certification decision remains blocked if required evidence is missing.",
                "Human review is preserved for safety-critical or incomplete cases.",
            ],
            missing_evidence_questions=[
                "Are all required certification evidence artifacts attached?",
                "Does this change affect safety, software, structure, electrical behavior, or control logic?",
                "Should a certification engineer or DER review this case before closure?",
            ],
            recommended_escalation="Certification Engineer review",
            confidence_score=0.0,
            audit_summary="AI provider was unavailable, so CertFlow used deterministic safety routing and preserved human oversight.",
        )

    def _build_prompt(self, certification_case: DesignChangeRequest) -> str:
        return f"""
You are an aerospace certification reasoning agent.

Your job is to analyze a design change case and produce an audit-safe certification review summary.

Rules:
- Do not approve safety-critical or missing-evidence cases.
- Do not invent regulations, regulation numbers, FAA parts, company policies, or private facts.
- Do not mention specific regulation names or numbers unless they appear in the case data.
- Base your reasoning only on the case data below.
- Use plain English suitable for a certification engineer and UiPath Maestro audit trail.
- Keep the output concise, professional, and evidence-based.

Case data:
{certification_case.model_dump_json(indent=2)}

Return a structured result with:
- ai_model
- risk_explanation
- certification_concerns
- missing_evidence_questions
- recommended_escalation
- confidence_score
- audit_summary
"""
