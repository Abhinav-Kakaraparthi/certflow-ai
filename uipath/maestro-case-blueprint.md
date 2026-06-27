# UiPath Maestro Case Blueprint

## Solution Name

CertFlow AI

## Track

Track 1: UiPath Maestro Case

## Case Type

Aerospace Certification Evidence Review Case

## Business Problem

Certification teams must review design changes, validate required evidence, identify missing documents, classify risk, and route exceptions to the right human reviewer. These workflows are long-running, exception-heavy, and require auditability.

CertFlow AI uses agents to triage certification cases and UiPath Maestro Case to coordinate the process across agents, APIs, and human decision points.

## Public API Used by UiPath

Base URL:

https://certflow-ai-api.onrender.com

Case start endpoint:

POST /api/uipath/cases/{case_id}/start

Example:

POST /api/uipath/cases/CERT-003/start

Human review endpoint:

POST /api/uipath/cases/{case_id}/human-review

## Maestro Case Stages

1. Intake
2. Agent Review
3. Evidence Collection
4. Certification Engineer Review
5. DER Review
6. Case Closure

## Case Data Fields

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

## Routing Logic

### Auto Approval Route

Condition:

next_uipath_action = auto_approve_case

UiPath action:

Move case to Case Closure.

Human involvement:

No human review required, but audit summary is retained.

### Missing Evidence Route

Condition:

next_uipath_action = request_missing_evidence

UiPath action:

Create human task for Certification Engineer.

Task title:

Request missing certification evidence

Case stage:

Evidence Collection

### Human Review Route

Condition:

next_uipath_action = create_human_review_task

UiPath action:

Create human task for Senior Certification Engineer.

Case stage:

Certification Engineer Review

### DER Review Route

Condition:

next_uipath_action = create_der_review_task

UiPath action:

Create human task for DER or Senior Certification Authority.

Case stage:

DER Review

## Agent Responsibilities

### Certification Basis Agent

Identifies affected certification areas such as cabin safety, structural substantiation, system safety, software verification, and electrical compatibility.

### Evidence Gap Agent

Checks whether required evidence exists and flags missing certification artifacts.

### Risk Classification Agent

Classifies the case as low, medium, or high risk based on system criticality, change type, and evidence completeness.

## Human-in-the-Loop Controls

Humans remain accountable for high-impact decisions.

Human reviewers can:

- approve the case
- reject the case
- request more evidence

The system records reviewer name, reviewer role, decision, comments, and audit summary.

## Demo Cases

### CERT-001

Low-risk cabin interior material change.

Expected route:

auto_approve_case

### CERT-002

Seat frame bracket update with missing stress and test evidence.

Expected route:

request_missing_evidence

### CERT-003

Avionics cooling controller replacement with missing system safety and software evidence.

Expected route:

request_missing_evidence

Risk:

high

Assigned role:

Certification Engineer

## Why this fits Maestro Case

This solution is designed for long-running certification cases where the process path changes based on evidence, risk, and human review decisions.

UiPath acts as the orchestration and governance layer while CertFlow AI provides agentic analysis through API endpoints.

## Labs Access Status

UiPath Labs access has been requested and is pending provisioning. Once access is available, this blueprint maps directly into a Maestro Case implementation using API Workflows and human tasks.
