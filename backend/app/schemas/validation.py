from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import ORMModel


class ValidationRunRequest(BaseModel):
    validation_ip: str | None = None
    scan_multiple_ips: bool = False


class ValidationRead(ORMModel):
    id: int
    segment_id: int
    validation_ip: str
    mode: str
    ping_ok: bool
    snmp_ok: bool
    response_time_ms: int | None
    error_message: str | None
    validated_by: str
    created_at: datetime
