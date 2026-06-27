# CertFlow AI

## Agentic Aerospace Certification Case Management on UiPath

CertFlow AI is an agentic certification case management system built for the UiPath AgentHack Track 1: UiPath Maestro Case.

The project demonstrates how aerospace certification engineers can use governed AI agents to review design changes, detect missing certification evidence, classify risk, and route exceptions to human reviewers before a case is approved or closed.

## Problem

Aerospace certification work is document-heavy, evidence-driven, and exception-heavy. Certification engineers often need to review engineering change requests, updated drawings, stress analysis reports, safety assessments, software verification evidence, compliance statements, and DER review records.

Many AI prototypes can summarize documents, but enterprise certification work requires more than summarization. It requires orchestration, traceability, role-based handoffs, evidence tracking, and human control.

## Solution

CertFlow AI turns certification review into a governed agentic case workflow.

For each certification case, the system:

1. Reads the design change request.
2. Identifies affected certification areas.
3. Checks whether required evidence is available.
4. Classifies risk as low, medium, or high.
5. Generates a UiPath-ready case action.
6. Routes exception cases to a human certification engineer.
7. Records the human decision as an audit trail.

## Demo Cases

| Case ID | Scenario | Outcome |
|---|---|---|
| CERT-001 | Seat tray table latch material change | Auto-approved |
| CERT-002 | Seat frame bracket geometry update | Missing evidence requested |
| CERT-003 | Avionics cooling fan controller replacement | High-risk evidence gap and human review |

## Agents

### Certification Basis Agent

Identifies certification areas affected by the design change, such as cabin interior compliance, structural substantiation, flammability review, system safety assessment, electrical interface compatibility, or software verification evidence.

### Evidence Gap Agent

Checks whether required certification artifacts are available and flags missing evidence such as stress analysis reports, test reports, system safety assessments, software verification evidence, or DER review records.

### Risk Classification Agent

Classifies the case as low, medium, or high risk based on affected system, missing evidence, structural impact, avionics impact, and software/control logic changes.

### Human Review Gate

Allows a certification engineer or DER reviewer to approve, reject, or request more evidence. The result is recorded as an audit trail.

## UiPath Alignment

This project is designed for Track 1: UiPath Maestro Case.

UiPath acts as the enterprise orchestration layer that coordinates:

- AI agent analysis
- Case stage progression
- Evidence collection
- Human review tasks
- Final case closure
- Audit trail generation

The backend exposes UiPath-ready API endpoints that can be called from UiPath Maestro Case, UiPath API Workflows, or UiPath Robots.

## UiPath Components Intended

- UiPath Automation Cloud
- UiPath Maestro Case
- UiPath API Workflows
- UiPath Robots
- Human-in-the-loop review task
- External FastAPI agent service

## Architecture

