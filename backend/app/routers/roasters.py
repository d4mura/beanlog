from fastapi import APIRouter, Query

from app.dependencies import DbSession
from app.schemas.roaster import RoasterDetailResponse, RoasterListResponse
from app.services import roaster_service

router = APIRouter()


@router.get("/roasters", response_model=RoasterListResponse)
def list_roasters(
    db: DbSession,
    q: str | None = Query(None, description="Name search"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=50),
):
    return roaster_service.list_roasters(db, q=q, page=page, per_page=per_page)


@router.get("/roasters/{roaster_id}", response_model=RoasterDetailResponse)
def get_roaster(db: DbSession, roaster_id: str):
    return roaster_service.get_roaster(db, roaster_id)
