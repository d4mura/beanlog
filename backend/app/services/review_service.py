from math import ceil

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import review_repo
from app.schemas.common import PaginationMeta
from app.schemas.review import (
    ReviewCreate,
    ReviewCreateResponse,
    ReviewDeleteResponse,
    ReviewListResponse,
    ReviewResponse,
    ReviewUpdate,
)
from app.schemas.user import UserPublic


def _review_to_response(review) -> ReviewResponse:
    flavor_slugs = [rfn.flavor_note.slug for rfn in review.flavor_notes]
    return ReviewResponse(
        id=str(review.id),
        bean_id=str(review.bean_id),
        user=UserPublic(
            id=str(review.user.id),
            username=review.user.username,
            avatar_url=review.user.avatar_url,
        ),
        rating=float(review.rating),
        flavor_notes=flavor_slugs,
        brew_method=review.brew_method,
        comment=review.comment,
        created_at=review.created_at,
        updated_at=review.updated_at,
    )


def list_reviews_for_bean(
    db: Session,
    bean_id: str,
    *,
    page: int = 1,
    per_page: int = 20,
) -> ReviewListResponse:
    reviews, total = review_repo.get_reviews_by_bean(db, bean_id, page=page, per_page=per_page)
    return ReviewListResponse(
        data=[_review_to_response(r) for r in reviews],
        meta=PaginationMeta(
            page=page,
            per_page=per_page,
            total=total,
            total_pages=ceil(total / per_page) if total > 0 else 0,
        ),
    )


def list_reviews_for_user(
    db: Session,
    user_id: str,
    *,
    page: int = 1,
    per_page: int = 20,
) -> ReviewListResponse:
    reviews, total = review_repo.get_reviews_by_user(db, user_id, page=page, per_page=per_page)
    return ReviewListResponse(
        data=[_review_to_response(r) for r in reviews],
        meta=PaginationMeta(
            page=page,
            per_page=per_page,
            total=total,
            total_pages=ceil(total / per_page) if total > 0 else 0,
        ),
    )


def create_review(
    db: Session,
    bean_id: str,
    user_id: str,
    data: ReviewCreate,
) -> ReviewCreateResponse:
    if review_repo.check_duplicate_review(db, bean_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "code": "DUPLICATE_REVIEW",
                "message": "You have already reviewed this bean. Please edit your existing review.",
            },
        )
    review = review_repo.create_review(
        db,
        bean_id=bean_id,
        user_id=user_id,
        rating=data.rating,
        brew_method=data.brew_method,
        comment=data.comment,
        flavor_slugs=data.flavor_notes,
    )
    return ReviewCreateResponse(data=_review_to_response(review))


def update_review(
    db: Session,
    review_id: str,
    user_id: str,
    data: ReviewUpdate,
) -> ReviewCreateResponse:
    review = review_repo.get_review_by_id(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if str(review.user_id) != user_id:
        raise HTTPException(status_code=403, detail="Not allowed to edit this review")

    updated = review_repo.update_review(
        db,
        review,
        rating=data.rating,
        brew_method=data.brew_method,
        comment=data.comment,
        flavor_slugs=data.flavor_notes,
    )
    return ReviewCreateResponse(data=_review_to_response(updated))


def delete_review(
    db: Session,
    review_id: str,
    user_id: str,
) -> ReviewDeleteResponse:
    review = review_repo.get_review_by_id(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if str(review.user_id) != user_id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this review")
    review_repo.soft_delete_review(db, review)
    return ReviewDeleteResponse(data={"id": str(review.id), "deleted": True})
