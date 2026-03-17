from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.models.segment import Segment
from app.schemas.segment import SegmentCreate, SegmentUpdate
from app.utils.network import overlaps, parse_network, validate_ip_in_network


def segment_query(db: Session):
    return db.query(Segment).options(
        joinedload(Segment.pool),
        joinedload(Segment.location),
        joinedload(Segment.node),
        joinedload(Segment.validations),
        joinedload(Segment.audits),
    )


def get_overlap_messages(db: Session) -> list[str]:
    segments = db.query(Segment).order_by(Segment.id.asc()).all()
    messages: list[str] = []
    for idx, segment in enumerate(segments):
        for other in segments[idx + 1 :]:
            if overlaps(segment.cidr, other.cidr):
                messages.append(f"Solapamiento detectado entre {segment.cidr} y {other.cidr}")
    return messages


def ensure_segment_integrity(db: Session, payload: SegmentCreate | SegmentUpdate, segment_id: int | None = None):
    network = parse_network(payload.cidr)
    duplicate = db.query(Segment).filter(Segment.cidr == str(network)).first()
    if duplicate and duplicate.id != segment_id:
        raise ValueError("El segmento ya existe")

    segments = db.query(Segment).all()
    for segment in segments:
        if segment.id == segment_id:
            continue
        if overlaps(segment.cidr, str(network)):
            raise ValueError(f"El segmento se traslapa con {segment.cidr}")

    if payload.primary_validation_ip:
        validate_ip_in_network(payload.primary_validation_ip, str(network))
    return network


def apply_segment_fields(segment: Segment, payload: SegmentCreate | SegmentUpdate, network, user_id: int | None):
    segment.name = payload.name
    segment.cidr = str(network)
    segment.network_address = str(network.network_address)
    segment.prefix_length = network.prefixlen
    segment.network_type = payload.network_type
    segment.description = payload.description
    segment.vlan = payload.vlan
    segment.equipment = payload.equipment
    segment.status = payload.status
    segment.observations = payload.observations
    segment.is_pool_member = payload.is_pool_member
    segment.pool_id = payload.pool_id
    segment.location_id = payload.location_id
    segment.node_id = payload.node_id
    segment.primary_validation_ip = payload.primary_validation_ip
    segment.scan_multiple_ips = payload.scan_multiple_ips
    segment.validation_frequency_minutes = payload.validation_frequency_minutes
    segment.snmp_community = payload.snmp_community
    segment.updated_by_id = user_id
    if not segment.created_by_id:
        segment.created_by_id = user_id


def apply_filters(
    query,
    search: str | None,
    network_type: str | None,
    status: str | None,
    location_id: int | None,
    node_id: int | None,
    pool_id: int | None,
    vlan: str | None,
):
    if search:
        term = f"%{search}%"
        query = query.filter(
            or_(
                Segment.cidr.ilike(term),
                Segment.description.ilike(term),
                Segment.vlan.ilike(term),
                Segment.equipment.ilike(term),
                Segment.name.ilike(term),
                Segment.observations.ilike(term),
            )
        )
    if network_type:
        query = query.filter(Segment.network_type == network_type)
    if status:
        query = query.filter(Segment.status == status)
    if location_id:
        query = query.filter(Segment.location_id == location_id)
    if node_id:
        query = query.filter(Segment.node_id == node_id)
    if pool_id:
        query = query.filter(Segment.pool_id == pool_id)
    if vlan:
        query = query.filter(Segment.vlan == vlan)
    return query