```text
Design Change Request
        |
        v
FastAPI Certification Case API
        |
        v
Certification Basis Agent
        |
        v
Evidence Gap Agent
        |
        v
Risk Classification Agent
        |
        v
UiPath-ready Case Payload
        |
        v
UiPath Maestro Case
        |
        v
Human Review / Evidence Request / Auto Approval
        |
        v
Audit Trail and Case Closure
@'
# CertFlow AI

## Agentic Aerospace Certification Case Management on UiPath

CertFlow AI is an agentic aerospace certification case management system built for UiPath AgentHack Track 1: UiPath Maestro Case.

The project demonstrates how certification engineers can use governed AI agents to review design changes, detect missing certification evidence, classify certification risk, and route exceptions to human reviewers before a case is approved or closed.

## Problem

Aerospace certification work is document-heavy, evidence-driven, and exception-heavy.

Certification engineers often need to review engineering change requests, updated drawings, stress analysis reports, test reports, safety assessments, software verification evidence, compliance statements, and DER review records.

Most AI prototypes can summarize documents, but enterprise certification work requires more than summarization. It requires orchestration, traceability, evidence tracking, role-based handoffs, human review, and auditability.

## Solution

CertFlow AI turns certification review into a governed agentic case workflow.

For each certification case, the system:

1. Reads the design change request.
2. Identifies affected certification areas.
3. Checks whether required evidence is available.
4. Classifies risk as low, medium, or high.
5. Generates a UiPath-ready case action.
6. Routes exception cases to a human certification engineer.
7. Records the human decision as an audit trail.

## Demo Cases

| Case ID | Scenario | Outcome |
|---|---|---|
| CERT-001 | Seat tray table latch material change | Auto-approved |
| CERT-002 | Seat frame bracket geometry update | Missing evidence requested |
| CERT-003 | Avionics cooling fan controller replacement | High-risk evidence gap and human review |

## Agents

### Certification Basis Agent

Identifies certification areas affected by the design change, such as cabin interior compliance, structural substantiation, flammability review, system safety assessment, electrical interface compatibility, or software verification evidence.

### Evidence Gap Agent

Checks whether required certification artifacts are available and flags missing evidence such as stress analysis reports, test reports, system safety assessments, software verification evidence, or DER review records.

### Risk Classification Agent

Classifies the case as low, medium, or high risk based on affected system, missing evidence, structural impact, avionics impact, and software or control logic changes.

### Human Review Gate

Allows a certification engineer or DER reviewer to approve, reject, or request more evidence. The result is recorded as an audit trail.

## UiPath Alignment

This project is designed for Track 1: UiPath Maestro Case.

UiPath acts as the enterprise orchestration layer that coordinates:

- AI agent analysis
- Case stage progression
- Evidence collection
- Human review tasks
- Final case closure
- Audit trail generation

The backend exposes UiPath-ready API endpoints that can be called from UiPath Maestro Case, UiPath API Workflows, or UiPath Robots.

## UiPath Components Intended

- UiPath Automation Cloud
- UiPath Maestro Case
- UiPath API Workflows
- UiPath Robots
- Human-in-the-loop review task
- External FastAPI agent service

## Architecture

Design Change Request
  -> FastAPI Certification Case API
  -> Certification Basis Agent
  -> Evidence Gap Agent
  -> Risk Classification Agent
  -> UiPath-ready Case Payload
  -> UiPath Maestro Case
  -> Human Review / Evidence Request / Auto Approval
  -> Audit Trail and Case Closure

## Tech Stack

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn
- Rule-based agent workflow for stable demo execution

### Frontend

- React
- Vite
- Lucide React
- Enterprise dark dashboard UI

### Demo Data

Synthetic aerospace certification cases inspired by public FAA certification planning and compliance references.

No proprietary Collins Aerospace, RTX, Boeing, FAA internal, customer, or confidential data is used.

## Public FAA References

See:

docs/public-faa-references.md

## Backend Setup

Windows PowerShell:

1. Move into the backend folder:

   cd backend

2. Activate the virtual environment:

   .\venv\Scripts\activate

3. Install dependencies:

   pip install -r requirements.txt

4. Run the backend:

   uvicorn app.main:app --reload --port 8001

Backend health check:

http://127.0.0.1:8001/api/health

Swagger docs:

http://127.0.0.1:8001/docs

## Frontend Setup

1. Move into the frontend folder:

   cd frontend

2. Install dependencies:

   npm install

3. Run the frontend:

   npm run dev

Frontend local URL:

http://localhost:5173/

## Important API Endpoints

### List certification cases

GET /api/cases

### Run agentic workflow for one case

POST /api/workflow/cases/{case_id}/run

### Generate UiPath-ready case payload

POST /api/uipath/cases/{case_id}/start

### Submit human certification review

POST /api/uipath/cases/{case_id}/human-review

Example human review payload:

{
  "reviewer_name": "Alex Morgan",
  "reviewer_role": "Senior Certification Engineer",
  "decision": "request_more_evidence",
  "comments": "System safety assessment and software verification evidence must be completed before DER review."
}

## Demo Flow

1. Start the backend on port 8001.
2. Start the frontend on port 5173.
3. Open the CertFlow AI dashboard.
4. Click Run Case Flow.
5. Review the three certification cases.
6. Select CERT-001 to show auto-approval.
7. Select CERT-002 to show missing evidence detection.
8. Select CERT-003 to show high-risk avionics certification review.
9. Submit a human review decision.
10. Show the audit trail recorded in the dashboard.

## Coding Agents Used

Coding agents were used to assist with:

- Backend service structure
- Agent workflow implementation
- API endpoint design
- Frontend dashboard implementation
- README and documentation organization

## Repository Structure

certflow-ai/
  backend/
    app/
      agents/
      api/
      core/
      models/
      services/
      workflows/
    tests/
    requirements.txt
  frontend/
    src/
      components/
      services/
  demo-data/
  docs/
  uipath/
  submissions/

## License

MIT

## Public Demo API

The CertFlow AI backend is deployed publicly for UiPath API Workflow and Maestro integration.

Base URL:

https://certflow-ai-api.onrender.com

Health check:

GET /api/health

UiPath-ready case start endpoint:

POST /api/uipath/cases/{case_id}/start

Example:

POST /api/uipath/cases/CERT-003/start

This returns a UiPath-ready orchestration payload containing:

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

Example routing result for CERT-003:

- next_uipath_action: request_missing_evidence
- maestro_stage: Evidence Collection
- assigned_role: Certification Engineer
- overall_risk: high

