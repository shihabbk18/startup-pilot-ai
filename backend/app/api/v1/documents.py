from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import RequestContext, get_request_context
from app.db.session import get_db
from app.models.entities import Document
from app.models.entities import DocumentStatus
from app.schemas.document import ChatRequest, ChatResponse, Citation, DocumentResponse
from app.services.rag import InMemoryRAGService

router = APIRouter()
rag_service = InMemoryRAGService()


@router.post(
    "/projects/{project_id}/documents",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    project_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    context: RequestContext = Depends(get_request_context),
) -> DocumentResponse:
    allowed_types = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "text/plain",
    }
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Unsupported file type")
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")
    document = Document(
        organization_id=context.organization_id,
        project_id=project_id,
        uploaded_by=context.user_id,
        filename=file.filename or "uploaded-file",
        mime_type=file.content_type or "application/octet-stream",
        storage_path=f"projects/{project_id}/documents/{file.filename or 'uploaded-file'}",
        status=DocumentStatus.INDEXED,
        token_count=len(text.split()),
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    rag_service.index_document(project_id=project_id, document_id=document.id, title=document.filename, text=text)
    return DocumentResponse.model_validate(document)


@router.get("/projects/{project_id}/documents", response_model=list[DocumentResponse])
def list_documents(
    project_id: UUID,
    db: Session = Depends(get_db),
    context: RequestContext = Depends(get_request_context),
) -> list[Document]:
    statement = select(Document).where(
        Document.project_id == project_id,
        Document.organization_id == context.organization_id,
    )
    return list(db.scalars(statement))


@router.post("/projects/{project_id}/chat", response_model=ChatResponse)
def chat_with_documents(
    project_id: UUID,
    payload: ChatRequest,
    context: RequestContext = Depends(get_request_context),
) -> ChatResponse:
    result = rag_service.answer(project_id=project_id, question=payload.message)
    return ChatResponse(
        answer=result.answer,
        citations=[
            Citation(document_id=item.document_id, title=item.title, excerpt=item.excerpt)
            for item in result.citations
        ],
    )
