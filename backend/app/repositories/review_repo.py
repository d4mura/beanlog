import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session, joinedload

from app.models.flavor_note import FlavorNote
from app.models.review import Review, ReviewFlavorNote


def get_reviews_by_bean(
    db: Session,
    bean_id: str,
    *,
    page: int = 1,
    per_page: int = 20,
) -> tuple[list[Review], int]:
    query = (
        db.query(Review)
        .options(
            joinedload(Review.user),
            joinedload(Review.flavor_notes).joinedload(ReviewFlavorNote.flavor_note),
        )
        .filter(Review.bean_id == uuid.UUID(bean_id), Review.deleted_at.is_(None))
        .order_by(Review.created_at.desc())
    )
    total = query.count()
    reviews = query.offset((page - 1) * per_page).limit(per_page).all()
    return reviews, total


def get_reviews_by_user(
    db: Session,
    user_id: str,
    *,
    page: int = 1,
    per_page: int = 20,
) -> tuple[list[Review], int]:
    query = (
        db.query(Review)
        .options(
            joinedload(Review.user),
            joinedload(Review.flavor_notes).joinedload(ReviewFlavorNote.flavor_note),
        )
        .filter(Review.user_id == uuid.UUID(user_id), Review.deleted_at.is_(None))
        .order_by(Review.created_at.desc())
    )
    total = query.count()
    reviews = query.offset((page - 1) * per_page).limit(per_page).all()
    return reviews, total


def get_review_by_id(db: Session, review_id: str) -> Review | None:
    return (
        db.query(Review)
        .options(
            joinedload(Review.user),
            joinedload(Review.flavor_notes).joinedload(ReviewFlavorNote.flavor_note),
        )
        .filter(Review.id == uuid.UUID(review_id), Review.deleted_at.is_(None))
        .first()
    )


def check_duplicate_review(db: Session, bean_id: str, user_id: str) -> bool:
    return (
        db.query(Review)
        .filter(
            Review.bean_id == uuid.UUID(bean_id),
            Review.user_id == uuid.UUID(user_id),
            Review.deleted_at.is_(None),
        )
        .first()
        is not None
    )


def create_review(
    db: Session,
    *,
    bean_id: str,
    user_id: str,
    rating: float,
    brew_method: str | None,
    comment: str | None,
    flavor_slugs: list[str],
) -> Review:
    review = Review(
        bean_id=uuid.UUID(bean_id),
        user_id=uuid.UUID(user_id),
        rating=rating,
        brew_method=brew_method,
        comment=comment,
    )
    db.add(review)
    db.flush()

    if flavor_slugs:
        notes = db.query(FlavorNote).filter(FlavorNote.slug.in_(flavor_slugs)).all()
        for note in notes:
            rfn = ReviewFlavorNote(review_id=review.id, flavor_note_id=note.id)
            db.add(rfn)

    db.commit()
    db.refresh(review)
    return get_review_by_id(db, str(review.id))


def update_review(
    db: Session,
    review: Review,
    *,
    rating: float | None = None,
    brew_method: str | None = None,
    comment: str | None = None,
    flavor_slugs: list[str] | None = None,
) -> Review:
    if rating is not None:
        review.rating = rating
    if brew_method is not None:
        review.brew_method = brew_method
    if comment is not None:
        review.comment = comment

    if flavor_slugs is not None:
        # Clear existing and re-add
        db.query(ReviewFlavorNote).filter(ReviewFlavorNote.review_id == review.id).delete()
        notes = db.query(FlavorNote).filter(FlavorNote.slug.in_(flavor_slugs)).all()
        for note in notes:
            rfn = ReviewFlavorNote(review_id=review.id, flavor_note_id=note.id)
            db.add(rfn)

    db.commit()
    db.refresh(review)
    return get_review_by_id(db, str(review.id))


def soft_delete_review(db: Session, review: Review) -> None:
    review.deleted_at = datetime.now(timezone.utc)
    db.commit()
