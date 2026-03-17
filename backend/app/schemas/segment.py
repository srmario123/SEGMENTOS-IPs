from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.schemas.audit import AuditRead
from app.schemas.common import ORMModel
from app.schemas.location import LocationRead
from app.schemas.node import NodeRead
from app.schemas.pool import PoolRead
from app.schemas.validation import ValidationRead


class SegmentBase(BaseModel):
    name: str
    cidr: str
    network_type: str = Field(pattern="^(public|private)$")
    description: str | None = None
    vlan: str | None = None
    equipment: str | None = None
    status: str = Field(pattern="^(active|in_use|reserved|free|disabled)$")
    observations: str | None = None
    is_pool_member: bool = False
    pool_id: int | None = None
    location_id: int | None = None
    node_id: int | None = None
    primary_validation_ip: str | None = None
    scan_multiple_ips: bool = False
    validation_frequency_minutes: int = Field(default=15, ge=5, le=1440)
    snmp_community: str | None = None

    @field_validator("cidr")
    @classmethod
    def strip_cidr(cls, value: str) -> str:
        return value.strip()


class SegmentCreate(SegmentBase):
    pass


class SegmentUpdate(SegmentBase):
    pass


class SegmentRead(ORMModel):
    id: int
    name: str
    cidr: str
    network_address: str
    prefix_length: int
    network_type: str
    description: str | None
    vlan: str | None
    equipment: str | None
    status: str
    observations: str | None
    is_pool_member: bool
    pool_id: int | None
    location_id: int | None
    node_id: int | None
    primary_validation_ip: str | None
    scan_multiple_ips: bool
    validation_frequency_minutes: int
    snmp_community: str | None
    last_ping_ok: bool | None
    last_snmp_ok: bool | None
    last_validation_at: str | None
    last_response_time_ms: int | None
    last_validation_error: str | None
    created_at: datetime
    updated_at: datetime
    pool: PoolRead | None = None
    location: LocationRead | None = None
    node: NodeRead | None = None


class SegmentDetail(SegmentRead):
    validations: list[ValidationRead] = []
    audits: list[AuditRead] = []


class SegmentListResponse(BaseModel):
    items: list[SegmentRead]
    total: int
    overlap_alerts: list[str]


class DashboardResponse(BaseModel):
    total_segments: int
    public_segments: int
    private_segments: int
    active_segments: int
    inactive_segments: int
    validation_ok: int
    ping_fail: int
    snmp_fail: int
    overlap_alerts: list[str]
