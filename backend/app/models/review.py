import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (
        UniqueConstraint("bean_id", "user_id", name="uq_review_bean_user"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    bean_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("beans.id"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    rating: Mapped[float] = mapped_column(Numeric(2, 1), nullable=False)
    brew_method: Mapped[str | None] = mapped_column(String, nullable=True)
    comment: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    bean: Mapped["Bean"] = relationship(back_populates="reviews")  # noqa: F821
    user: Mapped["User"] = relationship(back_populates="reviews")  # noqa: F821
    flavor_notes: Mapped[list["ReviewFlavorNote"]] = relationship(
        back_populates="review", cascade="all, delete-orphan"
    )


class ReviewFlavorNote(Base):
    __tablename__ = "review_flavor_notes"
    __table_args__ = (
        UniqueConstraint("review_id", "flavor_note_id", name="uq_review_flavor_note"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    review_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("reviews.id", ondelete="CASCADE"), nullable=False
    )
    flavor_note_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("flavor_notes.id"), nullable=False
    )

    review: Mapped["Review"] = relationship(back_populates="flavor_notes")
    flavor_note: Mapped["FlavorNote"] = relationship()  # noqa: F821
