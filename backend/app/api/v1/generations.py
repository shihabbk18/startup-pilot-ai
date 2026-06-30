from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import RequestContext, get_request_context
from app.core.config import settings
from app.db.session import get_db
from app.models.entities import Generation, JobStatus
from app.repositories.generations import GenerationRepository
from app.repositories.projects import ProjectRepository
from app.schemas.generation import FullPlanRequest, FullPlanResponse, GenerationCreate, GenerationResponse
from app.services.planning import StartupPlanningEngine, render_markdown

router = APIRouter()
planning_engine = StartupPlanningEngine()


@router.post("/plans/full", response_model=FullPlanResponse)
def generate_full_plan(payload: FullPlanRequest) -> FullPlanResponse:
    sections = planning_engine.build_full_plan(idea=payload.idea, industry=payload.industry)
    title = f"MVP Plan: {payload.idea[:72]}"
    return FullPlanResponse(title=title, sections=sections, markdown=render_markdown(title, sections))


@router.post(
    "/projects/{project_id}/generations",
    response_model=GenerationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_generation(
    project_id: UUID,
    payload: GenerationCreate,
    db: Session = Depends(get_db),
    context: RequestContext = Depends(get_request_context),
) -> GenerationResponse:
    project = ProjectRepository(db).get_for_organization(project_id, context.organization_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    output = planning_engine.build_generator_plan(
        idea=project.idea,
        generator_type=payload.generator_type,
        industry=project.industry,
    )
    generation = Generation(
        organization_id=context.organization_id,
        project_id=project_id,
        user_id=context.user_id,
        generator_type=payload.generator_type,
        status=JobStatus.COMPLETED,
        prompt_version="startup-plan-v1",
        model_name=settings.openai_model,
        input=payload.model_dump(mode="json"),
        output={
            "model": settings.openai_model,
            "sections": output,
            "markdown": render_markdown(payload.generator_type.value.replace("_", " ").title(), output),
        },
    )
    saved = GenerationRepository(db).add(generation)
    return GenerationResponse.model_validate(saved)


@router.get("/projects/{project_id}/generations", response_model=list[GenerationResponse])
def list_generations(
    project_id: UUID,
    db: Session = Depends(get_db),
    context: RequestContext = Depends(get_request_context),
) -> list[Generation]:
    return GenerationRepository(db).list_for_project(project_id, context.organization_id)


@router.get("/generations/{generation_id}", response_model=GenerationResponse)
def get_generation(
    generation_id: UUID,
    db: Session = Depends(get_db),
    context: RequestContext = Depends(get_request_context),
) -> GenerationResponse:
    generation = GenerationRepository(db).get(generation_id)
    if generation and generation.organization_id != context.organization_id:
        generation = None
    if not generation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Generation not found")
    return GenerationResponse.model_validate(generation)
