from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings


def _fix_db_url(url: str) -> str:
    """Fly.io uses postgres:// but SQLAlchemy requires postgresql://."""
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url


engine = create_engine(_fix_db_url(settings.database_url), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]


# Dev user ID used when Supabase auth is not configured
_DEV_USER_ID = "00000000-0000-0000-0000-000000000001"


def _is_auth_configured() -> bool:
    return bool(settings.supabase_url and settings.supabase_service_role_key)


def get_current_user_id(authorization: str = Header(default="")) -> str:
    """Extract and verify user ID from Supabase JWT token.

    In development mode (no SUPABASE_URL configured), returns a fixed dev user ID.
    """
    if not _is_auth_configured():
        # Dev mode: skip auth, return dev user
        return _DEV_USER_ID

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is required",
        )
    token = authorization.replace("Bearer ", "")
    try:
        from supabase import create_client

        client = create_client(settings.supabase_url, settings.supabase_service_role_key)
        user_response = client.auth.get_user(token)
        if not user_response or not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        return str(user_response.user.id)
    except ImportError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="supabase package not installed; cannot verify token",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
        )


def get_optional_user_id(authorization: str = Header(default="")) -> str | None:
    """Optionally extract user ID — returns None if no valid auth."""
    if not _is_auth_configured():
        return _DEV_USER_ID
    if not authorization:
        return None
    try:
        return get_current_user_id(authorization)
    except HTTPException:
        return None


CurrentUserId = Annotated[str, Depends(get_current_user_id)]
OptionalUserId = Annotated[str | None, Depends(get_optional_user_id)]
