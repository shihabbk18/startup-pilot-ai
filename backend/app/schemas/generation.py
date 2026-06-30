from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.entities import GeneratorType, JobStatus


class GenerationCreate(BaseModel):
    generator_type: GeneratorType
    additional_context: str | None = Field(default=None, max_length=4000)


class GenerationResponse(BaseModel):
    id: UUID
    project_id: UUID
    generator_type: GeneratorType
    status: JobStatus
    output: dict | None
    error_message: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class FullPlanRequest(BaseModel):
    idea: str = Field(min_length=10, max_length=4000)
    industry: str | None = Field(default=None, max_length=120)


class FullPlanResponse(BaseModel):
    title: str
    sections: dict[str, str | list[str] | dict]
    markdown: str

