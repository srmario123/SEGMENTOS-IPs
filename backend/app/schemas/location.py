from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import ORMModel


class LocationBase(BaseModel):
    name: str
    description: str | None = None


class LocationCreate(LocationBase):
    pass


class LocationUpdate(LocationBase):
    pass


class LocationRead(ORMModel):
    id: int
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime
