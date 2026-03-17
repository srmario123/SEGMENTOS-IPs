from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.location import Location
from app.models.node import Node
from app.models.pool import Pool
from app.models.user import User
from app.schemas.location import LocationCreate, LocationRead, LocationUpdate
from app.schemas.node import NodeCreate, NodeRead, NodeUpdate
from app.schemas.pool import PoolCreate, PoolRead, PoolUpdate
from app.services.auth import get_current_user, require_roles

router = APIRouter(tags=["catalogs"])


@router.get("/locations", response_model=list[LocationRead])
def list_locations(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Location).order_by(Location.name.asc()).all()


@router.post("/locations", response_model=LocationRead)
def create_location(
    payload: LocationCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "operator")),
):
    item = Location(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/locations/{item_id}", response_model=LocationRead)
def update_location(
    item_id: int,
    payload: LocationUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "operator")),
):
    item = db.get(Location, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    for key, value in payload.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/locations/{item_id}")
def delete_location(item_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles("admin"))):
    item = db.get(Location, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    db.delete(item)
    db.commit()
    return {"message": "Eliminado"}


@router.get("/nodes", response_model=list[NodeRead])
def list_nodes(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Node).order_by(Node.name.asc()).all()


@router.post("/nodes", response_model=NodeRead)
def create_node(payload: NodeCreate, db: Session = Depends(get_db), _: User = Depends(require_roles("admin", "operator"))):
    item = Node(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/nodes/{item_id}", response_model=NodeRead)
def update_node(item_id: int, payload: NodeUpdate, db: Session = Depends(get_db), _: User = Depends(require_roles("admin", "operator"))):
    item = db.get(Node, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Nodo no encontrado")
    for key, value in payload.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/nodes/{item_id}")
def delete_node(item_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles("admin"))):
    item = db.get(Node, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Nodo no encontrado")
    db.delete(item)
    db.commit()
    return {"message": "Eliminado"}


@router.get("/pools", response_model=list[PoolRead])
def list_pools(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Pool).order_by(Pool.name.asc()).all()


@router.post("/pools", response_model=PoolRead)
def create_pool(payload: PoolCreate, db: Session = Depends(get_db), _: User = Depends(require_roles("admin", "operator"))):
    item = Pool(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/pools/{item_id}", response_model=PoolRead)
def update_pool(item_id: int, payload: PoolUpdate, db: Session = Depends(get_db), _: User = Depends(require_roles("admin", "operator"))):
    item = db.get(Pool, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Pool no encontrado")
    for key, value in payload.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/pools/{item_id}")
def delete_pool(item_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles("admin"))):
    item = db.get(Pool, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Pool no encontrado")
    db.delete(item)
    db.commit()
    return {"message": "Eliminado"}
