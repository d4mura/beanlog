from math import ceil

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import roaster_repo
from app.schemas.common import PaginationMeta
from app.schemas.roaster import (
    RoasterDetail,
    RoasterDetailResponse,
    RoasterListItem,
    RoasterListResponse,
)


def list_roasters(
    db: Session,
    *,
    q: str | None = None,
    page: int = 1,
    per_page: int = 20,
) -> RoasterListResponse:
    items, total = roaster_repo.get_roasters(db, q=q, page=page, per_page=per_page)
    return RoasterListResponse(
        data=[RoasterListItem(**item) for item in items],
        meta=PaginationMeta(
            page=page,
            per_page=per_page,
            total=total,
            total_pages=ceil(total / per_page) if total > 0 else 0,
        ),
    )


def get_roaster(db: Session, roaster_id: str) -> RoasterDetailResponse:
    data = roaster_repo.get_roaster_by_id(db, roaster_id)
    if not data:
        raise HTTPException(status_code=404, detail="Roaster not found")
    return RoasterDetailResponse(data=RoasterDetail(**data))
