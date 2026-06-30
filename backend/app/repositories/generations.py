from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import Generation
from app.repositories.base import Repository


class GenerationRepository(Repository[Generation]):
    """Repository for AI generation jobs."""

    def __init__(self, db: Session) -> None:
        super().__init__(db, Generation)

    def list_for_project(self, project_id: UUID, organization_id: UUID) -> list[Generation]:
        statement = (
            select(Generation)
            .where(
                Generation.project_id == project_id,
                Generation.organization_id == organization_id,
            )
            .order_by(Generation.created_at.desc())
        )
        return list(self.db.scalars(statement))

