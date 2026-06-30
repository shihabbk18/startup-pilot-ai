import re

from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.db.session import get_db
from app.models.entities import Membership, Organization, OrganizationRole, User
from app.schemas.auth import CurrentUserResponse, LoginRequest, RegisterRequest, TokenResponse

router = APIRouter()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "organization"


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> TokenResponse:
    """Register a user, organization, and owner membership."""
    existing_user = db.scalar(select(User).where(User.email == payload.email))
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    base_slug = slugify(payload.organization_name)
    slug = base_slug
    suffix = 2
    while db.scalar(select(Organization).where(Organization.slug == slug)):
        slug = f"{base_slug}-{suffix}"
        suffix += 1

    organization = Organization(name=payload.organization_name, slug=slug)
    user = User(
        email=str(payload.email),
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
    )
    db.add_all([organization, user])
    db.flush()
    db.add(Membership(organization_id=organization.id, user_id=user.id, role=OrganizationRole.OWNER))
    db.commit()
    return TokenResponse(access_token=create_access_token(user.id, organization.id))


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.scalar(select(User).where(User.email == payload.email))
    if not user or not user.hashed_password or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    membership = db.scalar(select(Membership).where(Membership.user_id == user.id))
    if not membership:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No organization membership")
    return TokenResponse(access_token=create_access_token(user.id, membership.organization_id))


@router.get("/me", response_model=CurrentUserResponse)
def me(
    authorization: str = Header(default=""),
    db: Session = Depends(get_db),
) -> CurrentUserResponse:
    from app.core.security import decode_access_token

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format")
    payload = decode_access_token(token)
    user_id = UUID(payload["sub"])
    user = db.get(User, user_id)
    membership = db.scalar(select(Membership).where(Membership.user_id == user_id))
    if not user or not membership:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return CurrentUserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        organization_id=membership.organization_id,
        role=membership.role.value,
    )
