from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import Project
from app.repositories.base import Repository


class ProjectRepository(Repository[Project]):
    """Repository for tenant-scoped project access."""

    def __init__(self, db: Session) -> None:
        super().__init__(db, Project)

    def list_for_organization(self, organization_id: UUID) -> list[Project]:
        statement = (
            select(Project)
            .where(Project.organization_id == organization_id)
            .order_by(Project.updated_at.desc())
        )
        return list(self.db.scalars(statement))

    def get_for_organization(self, project_id: UUID, organization_id: UUID) -> Project | None:
        statement = select(Project).where(
            Project.id == project_id,
            Project.organization_id == organization_id,
        )
        return self.db.scalar(statement)

