from datetime import UTC, datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import RequestContext, get_request_context
from app.db.session import get_db
from app.models.entities import Project
from app.repositories.projects import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate

router = APIRouter()


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    context: RequestContext = Depends(get_request_context),
) -> Project:
    project = Project(
        organization_id=context.organization_id,
        owner_id=context.user_id,
        name=payload.name,
        idea=payload.idea,
        industry=payload.industry,
        stage="idea",
    )
    return ProjectRepository(db).add(project)


@router.get("", response_model=list[ProjectResponse])
def list_projects(
    db: Session = Depends(get_db),
    context: RequestContext = Depends(get_request_context),
) -> list[Project]:
    return ProjectRepository(db).list_for_organization(context.organization_id)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: UUID,
    db: Session = Depends(get_db),
    context: RequestContext = Depends(get_request_context),
) -> Project:
    project = ProjectRepository(db).get_for_organization(project_id, context.organization_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: UUID,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
    context: RequestContext = Depends(get_request_context),
) -> Project:
    project = ProjectRepository(db).get_for_organization(project_id, context.organization_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, key, value)
    project.updated_at = datetime.now(UTC)
    db.commit()
    db.refresh(project)
    return project
