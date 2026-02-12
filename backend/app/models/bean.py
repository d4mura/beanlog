import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Bean(Base):
    __tablename__ = "beans"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    name_en: Mapped[str | None] = mapped_column(String, nullable=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    description_en: Mapped[str | None] = mapped_column(String, nullable=True)
    roaster_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("roasters.id"), nullable=False
    )
    origin_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("origins.id"), nullable=True
    )
    variety: Mapped[str | None] = mapped_column(String, nullable=True)
    process: Mapped[str | None] = mapped_column(String, nullable=True)
    roast_level: Mapped[str | None] = mapped_column(String, nullable=True)
    altitude_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    altitude_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    barcode: Mapped[str | None] = mapped_column(String, nullable=True, unique=True)
    image_url: Mapped[str | None] = mapped_column(String, nullable=True)
    purchase_url: Mapped[str | None] = mapped_column(String, nullable=True)
    avg_rating: Mapped[float] = mapped_column(Numeric(2, 1), default=0.0)
    review_count: Mapped[int] = mapped_column(Integer, default=0)
    flavor_embedding = mapped_column(Vector(384), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    roaster: Mapped["Roaster"] = relationship(back_populates="beans")  # noqa: F821
    origin: Mapped["Origin | None"] = relationship()  # noqa: F821
    reviews: Mapped[list["Review"]] = relationship(back_populates="bean")  # noqa: F821
    flavor_notes: Mapped[list["BeanFlavorNote"]] = relationship(
        back_populates="bean", cascade="all, delete-orphan"
    )


class BeanFlavorNote(Base):
    __tablename__ = "bean_flavor_notes"
    __table_args__ = (
        UniqueConstraint("bean_id", "flavor_note_id", name="uq_bean_flavor_note"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    bean_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("beans.id", ondelete="CASCADE"), nullable=False
    )
    flavor_note_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("flavor_notes.id"), nullable=False
    )

    bean: Mapped["Bean"] = relationship(back_populates="flavor_notes")
    flavor_note: Mapped["FlavorNote"] = relationship()  # noqa: F821
