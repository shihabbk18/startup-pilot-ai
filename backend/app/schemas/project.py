from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    idea: str = Field(min_length=10, max_length=4000)
    industry: str | None = Field(default=None, max_length=120)


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    idea: str | None = Field(default=None, min_length=10, max_length=4000)
    industry: str | None = Field(default=None, max_length=120)
    stage: str | None = Field(default=None, max_length=50)


class ProjectResponse(BaseModel):
    id: UUID
    organization_id: UUID
    owner_id: UUID
    name: str
    idea: str
    industry: str | None
    stage: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

