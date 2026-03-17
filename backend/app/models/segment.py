from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.mixins import TimestampMixin


class Segment(TimestampMixin, Base):
    __tablename__ = "segments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    cidr: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    network_address: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    prefix_length: Mapped[int] = mapped_column(Integer, nullable=False)
    network_type: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    vlan: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    equipment: Mapped[str | None] = mapped_column(String(150), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active", index=True)
    observations: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_pool_member: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    primary_validation_ip: Mapped[str | None] = mapped_column(String(32), nullable=True)
    scan_multiple_ips: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    validation_frequency_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=15)
    snmp_community: Mapped[str | None] = mapped_column(String(120), nullable=True)
    last_ping_ok: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    last_snmp_ok: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    last_validation_at: Mapped[str | None] = mapped_column(String(40), nullable=True)
    last_response_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    last_validation_error: Mapped[str | None] = mapped_column(Text, nullable=True)

    pool_id: Mapped[int | None] = mapped_column(ForeignKey("pools.id"), nullable=True)
    location_id: Mapped[int | None] = mapped_column(ForeignKey("locations.id"), nullable=True)
    node_id: Mapped[int | None] = mapped_column(ForeignKey("nodes.id"), nullable=True)
    created_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    updated_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    pool = relationship("Pool", back_populates="segments")
    location = relationship("Location", back_populates="segments")
    node = relationship("Node", back_populates="segments")
    validations = relationship("ValidationResult", back_populates="segment", cascade="all, delete-orphan")
    audits = relationship("AuditLog", back_populates="segment", cascade="all, delete-orphan")
    created_by = relationship("User", foreign_keys=[created_by_id], back_populates="created_segments")
    updated_by = relationship("User", foreign_keys=[updated_by_id], back_populates="updated_segments")
