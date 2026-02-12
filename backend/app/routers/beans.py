from fastapi import APIRouter, HTTPException, Query

from app.dependencies import DbSession
from app.schemas.bean import BeanDetailResponse, BeanListResponse
from app.services import bean_service

router = APIRouter()


@router.get("/beans", response_model=BeanListResponse)
def list_beans(
    db: DbSession,
    q: str | None = Query(None, description="Full-text search"),
    origin: str | None = Query(None, description="Origin country code (ISO 3166-1 alpha-2)"),
    roast_level: str | None = Query(None, description="Roast level filter"),
    process: str | None = Query(None, description="Process filter"),
    flavor: str | None = Query(None, description="Flavor note slugs (comma-separated)"),
    roaster_id: str | None = Query(None, description="Roaster ID filter"),
    sort: str = Query("created_desc", description="Sort order"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=50, description="Items per page"),
):
    return bean_service.list_beans(
        db,
        q=q,
        origin=origin,
        roast_level=roast_level,
        process=process,
        flavor=flavor,
        roaster_id=roaster_id,
        sort=sort,
        page=page,
        per_page=per_page,
    )


@router.get("/beans/barcode/{code}", response_model=BeanDetailResponse)
def get_bean_by_barcode(db: DbSession, code: str):
    result = bean_service.get_bean_by_barcode(db, code)
    if not result:
        raise HTTPException(
            status_code=404,
            detail={"code": "BEAN_NOT_FOUND", "message": f"No bean found for barcode: {code}"},
        )
    return result


@router.get("/beans/{bean_id}", response_model=BeanDetailResponse)
def get_bean(db: DbSession, bean_id: str):
    result = bean_service.get_bean(db, bean_id)
    if not result:
        raise HTTPException(status_code=404, detail="Bean not found")
    return result
