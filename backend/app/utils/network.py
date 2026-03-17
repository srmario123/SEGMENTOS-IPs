import ipaddress


def parse_network(cidr: str) -> ipaddress.IPv4Network:
    try:
        network = ipaddress.ip_network(cidr, strict=True)
    except ValueError as exc:
        raise ValueError(f"CIDR inválido: {cidr}") from exc
    if network.version != 4:
        raise ValueError("Solo IPv4 está soportado en esta versión")
    return network


def validate_ip_in_network(ip_str: str, cidr: str) -> None:
    network = parse_network(cidr)
    ip = ipaddress.ip_address(ip_str)
    if ip not in network:
        raise ValueError(f"La IP {ip_str} no pertenece al segmento {cidr}")


def get_candidate_ips(cidr: str, preferred_ip: str | None = None, multiple: bool = False) -> list[str]:
    network = parse_network(cidr)
    if preferred_ip:
        validate_ip_in_network(preferred_ip, cidr)
        if not multiple:
            return [preferred_ip]
    hosts = [str(host) for host in network.hosts()]
    if not hosts:
        return [str(network.network_address)]
    if preferred_ip and multiple:
        remaining = [ip for ip in hosts if ip != preferred_ip]
        return [preferred_ip, *remaining[:4]]
    return hosts[:5] if multiple else [hosts[0]]


def overlaps(existing_cidr: str, new_cidr: str) -> bool:
    return parse_network(existing_cidr).overlaps(parse_network(new_cidr))
