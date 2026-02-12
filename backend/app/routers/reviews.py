from fastapi import APIRouter, Query

from app.dependencies import CurrentUserId, DbSession
from app.schemas.review import (
    ReviewCreate,
    ReviewCreateResponse,
    ReviewDeleteResponse,
    ReviewListResponse,
    ReviewUpdate,
)
from app.services import review_service

router = APIRouter()


@router.get("/beans/{bean_id}/reviews", response_model=ReviewListResponse)
def list_bean_reviews(
    db: DbSession,
    bean_id: str,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=50),
):
    return review_service.list_reviews_for_bean(db, bean_id, page=page, per_page=per_page)


@router.post("/beans/{bean_id}/reviews", response_model=ReviewCreateResponse, status_code=201)
def create_review(
    db: DbSession,
    bean_id: str,
    data: ReviewCreate,
    user_id: CurrentUserId,
):
    return review_service.create_review(db, bean_id, user_id, data)


@router.patch("/reviews/{review_id}", response_model=ReviewCreateResponse)
def update_review(
    db: DbSession,
    review_id: str,
    data: ReviewUpdate,
    user_id: CurrentUserId,
):
    return review_service.update_review(db, review_id, user_id, data)


@router.delete("/reviews/{review_id}", response_model=ReviewDeleteResponse)
def delete_review(
    db: DbSession,
    review_id: str,
    user_id: CurrentUserId,
):
    return review_service.delete_review(db, review_id, user_id)


@router.get("/users/{user_id}/reviews", response_model=ReviewListResponse)
def list_user_reviews(
    db: DbSession,
    user_id: str,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=50),
):
    return review_service.list_reviews_for_user(db, user_id, page=page, per_page=per_page)
