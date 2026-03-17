from datetime import datetime

from app.schemas.common import ORMModel


class AuditRead(ORMModel):
    id: int
    segment_id: int
    user_id: int | None
    action: str
    details: str | None
    created_at: datetime
