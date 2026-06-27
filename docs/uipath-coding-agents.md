# UiPath for Coding Agents Usage

## Purpose

UiPath AgentHack gives bonus consideration to solutions that use UiPath for Coding Agents, including coding tools such as Cursor, Claude Code, Codex, Gemini CLI, and others.

CertFlow AI uses UiPath for Coding Agents support to prepare the project for UiPath-based automation development and deployment.

## What was installed

The UiPath CLI package was installed globally using npm:

npm install -g @uipath/cli

The installed CLI version was verified:

uip --version

Verified version:

1.196.0

## Coding agent skills

UiPath coding-agent skills were installed locally for Cursor using:

uip skills install --agent cursor --local

This adds UiPath automation guidance into the project workspace so a coding agent can understand UiPath development tasks such as building, packaging, publishing, deploying, and operating automations.

## How this applies to CertFlow AI

CertFlow AI combines:

- External coded agents in FastAPI
- React dashboard for certification engineers
- UiPath-ready API endpoints
- UiPath CLI and coding-agent setup
- Planned UiPath Maestro Case orchestration once Labs access is activated

## Important note

The team requested UiPath Labs access and received confirmation that access will be provisioned within 3 business days.

Until Labs access is available, the repository includes:

- UiPath integration plan
- UiPath-ready API payloads
- UiPath CLI setup
- Cursor coding-agent skills setup
- API endpoints designed for UiPath API Workflows and Maestro Case

## Relevant endpoints

POST /api/uipath/cases/{case_id}/start

POST /api/uipath/cases/{case_id}/human-review
