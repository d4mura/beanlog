import uuid
from math import ceil

from sqlalchemy import func, or_
from sqlalchemy.orm import Session, joinedload

from app.models.bean import Bean, BeanFlavorNote
from app.models.flavor_note import FlavorNote
from app.models.review import Review


def get_beans(
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
) -> tuple[list[Bean], int]:
    query = (
        db.query(Bean)
        .options(
            joinedload(Bean.roaster),
            joinedload(Bean.origin),
            joinedload(Bean.flavor_notes).joinedload(BeanFlavorNote.flavor_note),
        )
        .filter(Bean.deleted_at.is_(None))
    )

    if q:
        query = query.filter(
            or_(Bean.name.ilike(f"%{q}%"), Bean.name_en.ilike(f"%{q}%"))
        )
    if origin:
        from app.models.origin import Origin

        query = query.join(Bean.origin).filter(Origin.country_code == origin)
    if roast_level:
        query = query.filter(Bean.roast_level == roast_level)
    if process:
        query = query.filter(Bean.process == process)
    if roaster_id:
        query = query.filter(Bean.roaster_id == uuid.UUID(roaster_id))
    if flavor:
        flavor_slugs = [s.strip() for s in flavor.split(",")]
        query = query.filter(
            Bean.id.in_(
                db.query(BeanFlavorNote.bean_id)
                .join(FlavorNote)
                .filter(FlavorNote.slug.in_(flavor_slugs))
                .subquery()
            )
        )

    total = query.count()

    if sort == "rating_desc":
        query = query.order_by(Bean.avg_rating.desc())
    elif sort == "name_asc":
        query = query.order_by(Bean.name.asc())
    else:
        query = query.order_by(Bean.created_at.desc())

    beans = query.offset((page - 1) * per_page).limit(per_page).all()
    return beans, total


def get_bean_by_id(db: Session, bean_id: str) -> Bean | None:
    return (
        db.query(Bean)
        .options(
            joinedload(Bean.roaster),
            joinedload(Bean.origin),
            joinedload(Bean.flavor_notes).joinedload(BeanFlavorNote.flavor_note),
        )
        .filter(Bean.id == uuid.UUID(bean_id), Bean.deleted_at.is_(None))
        .first()
    )


def get_bean_by_barcode(db: Session, barcode: str) -> Bean | None:
    return (
        db.query(Bean)
        .options(
            joinedload(Bean.roaster),
            joinedload(Bean.origin),
            joinedload(Bean.flavor_notes).joinedload(BeanFlavorNote.flavor_note),
        )
        .filter(Bean.barcode == barcode, Bean.deleted_at.is_(None))
        .first()
    )


def get_rating_distribution(db: Session, bean_id: str) -> dict[str, int]:
    results = (
        db.query(
            func.floor(Review.rating).label("star"),
            func.count().label("cnt"),
        )
        .filter(
            Review.bean_id == uuid.UUID(bean_id),
            Review.deleted_at.is_(None),
        )
        .group_by("star")
        .all()
    )
    dist = {"5": 0, "4": 0, "3": 0, "2": 0, "1": 0}
    for row in results:
        key = str(int(row.star))
        if key in dist:
            dist[key] = row.cnt
    return dist
