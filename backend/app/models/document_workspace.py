from typing import Optional

from pydantic import BaseModel


class DocumentSection(BaseModel):
    section_id: str
    title: str
    status: str
    content: str


class WorkspaceDocument(BaseModel):
    document_id: str
    case_id: str
    title: str
    artifact_type: str
    format: str
    owner_id: str
    current_editor_id: Optional[str] = None
    created_by: str
    version: str
    status: str
    ai_review_status: str
    required_review_role: str
    last_edited_at: str
    content_summary: str
    sections: list[DocumentSection]


class DocumentSectionUpdate(BaseModel):
    section_id: str
    editor_id: str
    content: str
    status: str = "in_progress"
    edit_summary: str


class DocumentCreateRequest(BaseModel):
    case_id: str
    title: str
    artifact_type: str
    format: str = "structured_document"
    owner_id: str
    created_by: str
    required_review_role: str
    content_summary: str
