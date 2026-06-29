# CertFlow AI

## Project Description

CertFlow AI is an enterprise aerospace certification workflow system built for the UiPath AgentHack Track 1 Maestro Case challenge.

The project helps certification teams manage aircraft design changes by turning every design change into a governed certification case. It detects missing evidence, classifies certification risk, explains the decision basis, supports in-app evidence authoring, routes work to human reviewers, and records audit history.

The problem CertFlow AI solves is that certification engineers often spend significant time on manual tracking, document follow-ups, evidence checking, and approval coordination across scattered documents, emails, and spreadsheets. CertFlow AI structures this work into a clear, auditable, AI-assisted workflow where UiPath can orchestrate the next action.

## UiPath Components Used

CertFlow AI is designed for UiPath Maestro-style case orchestration and exposes UiPath-ready API endpoints that can be consumed by UiPath workflows.

UiPath components and concepts used:

- UiPath Maestro Case architecture for long-running certification workflows
- UiPath API Workflow-ready endpoints
- UiPath Orchestrator / Automation Cloud environment for workflow execution
- UiPath human-in-the-loop task routing concept
- UiPath Coded Agent / API-based agent integration pattern
- UiPath CLI for local setup verification
- UiPath for Coding Agents with Cursor local skills
- Public REST endpoints for case start and document routing

Key UiPath-ready endpoints:

POST https://certflow-ai-api.onrender.com/api/uipath/cases/CERT-003/start

POST https://certflow-ai-api.onrender.com/api/uipath/documents/DOC-001/route

Example routing output:

{
  "maestro_stage": "AI Evidence Review",
  "next_uipath_action": "create_ai_review_task",
  "assigned_role": "DER Reviewer",
  "human_review_required": true
}

## Agent Type

CertFlow AI uses a hybrid agent architecture.

### Coded Agents

The backend includes coded agents implemented in Python and FastAPI:

- Certification Basis Agent
- Evidence Gap Agent
- Risk Classification Agent
- Gemini Reasoning Agent
- Evidence Workspace Actor
- Human Review Actor
- UiPath Routing Agent

These agents inspect certification cases, compare required vs available evidence, classify risk, generate reviewer guidance, update audit history, and return UiPath-ready routing decisions.

### Low-code / Maestro-style Orchestration

The solution is designed for UiPath Maestro and API Workflow orchestration. UiPath acts as the orchestration layer that can call CertFlow AI endpoints, inspect the next action, create human review tasks, and route cases to engineers, DER reviewers, or evidence owners.

## Setup Instructions

### 1. Clone the repository

git clone https://github.com/Abhinav-Kakaraparthi/certflow-ai.git

cd certflow-ai

### 2. Backend setup

cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload --port 8001

Backend runs at:

http://localhost:8001

### 3. Frontend setup

Open a new terminal:

cd frontend

npm install

npm run dev

Frontend runs at:

http://localhost:5173

### 4. Environment variables

For local Gemini AI reasoning, create:

backend/.env

Add:

GEMINI_API_KEY=your_gemini_api_key

GEMINI_MODEL=gemini-3.1-flash-lite

The system includes deterministic fallback routing, so the workflow remains functional even if Gemini is unavailable.

### 5. Run tests

cd backend

pytest

Expected result:

4 passed

### 6. Public deployment

Frontend website:

https://certflow-ai-web.onrender.com

Backend API:

https://certflow-ai-api.onrender.com

Health checks:

GET https://certflow-ai-api.onrender.com/health

GET https://certflow-ai-api.onrender.com/api/health

### 7. Test UiPath-ready endpoints

Start high-risk certification case:

curl -X POST https://certflow-ai-api.onrender.com/api/uipath/cases/CERT-003/start

Route edited evidence document:

curl -X POST https://certflow-ai-api.onrender.com/api/uipath/documents/DOC-001/route

## Live Links

- Website: https://certflow-ai-web.onrender.com
- Backend API: https://certflow-ai-api.onrender.com
- GitHub Repository: https://github.com/Abhinav-Kakaraparthi/certflow-ai
