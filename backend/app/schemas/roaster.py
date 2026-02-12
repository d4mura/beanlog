from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import PaginationMeta


class RoasterSummary(BaseModel):
    id: str
    name: str
    name_en: str | None = None

    model_config = {"from_attributes": True}


class RoasterListItem(BaseModel):
    id: str
    name: str
    name_en: str | None = None
    location: str | None = None
    bean_count: int = 0
    avg_rating: float | None = None
    image_url: str | None = None

    model_config = {"from_attributes": True}


class RoasterBeanSummary(BaseModel):
    id: str
    name: str
    avg_rating: float | None = None
    review_count: int = 0

    model_config = {"from_attributes": True}


class RoasterDetail(BaseModel):
    id: str
    name: str
    name_en: str | None = None
    description: str | None = None
    description_en: str | None = None
    location: str | None = None
    prefecture: str | None = None
    website_url: str | None = None
    instagram_url: str | None = None
    image_url: str | None = None
    bean_count: int = 0
    avg_rating: float | None = None
    beans: list[RoasterBeanSummary] = []
    created_at: datetime

    model_config = {"from_attributes": True}


class RoasterListResponse(BaseModel):
    data: list[RoasterListItem]
    meta: PaginationMeta


class RoasterDetailResponse(BaseModel):
    data: RoasterDetail
