# AI Reasoning Architecture

## Purpose

CertFlow AI uses a hybrid agentic architecture:

1. Deterministic certification agents for reliable workflow routing
2. Gemini AI reasoning for high-risk or incomplete certification cases
3. UiPath-ready payloads for Maestro Case orchestration
4. Human review gates for accountability

This prevents the system from relying blindly on an LLM while still using AI where reasoning adds value.

## AI Model

The live AI reasoning layer uses:

gemini-3.1-flash-lite

The model is used through the Google GenAI Python SDK.

## When AI Runs

Gemini reasoning is not called for every case.

To support enterprise-scale usage and avoid unnecessary cost or quota usage, AI reasoning runs only when:

- the case is high risk
- required evidence is missing
- human review is required

Low-risk complete cases use deterministic routing.

## Why This Matters

Certification workflows require consistency, auditability, and human accountability.

CertFlow AI therefore uses deterministic agents for predictable routing and LLM reasoning for deeper analysis, reviewer questions, risk explanation, and escalation recommendations.

## AI Output

The AI reasoning agent returns structured JSON:

- ai_model
- risk_explanation
- certification_concerns
- missing_evidence_questions
- recommended_escalation
- confidence_score
- audit_summary

This output is included directly in the UiPath-ready endpoint:

POST /api/uipath/cases/{case_id}/start

## Example High-Risk Case

CERT-003 is an avionics cooling fan controller replacement with missing system safety and software verification evidence.

Expected AI result:

- recommended_escalation: DER review
- confidence_score: high
- certification_concerns: safety assessment, software verification, interface compatibility
- reviewer_questions: evidence questions for certification engineer review

## Safety and Fallback

If the AI provider is unavailable or rate-limited, CertFlow AI does not fail open.

Instead, it uses deterministic safety fallback routing and preserves human oversight.

The system never auto-approves safety-critical or incomplete certification cases based only on AI output.
