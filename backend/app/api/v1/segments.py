import csv
import io

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.segment import Segment
from app.models.user import User
from app.schemas.segment import DashboardResponse, SegmentCreate, SegmentDetail, SegmentListResponse, SegmentRead, SegmentUpdate
from app.schemas.validation import ValidationRead, ValidationRunRequest
from app.services.audit import log_segment_action
from app.services.auth import get_current_user, require_roles
from app.services.segment_service import apply_filters, apply_segment_fields, ensure_segment_integrity, get_overlap_messages, segment_query
from app.services.validation_service import run_segment_validation

router = APIRouter(prefix="/segments", tags=["segments"])


@router.get("", response_model=SegmentListResponse)
def list_segments(
    search: str | None = None,
    network_type: str | None = None,
    status: str | None = None,
    location_id: int | None = None,
    node_id: int | None = None,
    pool_id: int | None = None,
    vlan: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = apply_filters(segment_query(db), search, network_type, status, location_id, node_id, pool_id, vlan)
    items = query.order_by(Segment.created_at.desc()).all()
    return SegmentListResponse(items=items, total=len(items), overlap_alerts=get_overlap_messages(db))


@router.get("/dashboard", response_model=DashboardResponse)
def dashboard(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return DashboardResponse(
        total_segments=db.query(func.count(Segment.id)).scalar() or 0,
        public_segments=db.query(func.count(Segment.id)).filter(Segment.network_type == "public").scalar() or 0,
        private_segments=db.query(func.count(Segment.id)).filter(Segment.network_type == "private").scalar() or 0,
        active_segments=db.query(func.count(Segment.id)).filter(Segment.status.in_(["active", "in_use"])).scalar() or 0,
        inactive_segments=db.query(func.count(Segment.id)).filter(Segment.status.in_(["reserved", "free", "disabled"])).scalar() or 0,
        validation_ok=db.query(func.count(Segment.id)).filter(Segment.last_ping_ok.is_(True), Segment.last_snmp_ok.is_(True)).scalar() or 0,
        ping_fail=db.query(func.count(Segment.id)).filter(Segment.last_ping_ok.is_(False)).scalar() or 0,
        snmp_fail=db.query(func.count(Segment.id)).filter(Segment.last_snmp_ok.is_(False)).scalar() or 0,
        overlap_alerts=get_overlap_messages(db),
    )


@router.get("/export/csv")
def export_csv(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "name",
            "cidr",
            "network_type",
            "description",
            "vlan",
            "equipment",
            "status",
            "observations",
            "primary_validation_ip",
            "validation_frequency_minutes",
        ]
    )
    for segment in db.query(Segment).order_by(Segment.id.asc()).all():
        writer.writerow(
            [
                segment.name,
                segment.cidr,
                segment.network_type,
                segment.description or "",
                segment.vlan or "",
                segment.equipment or "",
                segment.status,
                segment.observations or "",
                segment.primary_validation_ip or "",
                segment.validation_frequency_minutes,
            ]
        )
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=segments.csv"},
    )


@router.post("/import/csv")
async def import_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("admin", "operator")),
):
    content = (await file.read()).decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))
    created = 0
    errors: list[str] = []
    for index, row in enumerate(reader, start=2):
        try:
            payload = SegmentCreate(
                name=row["name"],
                cidr=row["cidr"],
                network_type=row["network_type"],
                description=row.get("description"),
                vlan=row.get("vlan"),
                equipment=row.get("equipment"),
                status=row.get("status", "active"),
                observations=row.get("observations"),
                primary_validation_ip=row.get("primary_validation_ip") or None,
                validation_frequency_minutes=int(row.get("validation_frequency_minutes") or 15),
            )
            network = ensure_segment_integrity(db, payload)
            segment = Segment()
            apply_segment_fields(segment, payload, network, user.id)
            db.add(segment)
            db.flush()
            log_segment_action(db, segment.id, "import", user.id, f"Importado desde CSV en línea {index}")
            db.commit()
            created += 1
        except Exception as exc:
            db.rollback()
            errors.append(f"Línea {index}: {exc}")
    return {"created": created, "errors": errors}


@router.get("/{segment_id}", response_model=SegmentDetail)
def get_segment(segment_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    segment = segment_query(db).filter(Segment.id == segment_id).first()
    if not segment:
        raise HTTPException(status_code=404, detail="Segmento no encontrado")
    return segment


@router.post("", response_model=SegmentRead)
def create_segment(payload: SegmentCreate, db: Session = Depends(get_db), user: User = Depends(require_roles("admin", "operator"))):
    try:
        network = ensure_segment_integrity(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    segment = Segment()
    apply_segment_fields(segment, payload, network, user.id)
    db.add(segment)
    db.flush()
    log_segment_action(db, segment.id, "create", user.id, f"Segmento {segment.cidr} creado")
    db.commit()
    db.refresh(segment)
    return segment


@router.put("/{segment_id}", response_model=SegmentRead)
def update_segment(
    segment_id: int,
    payload: SegmentUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("admin", "operator")),
):
    segment = db.get(Segment, segment_id)
    if not segment:
        raise HTTPException(status_code=404, detail="Segmento no encontrado")
    try:
        network = ensure_segment_integrity(db, payload, segment_id=segment_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    apply_segment_fields(segment, payload, network, user.id)
    log_segment_action(db, segment.id, "update", user.id, f"Segmento {segment.cidr} actualizado")
    db.commit()
    db.refresh(segment)
    return segment


@router.delete("/{segment_id}")
def delete_segment(segment_id: int, db: Session = Depends(get_db), user: User = Depends(require_roles("admin"))):
    segment = db.get(Segment, segment_id)
    if not segment:
        raise HTTPException(status_code=404, detail="Segmento no encontrado")
    log_segment_action(db, segment.id, "delete", user.id, f"Segmento {segment.cidr} eliminado")
    db.delete(segment)
    db.commit()
    return {"message": "Segmento eliminado"}


@router.post("/{segment_id}/validate", response_model=list[ValidationRead])
async def validate_segment(
    segment_id: int,
    payload: ValidationRunRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("admin", "operator")),
):
    segment = db.get(Segment, segment_id)
    if not segment:
        raise HTTPException(status_code=404, detail="Segmento no encontrado")
    try:
        results = await run_segment_validation(db, segment, payload.validation_ip, payload.scan_multiple_ips, user.username)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    log_segment_action(db, segment.id, "validate", user.id, f"Validación ejecutada sobre {segment.cidr}")
    db.commit()
    for result in results:
        db.refresh(result)
    return results


@router.get("/{segment_id}/validations", response_model=list[ValidationRead])
def segment_validations(segment_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    segment = db.get(Segment, segment_id)
    if not segment:
        raise HTTPException(status_code=404, detail="Segmento no encontrado")
    return segment.validations
