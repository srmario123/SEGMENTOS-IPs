from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.mixins import TimestampMixin


class ValidationResult(TimestampMixin, Base):
    __tablename__ = "validations"

    id: Mapped[int] = mapped_column(primary_key=True)
    segment_id: Mapped[int] = mapped_column(ForeignKey("segments.id"), nullable=False, index=True)
    validation_ip: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(20), nullable=False, default="single")
    ping_ok: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    snmp_ok: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    response_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    validated_by: Mapped[str] = mapped_column(String(50), nullable=False, default="system")

    segment = relationship("Segment", back_populates="validations")
