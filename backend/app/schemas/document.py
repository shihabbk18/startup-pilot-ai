from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.entities import DocumentStatus


class DocumentResponse(BaseModel):
    id: UUID
    project_id: UUID
    filename: str
    mime_type: str
    storage_path: str
    status: DocumentStatus
    token_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    conversation_id: UUID | None = None


class Citation(BaseModel):
    document_id: UUID | None = None
    title: str
    excerpt: str


class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation]

