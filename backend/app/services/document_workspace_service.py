import json
from datetime import datetime, timezone
from pathlib import Path

from app.models.document_workspace import (
    DocumentCreateRequest,
    DocumentSection,
    DocumentSectionUpdate,
    WorkspaceDocument,
)

DATA_DIR = Path(__file__).resolve().parents[2] / "demo-data"
DOCUMENTS_PATH = DATA_DIR / "document_workspace.json"
AUDIT_EVENTS_PATH = DATA_DIR / "audit_events.json"
USERS_PATH = DATA_DIR / "users.json"


def _load_json(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def _save_json(path: Path, records: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=2)


def _load_raw_documents() -> list[dict]:
    return _load_json(DOCUMENTS_PATH)


def _save_raw_documents(documents: list[dict]) -> None:
    _save_json(DOCUMENTS_PATH, documents)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _user_role(user_id: str) -> str:
    users = _load_json(USERS_PATH)

    for user in users:
        if user["user_id"] == user_id:
            return user["role"]

    return "Unknown User"


def _next_audit_id(events: list[dict]) -> str:
    return f"AUD-{len(events) + 1:03d}"


def _append_audit_event(
    case_id: str,
    actor_id: str,
    action: str,
    target: str,
    summary: str,
) -> None:
    events = _load_json(AUDIT_EVENTS_PATH)

    events.append(
        {
            "event_id": _next_audit_id(events),
            "case_id": case_id,
            "actor_id": actor_id,
            "actor_role": _user_role(actor_id),
            "action": action,
            "target": target,
            "timestamp": _utc_now(),
            "summary": summary,
        }
    )

    _save_json(AUDIT_EVENTS_PATH, events)


def load_workspace_documents() -> list[WorkspaceDocument]:
    return [WorkspaceDocument(**item) for item in _load_raw_documents()]


def get_documents_for_case(case_id: str) -> list[WorkspaceDocument]:
    return [
        document
        for document in load_workspace_documents()
        if document.case_id == case_id
    ]


def get_workspace_document(document_id: str) -> WorkspaceDocument:
    for document in load_workspace_documents():
        if document.document_id == document_id:
            return document

    raise ValueError(f"Document {document_id} was not found")


def update_document_section(
    document_id: str,
    update: DocumentSectionUpdate,
) -> WorkspaceDocument:
    documents = _load_raw_documents()

    for document in documents:
        if document["document_id"] != document_id:
            continue

        section_updated = False
        edited_section_title = update.section_id

        for section in document["sections"]:
            if section["section_id"] == update.section_id:
                section["content"] = update.content
                section["status"] = update.status
                edited_section_title = section["title"]
                section_updated = True
                break

        if not section_updated:
            raise ValueError(
                f"Section {update.section_id} was not found in document {document_id}"
            )

        document["current_editor_id"] = update.editor_id
        document["last_edited_at"] = _utc_now()
        document["status"] = "in_progress"
        document["ai_review_status"] = "needs_revision"

        _save_raw_documents(documents)

        _append_audit_event(
            case_id=document["case_id"],
            actor_id=update.editor_id,
            action="Edited certification evidence",
            target=document["title"],
            summary=(
                f"{edited_section_title} was updated inside the CertFlow evidence "
                f"workspace. Edit summary: {update.edit_summary}. AI review status "
                "was reset to needs_revision."
            ),
        )

        return WorkspaceDocument(**document)

    raise ValueError(f"Document {document_id} was not found")


def create_workspace_document(
    request: DocumentCreateRequest,
) -> WorkspaceDocument:
    documents = _load_raw_documents()
    next_number = len(documents) + 1
    document_id = f"DOC-{next_number:03d}"
    section_id = f"SEC-{100 + next_number}"

    document = WorkspaceDocument(
        document_id=document_id,
        case_id=request.case_id,
        title=request.title,
        artifact_type=request.artifact_type,
        format=request.format,
        owner_id=request.owner_id,
        current_editor_id=request.owner_id,
        created_by=request.created_by,
        version="0.1",
        status="draft",
        ai_review_status="not_reviewed",
        required_review_role=request.required_review_role,
        last_edited_at=_utc_now(),
        content_summary=request.content_summary,
        sections=[
            DocumentSection(
                section_id=section_id,
                title="Initial Draft",
                status="draft",
                content="New certification artifact created inside CertFlow AI workspace.",
            )
        ],
    )

    documents.append(document.model_dump())
    _save_raw_documents(documents)

    _append_audit_event(
        case_id=request.case_id,
        actor_id=request.created_by,
        action="Created certification artifact",
        target=request.title,
        summary=(
            f"{request.title} was created directly inside the CertFlow evidence "
            f"workspace and assigned to {request.required_review_role} review."
        ),
    )

    return document
