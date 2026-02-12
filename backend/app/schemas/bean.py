from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import PaginationMeta
from app.schemas.roaster import RoasterSummary


class OriginInfo(BaseModel):
    code: str
    name: str
    name_en: str
    region: str | None = None
    region_en: str | None = None

    model_config = {"from_attributes": True}


class BeanListItem(BaseModel):
    id: str
    name: str
    name_en: str | None = None
    roaster: RoasterSummary | None = None
    origin: OriginInfo | None = None
    roast_level: str | None = None
    process: str | None = None
    flavor_notes: list[str] = []
    avg_rating: float | None = None
    review_count: int = 0
    image_url: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class RatingDistribution(BaseModel):
    five: int = 0
    four: int = 0
    three: int = 0
    two: int = 0
    one: int = 0


class BeanDetail(BaseModel):
    id: str
    name: str
    name_en: str | None = None
    description: str | None = None
    description_en: str | None = None
    roaster: RoasterSummary | None = None
    origin: OriginInfo | None = None
    variety: str | None = None
    process: str | None = None
    roast_level: str | None = None
    altitude_min: int | None = None
    altitude_max: int | None = None
    flavor_notes: list[str] = []
    barcode: str | None = None
    avg_rating: float | None = None
    review_count: int = 0
    rating_distribution: RatingDistribution | None = None
    image_url: str | None = None
    purchase_url: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class BeanListResponse(BaseModel):
    data: list[BeanListItem]
    meta: PaginationMeta


class BeanDetailResponse(BaseModel):
    data: BeanDetail
