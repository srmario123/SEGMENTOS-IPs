from app.core.security import get_password_hash
from app.db.session import Base, SessionLocal, engine
from app.models.location import Location
from app.models.node import Node
from app.models.pool import Pool
from app.models.segment import Segment
from app.models.user import User


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.username == "admin").first():
            db.add_all(
                [
                    User(username="admin", full_name="Administrador NOC", email="admin@example.com", role="admin", password_hash=get_password_hash("admin123")),
                    User(username="operador", full_name="Operador NOC", email="operador@example.com", role="operator", password_hash=get_password_hash("operador123")),
                    User(username="viewer", full_name="Solo Lectura", email="viewer@example.com", role="viewer", password_hash=get_password_hash("viewer123")),
                ]
            )
        if not db.query(Location).first():
            santiago = Location(name="Santiago DC", description="Datacenter principal")
            valpo = Location(name="Valparaiso POP", description="Punto de presencia regional")
            db.add_all([santiago, valpo])
            db.flush()
            n1 = Node(name="NODO-STGO-01", description="Core metropolitano", location_id=santiago.id)
            n2 = Node(name="NODO-VAPO-01", description="Agregación costa", location_id=valpo.id)
            pool = Pool(name="Pool CGNAT", description="Bloques para clientes residenciales")
            db.add_all([n1, n2, pool])
            db.flush()
            db.add_all(
                [
                    Segment(
                        name="LAN Gestion Core",
                        cidr="10.10.10.0/24",
                        network_address="10.10.10.0",
                        prefix_length=24,
                        network_type="private",
                        description="Segmento de gestion del core",
                        vlan="110",
                        equipment="CRS-Core-01",
                        status="active",
                        observations="Gateway en .1",
                        is_pool_member=False,
                        primary_validation_ip="10.10.10.1",
                        validation_frequency_minutes=15,
                        location_id=santiago.id,
                        node_id=n1.id,
                    ),
                    Segment(
                        name="Pool Clientes Norte",
                        cidr="45.170.10.0/24",
                        network_address="45.170.10.0",
                        prefix_length=24,
                        network_type="public",
                        description="Pool publico para clientes norte",
                        vlan="210",
                        equipment="BNG-01",
                        status="in_use",
                        observations="Asignacion dinamica",
                        is_pool_member=True,
                        primary_validation_ip="45.170.10.1",
                        validation_frequency_minutes=30,
                        location_id=valpo.id,
                        node_id=n2.id,
                        pool_id=pool.id,
                    ),
                ]
            )
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    main()
