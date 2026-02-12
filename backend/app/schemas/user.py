from datetime import datetime

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str
    avatar_url: str | None = None
    preferred_language: str = "ja"


class UserUpdate(BaseModel):
    username: str | None = None
    avatar_url: str | None = None
    preferred_language: str | None = Field(None, pattern=r"^(ja|en)$")


class UserPublic(BaseModel):
    id: str
    username: str
    avatar_url: str | None = None

    model_config = {"from_attributes": True}


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    avatar_url: str | None = None
    preferred_language: str
    review_count: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}


class UserMeResponse(BaseModel):
    data: UserResponse
