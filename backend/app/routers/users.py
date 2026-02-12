import uuid

from fastapi import APIRouter, HTTPException

from app.dependencies import CurrentUserId, DbSession
from app.models.user import User
from app.schemas.user import UserMeResponse, UserResponse, UserUpdate

router = APIRouter()


@router.get("/users/me", response_model=UserMeResponse)
def get_me(db: DbSession, user_id: CurrentUserId):
    user = db.query(User).filter(User.id == uuid.UUID(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    review_count = len([r for r in user.reviews if r.deleted_at is None])
    return UserMeResponse(
        data=UserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            avatar_url=user.avatar_url,
            preferred_language=user.preferred_language,
            review_count=review_count,
            created_at=user.created_at,
        )
    )


@router.patch("/users/me", response_model=UserMeResponse)
def update_me(db: DbSession, user_id: CurrentUserId, data: UserUpdate):
    user = db.query(User).filter(User.id == uuid.UUID(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if data.username is not None:
        user.username = data.username
    if data.avatar_url is not None:
        user.avatar_url = data.avatar_url
    if data.preferred_language is not None:
        user.preferred_language = data.preferred_language
    db.commit()
    db.refresh(user)
    review_count = len([r for r in user.reviews if r.deleted_at is None])
    return UserMeResponse(
        data=UserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            avatar_url=user.avatar_url,
            preferred_language=user.preferred_language,
            review_count=review_count,
            created_at=user.created_at,
        )
    )


@router.get("/users/{target_user_id}", response_model=dict)
def get_user_profile(db: DbSession, target_user_id: str):
    user = db.query(User).filter(User.id == uuid.UUID(target_user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "data": {
            "id": str(user.id),
            "username": user.username,
            "avatar_url": user.avatar_url,
        }
    }
