from fastapi import APIRouter, HTTPException

from app.models.document_workspace import (
    DocumentCreateRequest,
    DocumentSectionUpdate,
    WorkspaceDocument,
)
from app.services.document_workspace_service import (
    create_workspace_document,
    get_documents_for_case,
    get_workspace_document,
    load_workspace_documents,
    update_document_section,
)

router = APIRouter(prefix="/documents", tags=["Document Workspace"])


@router.get("", response_model=list[WorkspaceDocument])
def get_all_workspace_documents() -> list[WorkspaceDocument]:
    return load_workspace_documents()


@router.get("/case/{case_id}", response_model=list[WorkspaceDocument])
def get_case_documents(case_id: str) -> list[WorkspaceDocument]:
    return get_documents_for_case(case_id)


@router.get("/{document_id}", response_model=WorkspaceDocument)
def get_document(document_id: str) -> WorkspaceDocument:
    try:
        return get_workspace_document(document_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.post("", response_model=WorkspaceDocument)
def create_document(request: DocumentCreateRequest) -> WorkspaceDocument:
    return create_workspace_document(request)


@router.patch("/{document_id}/sections", response_model=WorkspaceDocument)
def edit_document_section(
    document_id: str,
    update: DocumentSectionUpdate,
) -> WorkspaceDocument:
    try:
        return update_document_section(document_id, update)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
