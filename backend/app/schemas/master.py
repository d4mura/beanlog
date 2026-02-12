from pydantic import BaseModel


class OriginResponse(BaseModel):
    id: str
    country_code: str
    name: str
    name_en: str
    region: str | None = None
    region_en: str | None = None

    model_config = {"from_attributes": True}


class FlavorNoteResponse(BaseModel):
    id: str
    slug: str
    name: str
    name_en: str
    category: str
    category_en: str
    sort_order: int

    model_config = {"from_attributes": True}


class ProcessResponse(BaseModel):
    value: str
    name: str
    name_en: str


class RoastLevelResponse(BaseModel):
    value: str
    name: str
    name_en: str


class BrewMethodResponse(BaseModel):
    value: str
    name: str
    name_en: str
