from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import ORMModel
from app.schemas.location import LocationRead


class NodeBase(BaseModel):
    name: str
    description: str | None = None
    location_id: int | None = None


class NodeCreate(NodeBase):
    pass


class NodeUpdate(NodeBase):
    pass


class NodeRead(ORMModel):
    id: int
    name: str
    description: str | None
    location_id: int | None
    location: LocationRead | None = None
    created_at: datetime
    updated_at: datetime
