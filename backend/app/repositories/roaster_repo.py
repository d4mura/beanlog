import uuid

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.bean import Bean
from app.models.roaster import Roaster


def get_roasters(
    db: Session,
    *,
    q: str | None = None,
    page: int = 1,
    per_page: int = 20,
) -> tuple[list[dict], int]:
    query = db.query(
        Roaster,
        func.count(Bean.id).label("bean_count"),
        func.round(func.avg(Bean.avg_rating), 1).label("avg_rating"),
    ).outerjoin(Bean, (Bean.roaster_id == Roaster.id) & (Bean.deleted_at.is_(None)))

    if q:
        query = query.filter(Roaster.name.ilike(f"%{q}%"))

    query = query.group_by(Roaster.id).order_by(Roaster.name.asc())
    total = query.count()
    results = query.offset((page - 1) * per_page).limit(per_page).all()

    items = []
    for roaster, bean_count, avg_rating in results:
        items.append({
            "id": str(roaster.id),
            "name": roaster.name,
            "name_en": roaster.name_en,
            "location": roaster.location,
            "bean_count": bean_count,
            "avg_rating": float(avg_rating) if avg_rating else None,
            "image_url": roaster.image_url,
        })
    return items, total


def get_roaster_by_id(db: Session, roaster_id: str) -> dict | None:
    roaster = (
        db.query(Roaster)
        .options(joinedload(Roaster.beans))
        .filter(Roaster.id == uuid.UUID(roaster_id))
        .first()
    )
    if not roaster:
        return None

    active_beans = [b for b in roaster.beans if b.deleted_at is None]
    avg = None
    if active_beans:
        ratings = [float(b.avg_rating) for b in active_beans if b.avg_rating]
        avg = round(sum(ratings) / len(ratings), 1) if ratings else None

    return {
        "id": str(roaster.id),
        "name": roaster.name,
        "name_en": roaster.name_en,
        "description": roaster.description,
        "description_en": roaster.description_en,
        "location": roaster.location,
        "prefecture": roaster.prefecture,
        "website_url": roaster.website_url,
        "instagram_url": roaster.instagram_url,
        "image_url": roaster.image_url,
        "bean_count": len(active_beans),
        "avg_rating": avg,
        "beans": [
            {
                "id": str(b.id),
                "name": b.name,
                "avg_rating": float(b.avg_rating) if b.avg_rating else None,
                "review_count": b.review_count,
            }
            for b in active_beans
        ],
        "created_at": roaster.created_at,
    }
