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

    def analyze_case(self, certification_case: DesignChangeRequest) -> AIReasoningResult:
        if not self.client:
            return AIReasoningResult(
                ai_model="fallback-no-api-key",
                risk_explanation="Gemini API key is not configured. Rule-based routing is available, but live AI reasoning is disabled.",
                certification_concerns=[
                    "Live AI certification reasoning was skipped because GEMINI_API_KEY is missing."
                ],
                missing_evidence_questions=[
                    "Configure GEMINI_API_KEY to enable live AI reasoning."
                ],
                recommended_escalation="Configuration required",
                confidence_score=0.0,
                audit_summary="AI reasoning unavailable because Gemini API key is not configured."
            )

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

        return result

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
