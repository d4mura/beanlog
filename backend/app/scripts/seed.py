"""Seed script: insert flavor notes and origin master data."""

import json
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.config import settings

SHARED_DIR = Path(__file__).resolve().parent.parent.parent.parent / "shared" / "constants"


def seed_flavor_notes(session):
    """Insert flavor notes from shared constants."""
    data = json.loads((SHARED_DIR / "flavor_tags.json").read_text())
    for item in data:
        session.execute(
            text("""
                INSERT INTO flavor_notes (slug, name, name_en, category, category_en, sort_order)
                VALUES (:slug, :name, :name_en, :category, :category_en, :sort_order)
                ON CONFLICT (slug) DO NOTHING
            """),
            item,
        )
    session.commit()
    print(f"Seeded {len(data)} flavor notes.")


def seed_origins(session):
    """Insert origin countries from shared constants."""
    data = json.loads((SHARED_DIR / "origins.json").read_text())
    for item in data:
        session.execute(
            text("""
                INSERT INTO origins (country_code, name, name_en)
                VALUES (:country_code, :name, :name_en)
                ON CONFLICT (country_code, region) DO NOTHING
            """),
            {**item, "region": None},
        )
    session.commit()
    print(f"Seeded {len(data)} origins.")


def main():
    engine = create_engine(settings.database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        seed_flavor_notes(session)
        seed_origins(session)
        print("Seed completed successfully.")
    except Exception as e:
        session.rollback()
        print(f"Seed failed: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
