"""Initial schema - all tables

Revision ID: 001
Revises:
Create Date: 2026-02-12
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

try:
    from pgvector.sqlalchemy import Vector
    HAS_PGVECTOR = True
except ImportError:
    HAS_PGVECTOR = False

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Extensions
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    try:
        op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    except Exception:
        pass  # pgvector not available - Phase 0 doesn't need it

    # --- users ---
    op.create_table(
        "users",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("username", sa.String, nullable=False, unique=True),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("avatar_url", sa.String, nullable=True),
        sa.Column("preferred_language", sa.String, nullable=False, server_default="ja"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("preferred_language IN ('ja', 'en')", name="ck_users_language"),
    )

    # --- roasters ---
    op.create_table(
        "roasters",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("name_en", sa.String, nullable=True),
        sa.Column("description", sa.String, nullable=True),
        sa.Column("description_en", sa.String, nullable=True),
        sa.Column("location", sa.String, nullable=True),
        sa.Column("prefecture", sa.String, nullable=True),
        sa.Column("website_url", sa.String, nullable=True),
        sa.Column("instagram_url", sa.String, nullable=True),
        sa.Column("image_url", sa.String, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.execute("CREATE INDEX idx_roasters_name ON roasters USING gin (name gin_trgm_ops)")
    op.create_index("idx_roasters_prefecture", "roasters", ["prefecture"])

    # --- origins ---
    op.create_table(
        "origins",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("country_code", sa.String, nullable=False),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("name_en", sa.String, nullable=False),
        sa.Column("region", sa.String, nullable=True),
        sa.Column("region_en", sa.String, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("country_code", "region", name="uq_origin_country_region"),
    )
    op.create_index("idx_origins_country", "origins", ["country_code"])

    # --- beans ---
    op.create_table(
        "beans",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("name_en", sa.String, nullable=True),
        sa.Column("description", sa.String, nullable=True),
        sa.Column("description_en", sa.String, nullable=True),
        sa.Column("roaster_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("roasters.id"), nullable=False),
        sa.Column("origin_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("origins.id"), nullable=True),
        sa.Column("variety", sa.String, nullable=True),
        sa.Column("process", sa.String, nullable=True),
        sa.Column("roast_level", sa.String, nullable=True),
        sa.Column("altitude_min", sa.Integer, nullable=True),
        sa.Column("altitude_max", sa.Integer, nullable=True),
        sa.Column("barcode", sa.String, nullable=True, unique=True),
        sa.Column("image_url", sa.String, nullable=True),
        sa.Column("purchase_url", sa.String, nullable=True),
        sa.Column("avg_rating", sa.Numeric(2, 1), server_default="0.0"),
        sa.Column("review_count", sa.Integer, server_default="0"),
        sa.Column("flavor_embedding", Vector(384) if HAS_PGVECTOR else sa.LargeBinary, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "process IN ('washed','natural','honey','anaerobic','carbonic_maceration','other')",
            name="ck_beans_process",
        ),
        sa.CheckConstraint(
            "roast_level IN ('light','medium_light','medium','medium_dark','dark')",
            name="ck_beans_roast_level",
        ),
    )
    op.create_index("idx_beans_roaster", "beans", ["roaster_id"])
    op.create_index("idx_beans_origin", "beans", ["origin_id"])
    op.create_index("idx_beans_process", "beans", ["process"])
    op.create_index("idx_beans_roast_level", "beans", ["roast_level"])
    op.execute("CREATE INDEX idx_beans_barcode ON beans (barcode) WHERE barcode IS NOT NULL")
    op.execute("CREATE INDEX idx_beans_name_trgm ON beans USING gin (name gin_trgm_ops)")
    op.create_index("idx_beans_avg_rating", "beans", [sa.text("avg_rating DESC")])
    op.create_index("idx_beans_created", "beans", [sa.text("created_at DESC")])
    op.execute("CREATE INDEX idx_beans_deleted ON beans (deleted_at) WHERE deleted_at IS NULL")

    # --- flavor_notes ---
    op.create_table(
        "flavor_notes",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("slug", sa.String, nullable=False, unique=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("name_en", sa.String, nullable=False),
        sa.Column("category", sa.String, nullable=False),
        sa.Column("category_en", sa.String, nullable=False),
        sa.Column("sort_order", sa.Integer, nullable=False, server_default="0"),
    )
    op.create_index("idx_flavor_notes_category", "flavor_notes", ["category"])
    op.create_index("idx_flavor_notes_slug", "flavor_notes", ["slug"])

    # --- bean_flavor_notes ---
    op.create_table(
        "bean_flavor_notes",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("bean_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("beans.id", ondelete="CASCADE"), nullable=False),
        sa.Column("flavor_note_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("flavor_notes.id"), nullable=False),
        sa.UniqueConstraint("bean_id", "flavor_note_id", name="uq_bean_flavor_note"),
    )
    op.create_index("idx_bean_flavor_bean", "bean_flavor_notes", ["bean_id"])
    op.create_index("idx_bean_flavor_note", "bean_flavor_notes", ["flavor_note_id"])

    # --- reviews ---
    op.create_table(
        "reviews",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("bean_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("beans.id"), nullable=False),
        sa.Column("user_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("rating", sa.Numeric(2, 1), nullable=False),
        sa.Column("brew_method", sa.String, nullable=True),
        sa.Column("comment", sa.String, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("bean_id", "user_id", name="uq_review_bean_user"),
        sa.CheckConstraint("rating >= 1.0 AND rating <= 5.0", name="ck_reviews_rating"),
        sa.CheckConstraint(
            "brew_method IN ('pour_over','espresso','french_press','aeropress','siphon','cold_brew','other')",
            name="ck_reviews_brew_method",
        ),
        sa.CheckConstraint("char_length(comment) <= 1000", name="ck_reviews_comment_len"),
    )
    op.execute("CREATE INDEX idx_reviews_bean ON reviews (bean_id) WHERE deleted_at IS NULL")
    op.execute("CREATE INDEX idx_reviews_user ON reviews (user_id) WHERE deleted_at IS NULL")
    op.create_index("idx_reviews_created", "reviews", [sa.text("created_at DESC")])

    # --- review_flavor_notes ---
    op.create_table(
        "review_flavor_notes",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("review_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("reviews.id", ondelete="CASCADE"), nullable=False),
        sa.Column("flavor_note_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("flavor_notes.id"), nullable=False),
        sa.UniqueConstraint("review_id", "flavor_note_id", name="uq_review_flavor_note"),
    )
    op.create_index("idx_review_flavor_review", "review_flavor_notes", ["review_id"])
    op.create_index("idx_review_flavor_note", "review_flavor_notes", ["flavor_note_id"])

    # --- Triggers ---
    # updated_at trigger function
    op.execute("""
        CREATE OR REPLACE FUNCTION public.set_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    for table in ["users", "beans", "roasters", "reviews"]:
        op.execute(f"""
            CREATE TRIGGER set_updated_at_{table}
                BEFORE UPDATE ON {table}
                FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();
        """)

    # Bean rating auto-update trigger
    op.execute("""
        CREATE OR REPLACE FUNCTION public.update_bean_rating()
        RETURNS TRIGGER AS $$
        BEGIN
            UPDATE beans SET
                avg_rating = (
                    SELECT ROUND(AVG(rating), 1)
                    FROM reviews
                    WHERE bean_id = COALESCE(NEW.bean_id, OLD.bean_id)
                      AND deleted_at IS NULL
                ),
                review_count = (
                    SELECT COUNT(*)
                    FROM reviews
                    WHERE bean_id = COALESCE(NEW.bean_id, OLD.bean_id)
                      AND deleted_at IS NULL
                ),
                updated_at = NOW()
            WHERE id = COALESCE(NEW.bean_id, OLD.bean_id);
            RETURN COALESCE(NEW, OLD);
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        CREATE TRIGGER trigger_update_bean_rating
            AFTER INSERT OR UPDATE OR DELETE ON reviews
            FOR EACH ROW EXECUTE FUNCTION public.update_bean_rating();
    """)

    # --- RLS policies ---
    # Note: RLS requires Supabase auth.uid(). For local development with direct
    # backend access, the table owner (beanlog) bypasses RLS automatically.
    # These policies are designed for when direct client access is needed via Supabase.
    for table in ["users", "reviews", "beans", "roasters", "origins", "flavor_notes"]:
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
        # Table owner bypasses RLS, but to be safe for any role:
        op.execute(f'CREATE POLICY "allow_all_{table}" ON {table} USING (true) WITH CHECK (true)')


def downgrade() -> None:
    op.drop_table("review_flavor_notes")
    op.drop_table("bean_flavor_notes")
    op.drop_table("reviews")
    op.drop_table("flavor_notes")
    op.drop_table("beans")
    op.drop_table("origins")
    op.drop_table("roasters")
    op.drop_table("users")
    op.execute("DROP FUNCTION IF EXISTS public.update_bean_rating() CASCADE")
    op.execute("DROP FUNCTION IF EXISTS public.set_updated_at() CASCADE")
