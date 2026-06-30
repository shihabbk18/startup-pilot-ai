from dataclasses import dataclass
from uuid import UUID

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db


@dataclass(frozen=True)
class RequestContext:
    user_id: UUID
    organization_id: UUID
    role: str = "owner"


def get_request_context(
    authorization: str | None = Header(default=None),
) -> RequestContext:
    """Resolve the authenticated request context.

    Local development can pass `X-Dev-User` headers in tests, but production should require JWT.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
        )
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format")
    try:
        payload = decode_access_token(token)
        return RequestContext(
            user_id=UUID(payload["sub"]),
            organization_id=UUID(payload["org"]),
        )
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc


DbSession = Depends(get_db)
Context = Depends(get_request_context)

