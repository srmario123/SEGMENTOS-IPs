from datetime import datetime, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.models.segment import Segment
from app.services.validation_service import run_segment_validation

scheduler = AsyncIOScheduler(timezone="UTC")


async def validate_due_segments():
    db = SessionLocal()
    try:
        segments = db.query(Segment).all()
        now = datetime.now(timezone.utc)
        for segment in segments:
            if not segment.last_validation_at:
                await run_segment_validation(db, segment, None, False, "scheduler")
                continue
            last = datetime.fromisoformat(segment.last_validation_at)
            delta_minutes = (now - last).total_seconds() / 60
            if delta_minutes >= segment.validation_frequency_minutes:
                await run_segment_validation(db, segment, None, False, "scheduler")
        db.commit()
    finally:
        db.close()


def start_scheduler():
    settings = get_settings()
    if not settings.scheduler_enabled or scheduler.running:
        return
    scheduler.add_job(validate_due_segments, "interval", minutes=5, id="segment-validation", replace_existing=True)
    scheduler.start()


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
