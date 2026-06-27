# CertFlow AI

## Tagline

Agentic aerospace certification case management with UiPath orchestration, evidence intelligence, and human-in-the-loop review.

## Track

UiPath Maestro Case

## Inspiration

Aerospace certification engineers work on safety-critical design changes where every decision needs evidence, traceability, and review. These workflows are not simple document-processing tasks. A low-risk design change may close quickly, a structural change may require missing analysis and test evidence, and a high-risk avionics change may require senior certification or DER review.

CertFlow AI was inspired by this real enterprise problem: how can AI agents help certification engineers move faster without removing human control?

## What it does

CertFlow AI turns aerospace certification review into a governed agentic case workflow.

For each certification case, the system:

1. Reads a design change request.
2. Identifies affected certification areas.
3. Detects missing certification evidence.
4. Classifies the case as low, medium, or high risk.
5. Generates a UiPath-ready next action.
6. Routes exceptions to a human certification engineer.
7. Records the final human decision as an audit trail.

## The problem it solves

Certification workflows are evidence-heavy, exception-heavy, and highly regulated. Teams need to track engineering changes, drawings, analysis reports, test evidence, safety assessments, software verification evidence, compliance statements, and DER review records.

Traditional automation struggles because each case can follow a different path. CertFlow AI helps by using agents to reason over the case, while UiPath remains the orchestration and governance layer.

## How it works

CertFlow AI uses three core agents:

Certification Basis Agent:
Identifies certification areas affected by the design change.

Evidence Gap Agent:
Checks whether required certification evidence is missing.

Risk Classification Agent:
Classifies the case risk and recommends the next case action.

The backend exposes UiPath-ready API endpoints. UiPath Maestro Case can call these endpoints, read the next recommended action, route the case to evidence collection, human review, DER review, or case closure, and preserve a traceable workflow.

## Demo scenarios

CERT-001:
A seat tray table latch material change is classified as low risk with complete evidence and is auto-approved.

CERT-002:
A seat frame bracket geometry update is classified as medium risk because stress analysis and test report evidence are missing.

CERT-003:
An avionics cooling fan controller replacement is classified as high risk because it affects control logic and electrical interface behavior. The system detects missing system safety assessment, software verification evidence, and DER review record, then routes the case to human review.

## UiPath integration

CertFlow AI is designed for UiPath Maestro Case.

UiPath is responsible for:

- Creating and tracking certification cases
- Calling the CertFlow AI agent service
- Reading the recommended next action
- Routing cases to the correct stage
- Creating human review or evidence collection tasks
- Recording final case status and audit trail

## Human-in-the-loop

CertFlow AI does not replace certification engineers. It supports them.

Human reviewers can approve, reject, or request more evidence. Their decision is recorded as an audit trail, ensuring that safety-critical certification decisions remain under human control.

## Tech stack

Backend:
Python, FastAPI, Pydantic, Uvicorn, Pytest

Frontend:
React, Vite, Lucide React, enterprise dark dashboard UI

Workflow:
Rule-based agent orchestration for reliable demo execution, with UiPath-ready case payloads

## Public data and safety

The project uses synthetic demo certification cases inspired by public FAA certification planning and compliance references. No proprietary Collins Aerospace, RTX, Boeing, FAA internal, customer, or confidential data is used.

## What we learned

The biggest learning was that enterprise AI agents need more than intelligence. They need orchestration, governance, exception handling, auditability, and human decision gates. CertFlow AI shows how UiPath can bridge that gap between AI agent output and real enterprise process execution.

## What's next

Future improvements include:

- Connecting to real document repositories
- Adding document upload and OCR extraction
- Integrating LLM-based evidence review
- Creating full UiPath Maestro Case implementation
- Adding role-based access control
- Supporting additional certification workflows beyond aerospace
