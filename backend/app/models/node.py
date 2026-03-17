from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.mixins import TimestampMixin


class Node(TimestampMixin, Base):
    __tablename__ = "nodes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    location_id: Mapped[int | None] = mapped_column(ForeignKey("locations.id"), nullable=True)

    location = relationship("Location", back_populates="nodes")
    segments = relationship("Segment", back_populates="node")
