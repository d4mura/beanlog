from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import PaginationMeta
from app.schemas.user import UserPublic


class ReviewCreate(BaseModel):
    rating: float = Field(..., ge=1.0, le=5.0)
    flavor_notes: list[str] = Field(default=[], max_length=5)
    brew_method: str | None = Field(
        None, pattern=r"^(pour_over|espresso|french_press|aeropress|siphon|cold_brew|other)$"
    )
    comment: str | None = Field(None, max_length=1000)


class ReviewUpdate(BaseModel):
    rating: float | None = Field(None, ge=1.0, le=5.0)
    flavor_notes: list[str] | None = Field(None, max_length=5)
    brew_method: str | None = Field(
        None, pattern=r"^(pour_over|espresso|french_press|aeropress|siphon|cold_brew|other)$"
    )
    comment: str | None = Field(None, max_length=1000)


class ReviewResponse(BaseModel):
    id: str
    bean_id: str
    user: UserPublic
    rating: float
    flavor_notes: list[str] = []
    brew_method: str | None = None
    comment: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ReviewListResponse(BaseModel):
    data: list[ReviewResponse]
    meta: PaginationMeta


class ReviewCreateResponse(BaseModel):
    data: ReviewResponse


class ReviewDeleteResponse(BaseModel):
    data: dict
