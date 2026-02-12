from math import ceil

from sqlalchemy.orm import Session

from app.repositories import bean_repo
from app.schemas.bean import (
    BeanDetail,
    BeanDetailResponse,
    BeanListItem,
    BeanListResponse,
    OriginInfo,
    RatingDistribution,
)
from app.schemas.common import PaginationMeta
from app.schemas.roaster import RoasterSummary


def _bean_to_list_item(bean) -> BeanListItem:
    origin = None
    if bean.origin:
        origin = OriginInfo(
            code=bean.origin.country_code,
            name=bean.origin.name,
            name_en=bean.origin.name_en,
            region=bean.origin.region,
            region_en=bean.origin.region_en,
        )
    roaster = None
    if bean.roaster:
        roaster = RoasterSummary(
            id=str(bean.roaster.id),
            name=bean.roaster.name,
            name_en=bean.roaster.name_en,
        )
    flavor_slugs = [bfn.flavor_note.slug for bfn in bean.flavor_notes]
    return BeanListItem(
        id=str(bean.id),
        name=bean.name,
        name_en=bean.name_en,
        roaster=roaster,
        origin=origin,
        roast_level=bean.roast_level,
        process=bean.process,
        flavor_notes=flavor_slugs,
        avg_rating=float(bean.avg_rating) if bean.avg_rating else None,
        review_count=bean.review_count,
        image_url=bean.image_url,
        created_at=bean.created_at,
    )


def _bean_to_detail(bean, rating_dist: dict) -> BeanDetail:
    origin = None
    if bean.origin:
        origin = OriginInfo(
            code=bean.origin.country_code,
            name=bean.origin.name,
            name_en=bean.origin.name_en,
            region=bean.origin.region,
            region_en=bean.origin.region_en,
        )
    roaster = None
    if bean.roaster:
        roaster = RoasterSummary(
            id=str(bean.roaster.id),
            name=bean.roaster.name,
            name_en=bean.roaster.name_en,
        )
    flavor_slugs = [bfn.flavor_note.slug for bfn in bean.flavor_notes]
    return BeanDetail(
        id=str(bean.id),
        name=bean.name,
        name_en=bean.name_en,
        description=bean.description,
        description_en=bean.description_en,
        roaster=roaster,
        origin=origin,
        variety=bean.variety,
        process=bean.process,
        roast_level=bean.roast_level,
        altitude_min=bean.altitude_min,
        altitude_max=bean.altitude_max,
        flavor_notes=flavor_slugs,
        barcode=bean.barcode,
        avg_rating=float(bean.avg_rating) if bean.avg_rating else None,
        review_count=bean.review_count,
        rating_distribution=RatingDistribution(
            five=rating_dist.get("5", 0),
            four=rating_dist.get("4", 0),
            three=rating_dist.get("3", 0),
            two=rating_dist.get("2", 0),
            one=rating_dist.get("1", 0),
        ),
        image_url=bean.image_url,
        purchase_url=bean.purchase_url,
        created_at=bean.created_at,
        updated_at=bean.updated_at,
    )


def list_beans(
    db: Session,
    *,
    q: str | None = None,
    origin: str | None = None,
    roast_level: str | None = None,
    process: str | None = None,
    flavor: str | None = None,
    roaster_id: str | None = None,
    sort: str = "created_desc",
    page: int = 1,
    per_page: int = 20,
) -> BeanListResponse:
    beans, total = bean_repo.get_beans(
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
    return BeanListResponse(
        data=[_bean_to_list_item(b) for b in beans],
        meta=PaginationMeta(
            page=page,
            per_page=per_page,
            total=total,
            total_pages=ceil(total / per_page) if total > 0 else 0,
        ),
    )


def get_bean(db: Session, bean_id: str) -> BeanDetailResponse | None:
    bean = bean_repo.get_bean_by_id(db, bean_id)
    if not bean:
        return None
    rating_dist = bean_repo.get_rating_distribution(db, bean_id)
    return BeanDetailResponse(data=_bean_to_detail(bean, rating_dist))


def get_bean_by_barcode(db: Session, barcode: str) -> BeanDetailResponse | None:
    bean = bean_repo.get_bean_by_barcode(db, barcode)
    if not bean:
        return None
    rating_dist = bean_repo.get_rating_distribution(db, str(bean.id))
    return BeanDetailResponse(data=_bean_to_detail(bean, rating_dist))
