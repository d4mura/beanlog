import json
from pathlib import Path

from fastapi import APIRouter

from app.dependencies import DbSession
from app.models.flavor_note import FlavorNote
from app.models.origin import Origin
from app.schemas.master import (
    BrewMethodResponse,
    FlavorNoteResponse,
    OriginResponse,
    ProcessResponse,
    RoastLevelResponse,
)

router = APIRouter()

SHARED_DIR = Path(__file__).resolve().parent.parent.parent.parent / "shared" / "constants"


@router.get("/master/origins", response_model=dict)
def list_origins(db: DbSession):
    origins = db.query(Origin).order_by(Origin.country_code).all()
    return {
        "data": [
            OriginResponse(
                id=str(o.id),
                country_code=o.country_code,
                name=o.name,
                name_en=o.name_en,
                region=o.region,
                region_en=o.region_en,
            )
            for o in origins
        ]
    }


@router.get("/master/flavors", response_model=dict)
def list_flavors(db: DbSession):
    notes = db.query(FlavorNote).order_by(FlavorNote.sort_order).all()
    return {
        "data": [
            FlavorNoteResponse(
                id=str(n.id),
                slug=n.slug,
                name=n.name,
                name_en=n.name_en,
                category=n.category,
                category_en=n.category_en,
                sort_order=n.sort_order,
            )
            for n in notes
        ]
    }


@router.get("/master/processes", response_model=dict)
def list_processes():
    data = json.loads((SHARED_DIR / "processes.json").read_text())
    return {"data": [ProcessResponse(**item) for item in data]}


@router.get("/master/roast-levels", response_model=dict)
def list_roast_levels():
    data = json.loads((SHARED_DIR / "roast_levels.json").read_text())
    return {"data": [RoastLevelResponse(**item) for item in data]}


@router.get("/master/brew-methods", response_model=dict)
def list_brew_methods():
    data = json.loads((SHARED_DIR / "brew_methods.json").read_text())
    return {"data": [BrewMethodResponse(**item) for item in data]}
