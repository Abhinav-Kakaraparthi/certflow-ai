# CertFlow AI Presentation Deck Content

## Slide 1: Title

CertFlow AI

Agentic Aerospace Certification Case Management on UiPath

Built for UiPath AgentHack
Track 1: UiPath Maestro Case

## Slide 2: Problem

Aerospace certification workflows are document-heavy, evidence-driven, and exception-heavy.

Certification engineers must review:

- Engineering change requests
- Drawing packages
- Stress analysis reports
- Test reports
- Safety assessments
- Software verification evidence
- Compliance statements
- DER review records

The challenge is not just extracting data. The challenge is coordinating evidence, risk, human review, and auditability.

## Slide 3: Why Existing Automation Falls Short

Traditional automation works well for fixed workflows.

Certification work is different:

- Each case can follow a different path
- Missing evidence changes the workflow
- High-risk changes require expert review
- Final decisions must be traceable
- Humans must stay in control

This makes certification a strong fit for UiPath Maestro Case.

## Slide 4: Solution

CertFlow AI is an agentic certification case manager.

It uses AI-style agents to:

- Identify affected certification areas
- Detect missing evidence
- Classify risk
- Recommend the next case action
- Route exceptions to human reviewers
- Record review decisions as audit trail

## Slide 5: Agent Workflow

Design Change Request
  -> Certification Basis Agent
  -> Evidence Gap Agent
  -> Risk Classification Agent
  -> UiPath-ready Case Payload
  -> Maestro Case Routing
  -> Human Review or Auto Approval
  -> Audit Trail

## Slide 6: Demo Cases

CERT-001:
Seat tray table latch material change
Outcome: Low risk, complete evidence, auto-approved

CERT-002:
Seat frame bracket geometry update
Outcome: Medium risk, stress analysis and test report missing

CERT-003:
Avionics cooling fan controller replacement
Outcome: High risk, missing safety assessment, software verification, and DER review record

## Slide 7: UiPath Integration

UiPath acts as the orchestration and governance layer.

UiPath can:

- Create certification cases
- Call CertFlow AI backend endpoint
- Read next_uipath_action
- Move the case to the right stage
- Create human review or evidence tasks
- Record final decision history

## Slide 8: Human-in-the-Loop

CertFlow AI does not replace certification engineers.

It keeps humans in control by allowing reviewers to:

- Approve
- Reject
- Request more evidence

Each decision is recorded as an audit message.

## Slide 9: Architecture

Frontend:
React enterprise dashboard

Backend:
FastAPI agent service

Agents:
Certification Basis Agent
Evidence Gap Agent
Risk Classification Agent

UiPath:
Maestro Case orchestration
Human review task
Case closure
Audit trail

## Slide 10: Business Impact

CertFlow AI helps teams:

- Reduce manual evidence review time
- Detect missing certification artifacts earlier
- Improve consistency of case triage
- Keep safety-critical decisions human-governed
- Improve auditability and traceability
- Make AI agents enterprise-ready through UiPath orchestration

## Slide 11: Public Data and Safety

The demo uses synthetic certification cases inspired by public FAA certification planning and compliance references.

No proprietary Collins Aerospace, RTX, Boeing, FAA internal, customer, or confidential data is used.

## Slide 12: Roadmap

Next steps:

- Add document upload and OCR
- Add LLM-based evidence review
- Connect to document repositories
- Build complete UiPath Maestro Case implementation
- Add role-based access control
- Support more certification workflows
