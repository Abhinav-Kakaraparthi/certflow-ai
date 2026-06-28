# UiPath AgentHack Implementation Proof

CertFlow AI was built for the UiPath AgentHack Track 1 Maestro Case challenge as an enterprise certification case-management workflow.

The implementation focuses on long-running, exception-heavy aerospace certification cases where evidence owners, certification engineers, AI agents, DER reviewers, and managers must coordinate across multiple stages.

## 1. UiPath orchestration contract

CertFlow AI exposes UiPath-ready endpoints that can be consumed by UiPath API Workflows or Maestro cases.

### Start certification case

POST https://certflow-ai-api.onrender.com/api/uipath/cases/CERT-003/start

Returns:
- case_id
- case_status
- overall_risk
- missing_documents
- maestro_stage
- next_uipath_action
- assigned_role
- human_review_required
- Gemini AI reasoning

For the high-risk avionics case, the endpoint routes the case to evidence collection and DER review.

### Route edited evidence artifact

POST https://certflow-ai-api.onrender.com/api/uipath/documents/DOC-001/route

Returns:
- document_id
- case_id
- artifact_type
- document_status
- ai_review_status
- maestro_stage
- next_uipath_action
- assigned_role
- human_review_required
- routing_reason

This proves the in-app Evidence Workspace is connected to UiPath-style orchestration. When an engineer edits certification evidence, UiPath can route the document to AI review, DER review, supplier follow-up, or human approval.

## 2. Agentic workflow components

CertFlow AI separates work into specialized agents and roles:

- Certification Basis Agent
- Evidence Gap Agent
- Risk Classification Agent
- Gemini Reasoning Agent
- Evidence Workspace Authoring Actor
- DER Reviewer
- Certification Manager
- UiPath Maestro Case Orchestrator

The backend produces deterministic routing decisions and uses Gemini for structured reasoning when the case is high-risk, incomplete, or requires human review.

## 3. Evidence Workspace implementation

Employees do not create Word documents outside the system and upload them manually.

Instead, CertFlow AI includes an in-app Evidence Workspace where users can:

- create certification artifacts
- edit evidence sections
- track document version
- track current editor
- track owner and required reviewer
- see AI review status
- trigger audit events after edits
- route artifacts through UiPath-ready endpoints

Implemented files:
- backend/demo-data/document_workspace.json
- backend/app/models/document_workspace.py
- backend/app/services/document_workspace_service.py
- backend/app/api/document_workspace.py
- frontend/src/components/dashboard/EvidenceWorkspace.jsx

## 4. Audit and governance

Document edits automatically create audit events.

Example flow:
1. Engineer edits a Failure Modes section.
2. Document status remains in_progress.
3. AI review status resets to needs_revision.
4. Audit event is created.
5. UiPath document routing endpoint returns create_ai_review_task.
6. Assigned role becomes DER Reviewer.

This supports governed enterprise automation instead of a simple chatbot or dashboard.

## 5. UiPath for Coding Agents evidence

UiPath CLI was installed and verified locally.

Command used:

uip --version

Verified version:

1.196.0

UiPath skills were installed for Cursor:

uip skills install --agent cursor --local

This produced local Cursor skill configuration under .cursor/skills. The .cursor folder is intentionally not committed because it is local tool configuration, but the implementation proof and commands are documented in docs/uipath-coding-agents.md.

## 6. Public deployment proof

Public API:

https://certflow-ai-api.onrender.com

Health checks:
- GET https://certflow-ai-api.onrender.com/health
- GET https://certflow-ai-api.onrender.com/api/health

Key UiPath endpoints:
- POST /api/uipath/cases/CERT-003/start
- POST /api/uipath/documents/DOC-001/route

Evidence workspace endpoints:
- GET /api/documents/case/CERT-003
- PATCH /api/documents/DOC-001/sections
- POST /api/documents

## 7. Why this is a Maestro Case

CertFlow AI is not a one-shot automation.

It is a long-running certification case process with:
- multiple evidence artifacts
- missing documentation
- AI risk analysis
- document authoring
- audit history
- exception routing
- role-based ownership
- human approval gates
- DER escalation

This maps directly to a UiPath Maestro-style case where agents, APIs, and humans collaborate across stages.
