# UiPath Integration Plan

## Track

CertFlow AI is designed for Track 1: UiPath Maestro Case.

The workflow is dynamic and exception-heavy because each certification case can follow a different path depending on evidence completeness, certification risk, and human review decisions.

## Role of UiPath

UiPath is the orchestration and governance layer.

The external CertFlow AI FastAPI service performs agentic certification analysis, but UiPath controls the enterprise process:

1. Create certification case
2. Call CertFlow AI agent endpoint
3. Read UiPath-ready case payload
4. Route case to the correct stage
5. Create human review task if needed
6. Request missing evidence if needed
7. Close or approve low-risk cases
8. Store decision history and audit trail

## Main UiPath-Ready Endpoint

POST /api/uipath/cases/{case_id}/start

Example:

POST http://127.0.0.1:8001/api/uipath/cases/CERT-003/start

## Response Fields Used by UiPath

- case_id
- case_status
- overall_risk
- human_review_required
- missing_documents
- next_uipath_action
- maestro_stage
- task_title
- assigned_role
- agent_summary
- agent_findings

## UiPath Action Mapping

| next_uipath_action | UiPath Maestro Case Behavior |
|---|---|
| auto_approve_case | Move case to Case Closure |
| request_missing_evidence | Create evidence collection task |
| create_human_review_task | Create certification engineer review task |
| create_der_review_task | Create DER or senior certification review task |

## Case Stage Mapping

| Condition | Maestro Stage |
|---|---|
| Low risk and complete evidence | Case Closure |
| Missing evidence | Evidence Collection |
| Medium risk | Certification Review |
| High risk | DER Review |

## Human Review Endpoint

POST /api/uipath/cases/{case_id}/human-review

Example payload:

{
  "reviewer_name": "Alex Morgan",
  "reviewer_role": "Senior Certification Engineer",
  "decision": "request_more_evidence",
  "comments": "System safety assessment and software verification evidence must be completed before DER review."
}

## Human Review Decisions

| Decision | Final Case Status |
|---|---|
| approve | approved |
| reject | rejected |
| request_more_evidence | needs_more_evidence |

## Demo Script for UiPath Portion

1. Start a new certification case in UiPath Maestro Case.
2. UiPath calls the CertFlow AI start endpoint.
3. CertFlow AI returns risk, missing evidence, and next action.
4. UiPath routes the case to the correct stage.
5. If evidence is missing, UiPath creates an evidence collection task.
6. If risk is high, UiPath creates a senior certification review task.
7. Human reviewer submits decision.
8. UiPath records the audit message and updates the case status.

## Why This Fits Maestro Case

Certification workflows are not always linear. A low-risk case can close quickly, a structural case may need missing evidence, and a high-risk avionics case may require senior review or DER review.

This makes the workflow a strong fit for UiPath Maestro Case because the case path changes based on agent findings and human decisions.
