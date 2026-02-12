"""Seed script: insert flavor notes and origin master data."""

import json
import uuid
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
                INSERT INTO flavor_notes (id, slug, name, name_en, category, category_en, sort_order)
                VALUES (:id, :slug, :name, :name_en, :category, :category_en, :sort_order)
                ON CONFLICT (slug) DO NOTHING
            """),
            {"id": str(uuid.uuid4()), **item},
        )
    session.commit()
    print(f"Seeded {len(data)} flavor notes.")


def seed_origins(session):
    """Insert origin countries from shared constants."""
    data = json.loads((SHARED_DIR / "origins.json").read_text())
    for item in data:
        # Check if already exists (ON CONFLICT with NULL region is tricky)
        existing = session.execute(
            text("SELECT id FROM origins WHERE country_code = :cc AND region IS NULL"),
            {"cc": item["country_code"]},
        ).first()
        if existing:
            continue
        session.execute(
            text("""
                INSERT INTO origins (id, country_code, name, name_en)
                VALUES (:id, :country_code, :name, :name_en)
            """),
            {"id": str(uuid.uuid4()), **item},
        )
    session.commit()
    print(f"Seeded {len(data)} origins.")


def seed_dev_user(session):
    """Insert a dev user for local development."""
    dev_user_id = "00000000-0000-0000-0000-000000000001"
    existing = session.execute(
        text("SELECT id FROM users WHERE id = :id"),
        {"id": dev_user_id},
    ).first()
    if existing:
        print("Dev user already exists.")
        return
    session.execute(
        text("""
            INSERT INTO users (id, username, email, preferred_language)
            VALUES (:id, :username, :email, :preferred_language)
        """),
        {
            "id": dev_user_id,
            "username": "dev_user",
            "email": "dev@example.com",
            "preferred_language": "ja",
        },
    )
    session.commit()
    print("Seeded dev user.")


def main():
    engine = create_engine(settings.database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        seed_flavor_notes(session)
        seed_origins(session)
        seed_dev_user(session)
        print("Seed completed successfully.")
    except Exception as e:
        session.rollback()
        print(f"Seed failed: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
