from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def log_segment_action(db: Session, segment_id: int, action: str, user_id: int | None, details: str | None = None) -> None:
    db.add(AuditLog(segment_id=segment_id, action=action, user_id=user_id, details=details))
