import platform
import re
import subprocess
from datetime import datetime, timezone
from time import perf_counter

from pysnmp.hlapi.asyncio import CommunityData, ContextData, ObjectIdentity, ObjectType, SnmpEngine, UdpTransportTarget
from pysnmp.hlapi.asyncio import get_cmd
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.segment import Segment
from app.models.validation import ValidationResult
from app.utils.network import get_candidate_ips


async def ping_ip(ip: str) -> tuple[bool, int | None, str | None]:
    is_windows = platform.system().lower().startswith("win")
    args = ["ping", "-n", "1", "-w", "1000", ip] if is_windows else ["ping", "-c", "1", "-W", "1", ip]
    start = perf_counter()
    try:
        completed = subprocess.run(args, capture_output=True, text=True, timeout=3, check=False)
        elapsed = int((perf_counter() - start) * 1000)
        success = completed.returncode == 0
        output = f"{completed.stdout}\n{completed.stderr}"
        if success:
            if is_windows:
                match = re.search(r"Average = (\d+)ms", output)
            else:
                match = re.search(r"time=(\d+(?:\.\d+)?) ms", output)
            if match:
                elapsed = int(float(match.group(1)))
        return success, elapsed, None if success else output.strip()[:400]
    except Exception as exc:
        return False, None, str(exc)


async def snmp_probe(ip: str, community: str) -> tuple[bool, str | None]:
    try:
        error_indication, error_status, _, _ = await get_cmd(
            SnmpEngine(),
            CommunityData(community, mpModel=1),
            await UdpTransportTarget.create((ip, 161), timeout=1, retries=0),
            ContextData(),
            ObjectType(ObjectIdentity("1.3.6.1.2.1.1.1.0")),
        )
        if error_indication:
            return False, str(error_indication)
        if error_status:
            return False, str(error_status)
        return True, None
    except Exception as exc:
        return False, str(exc)


async def run_segment_validation(db: Session, segment: Segment, requested_ip: str | None, scan_multiple_ips: bool, actor: str):
    settings = get_settings()
    ips = get_candidate_ips(segment.cidr, requested_ip or segment.primary_validation_ip, scan_multiple_ips or segment.scan_multiple_ips)
    results: list[ValidationResult] = []
    ping_any_ok = False
    snmp_any_ok = False
    best_response: int | None = None
    errors: list[str] = []

    for ip in ips:
        ping_ok, response_time, ping_error = await ping_ip(ip)
        snmp_ok, snmp_error = await snmp_probe(ip, segment.snmp_community or settings.global_snmp_community)
        errors_for_ip = [error for error in [ping_error, snmp_error] if error]
        result = ValidationResult(
            segment_id=segment.id,
            validation_ip=ip,
            mode="scan" if len(ips) > 1 else "single",
            ping_ok=ping_ok,
            snmp_ok=snmp_ok,
            response_time_ms=response_time,
            error_message=" | ".join(errors_for_ip) if errors_for_ip else None,
            validated_by=actor,
        )
        db.add(result)
        results.append(result)
        ping_any_ok = ping_any_ok or ping_ok
        snmp_any_ok = snmp_any_ok or snmp_ok
        if response_time is not None:
            best_response = response_time if best_response is None else min(best_response, response_time)
        if errors_for_ip:
            errors.extend(errors_for_ip)

    segment.last_ping_ok = ping_any_ok
    segment.last_snmp_ok = snmp_any_ok
    segment.last_validation_at = datetime.now(timezone.utc).isoformat()
    segment.last_response_time_ms = best_response
    segment.last_validation_error = " | ".join(errors[:3]) if errors else None
    db.flush()
    return results
